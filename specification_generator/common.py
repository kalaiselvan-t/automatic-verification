from string import Template
from specification_generator.config import *

traffic_signs = {
    "ahead_only": {
        "shape": "circle",
        "content": "straight_ahead_arrow"
    },
    "end_of_speed_limit_80": {
        "shape": "circle",
        "content": ["80", "end_of_lines_graphic"]
    },
    "speed_limit_60": {
        "shape": "circle",
        "content": "60"
    },
    "road_work": {
        "shape": "triangle",
        "content": "road_work_graphic"
    },
    "pedestrian": {
        "shape": "triangle",
        "content": "pedestrian_graphic"
    },
    "stop": {
        "shape": "hexagon",
        "content": "stop_text"
    }
}

common_data = {
    "shape": ["circle", "triangle", "hexagon"],
    "content": ["straight_ahead_arrow", 80, 60, "end_of_lines_graphic", "road_work_graphic", "pedestrian_graphic", "stop_text"]
}

concepts= ["shape", "content"]

class Specification_generator:

    def __init__(self,concepts, common_data, traffic_signs, spec_file = spec_file):
        self.lookup = dict()
        self.spec_file = spec_file

        self.concepts = concepts
        self.common_data = common_data
        self.traffic_signs = traffic_signs

        self.generate()
    
    def get_relevant_features(self,cls,attr):
        relevant = self.traffic_signs[cls][attr]
        irrelevant = [item for item in self.common_data[attr] if item != relevant]

        if type(relevant) == str:
            relevant = [relevant]

        return relevant, irrelevant

    def id_generator(self,cls,attr,cls_relevant_features,cls_irrelevant_features,nn = "yolo",rep = "clip"):
        cls = cls.lower()
        if not cls in self.lookup:
            self.lookup[cls] = dict()

            self.lookup[cls][attr] = dict()

            
    
    def predict_stub(self,cls,counter):
        cls = cls.lower()
        
        counter += 1
        sub = f"E e{counter} ::> predict({cls})"

        self.lookup[cls]["predict_stub"] = sub
    
    def has_feature_stub(self,cls, counter):
        cls = cls.lower()

        sub = ""
        for feat_id in self.lookup[cls]["cls_features"]:
            counter += 1 
            sub = sub + f"\n\tE e{counter} ::> hasCon(${feat_id})"
        
        self.lookup[cls]["has_feature_stub"] = Template(sub)

        return counter
    
    def strength_predicate_stub(self,cls,counter,split=True):
        cls = cls.lower()
        out = self.lookup[cls]

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

        self.lookup[cls]["strength_predicate_stub"] = Template(sub)

        return counter
    
    def fill_template(self,template, values):
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

    def main_template_stub(self,id,cls):
        # cls = cls.lower()
        module_name = f"module_{id}"

        sub = f"Module {module_name} $cls_triple"
        sub = sub + " {\n\t$predict_stub \n\t$has_feature_stub\n \n\t$strength_predicate_stub\n}\n\n"
                                                
        return Template(sub)
    
    def generate(self):
        with open(self.spec_file, "w") as file:
            pass
        file.close()

        try:
            with open(self.spec_file, "a") as file:
                for id,sign in enumerate(self.traffic_signs):
                    main_template = self.main_template_stub(id,sign)
                    self.lookup[sign] = dict()
                    counter = 0

                    for key, value in self.traffic_signs.items():
                        for k,v in value.items():
                            rel, irrel = self.get_relevant_features(key,k)
                            self.id_generator(key,k,rel,irrel)
                            # print(rel, irrel)
                            # print("="*10)
                        # print(rel, irrel)
                    #     self.id_generator(sign,rel,irrel)
                    
                    # for con in concepts:
                    #     self.predict_stub(sign,counter)
                    
                    # for con in concepts:
                    #     counter = self.has_feature_stub(sign,counter)
                    
                    # for con in concepts:
                    #     counter = self.strength_predicate_stub(sign,counter)

                    # for key, value in self.lookup[sign].items():
                    #     print(key, value, "\n")

                    # for con in concepts:
                    #     counter = 0
                    #     rel, irrel = self.get_relevant_features(sign,con)

                    #     self.id_generator(sign,rel,irrel)
                    #     self.predict_stub(sign,counter)
                    #     self.has_feature_stub(sign,counter)
                    #     self.strength_predicate_stub(sign,counter)

                    for key, value in self.lookup[sign].items():
                        if isinstance(value, Template):
                            self.lookup[sign][key] = self.fill_template(value, self.lookup[sign])

                    result = self.fill_template(main_template, self.lookup[sign])
                    file.write(result)
        finally:
            file.close()

