#=========================imports=========================
from textx import metamodel_from_file
from string import Template
from owlready2 import *
from string import Template
import re

from specification_generator.config import *

#=========================Setup===========================
#------------------------Grammar--------------------------
conspec_metamodel = metamodel_from_file(grammar_file)
#------------------------Ontology-------------------------
onto = get_ontology(f"file://{ontology_file_path}").load()

#-----------------------Templating------------------------
lookup = {}
templates = {}
#========================Functions========================

#------------------------Ontology-------------------------
def print_hierarchy(cls, level=0):
    print("  " * level + cls.name)
    for sub_cls in cls.subclasses():
        print_hierarchy(sub_cls, level + 1)

def load_onto(cls,onto_data,level=0):
    onto_data[cls.name] = dict()
    for sub_cls in cls.subclasses():
        load_onto(sub_cls,onto_data[cls.name],level+1)

def extract_features(data):
    global objects
    for key in data.keys():
        lt = re.split(r"(?=[A-Z])", key)
        word = lt[0].capitalize()
        if word in objects.keys():
            if not objects[word]:
                objects[word]["features"] = list()
            objects[word]["features"].append(str(lt[1]))

#-----------------------Templating------------------------
def fill_template(template, values):
    # Substitute values in the current template
    filled_template = template.safe_substitute(values)
    
    # Check if the substitution introduced new template patterns to be filled
    while True:
        temp_template = Template(filled_template)
        try:
            # Try to substitute again
            new_filled_template = temp_template.safe_substitute(values)
            # Break the loop if no further substitutions are there
            if new_filled_template == filled_template:
                break
            filled_template = new_filled_template
        except KeyError:
            # Stop when there are no keys to substitute
            break
    
    return filled_template

def declarations_stub(classes,concepts,nn,rep):
    sub = ""

    for cls in classes:
        cls = cls.lower()
        sub = sub + f"class {cls}\n"
    sub = sub + "\n"
    for con in concepts:
        con = con.lower()
        sub = sub + f"con {con}\n"
    sub = sub + "\n"

    sub = sub + f"network {nn}\n"
    sub = sub + f"rep {rep}\n"
    sub = sub + "\n"
    
    return sub

def main_template_stub(id,cls):
    cls = cls.lower()
    module_name = f"module_{id}"
    out = lookup[cls]

    sub = f"Module {module_name} $cls_triple"
    sub = sub + " {\n\t$predict_stub \n\t$has_feature_stub\n \n\t$strength_predicate_stub\n}\n\n"
                                              
    return Template(sub)


def id_generator(cls,cls_relevant_features,cls_irrelevant_features,nn,rep):
    cls = cls.lower()
    id = f"{cls}"
    cls_triple = f"({nn},{cls},{rep})"
    inp_features = []

    lookup[id] = dict()
    
    for i,feat in enumerate(cls_relevant_features):
        feat_name = f"{cls}_feat{i}"
        lookup[id][feat_name] = feat
        inp_features.append(f"{cls}_feat{i}")
    
    
    lookup[id]["cls_name"] = cls
    lookup[id]["cls_features"] = inp_features
    lookup[id]["cls_triple"] = Template(cls_triple)
    lookup[id]["cls_irrelevant_features"] = cls_irrelevant_features

def predict_stub(cls,counter):
    cls = cls.lower()
    
    counter += 1
    sub = f"E e{counter} ::> predict({cls})"

    lookup[cls]["predict_stub"] = sub

def has_feature_stub(cls, counter):
    cls = cls.lower()

    sub = ""
    for feat_id in lookup[cls]["cls_features"]:
        counter += 1 
        sub = sub + f"\n\tE e{counter} ::> hasCon(${feat_id})"
    
    lookup[cls]["has_feature_stub"] = Template(sub)
    

def strength_predicate_stub(cls,counter,split=True):
    cls = cls.lower()
    out = lookup[cls]

    sub = ""

    if split:
        for feat_name in out["cls_features"]:
            for j in out["cls_irrelevant_features"]:
                counter +=1
                temp = f"E e{counter} ::> "
                temp = temp + f">({cls},${feat_name},{j})"
                sub = sub + temp + "\n\t"
    else: 
        for feat_name in out["cls_features"]:
            counter +=1
            temp = f"E e{counter} ::> "
            for ind,j in enumerate(out["cls_irrelevant_features"]):
                temp = temp + f">({cls},${feat_name},{j})"
                if not((j == out["cls_irrelevant_features"][-1]) or (feat_name == out["cls_features"][-1] and j == out["cls_irrelevant_features"][-2])):
                    temp = temp + " ^ "
            sub = sub + temp + "\n\t"

    lookup[cls]["strength_predicate_stub"] = Template(sub)

def generate_specifications():
    try:
        with open(spec_file,'w') as file:

            file.write(declarations_stub(classes=list(objects.keys()),concepts=concept_list,nn = nn, rep = rep))

            for ind,object in enumerate(objects.keys()):

                cls_relevant_features = objects[object]["features"]
                cls_irrelevant_features = [feat for feat in concept_list if feat not in cls_relevant_features]
                cls_relevant_features = [feat.lower() for feat in cls_relevant_features]
                cls_irrelevant_features = [feat.lower() for feat in cls_irrelevant_features]

                id = ind
                counter = 0

                id_generator(object,cls_relevant_features,cls_irrelevant_features,nn,rep)
                predict_stub(object,counter)
                has_feature_stub(object,counter)
                strength_predicate_stub(object,counter)

                object = object.lower()
                for key, value in lookup[object].items():
                    if isinstance(value, Template):
                        lookup[object][key] = fill_template(value, lookup[object])

                main_template = main_template_stub(id,object)

                result = fill_template(main_template, lookup[object])
                file.write(result)

    finally:
        file.close()
    
    # conspec = conspec_metamodel.model_from_file(spec_file)
    # return True
    
    try:
        conspec = conspec_metamodel.model_from_file(spec_file)
        print("Syntax check: no errors!")
        return True
    except:
        print("STOP!, The code has syntax errors")
        return False

#------------------------Ontology-------------------------
onto_data = dict()
load_onto(Thing,onto_data)

objects = onto_data["Thing"]["Object"]
concepts = onto_data["Thing"]["Concept"]
extract_features(onto_data["Thing"]["ObjectConcept"])

concept_list = []
for key, value in concepts.items():
    concept_list.append(key)
    if value:
        for k,v in value.items():
            concept_list.append(k)

#-----------------------Templating------------------------
nn = "yolo"
rep = "clip"
    

if __name__ == "__main__":
    generate_specifications()
