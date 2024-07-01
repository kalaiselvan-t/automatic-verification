from verifier.common import *
from verifier.optimization_functions import *

class Verification:

    def __init__(self, grammar_file, specification_file,verification_list = verification_labels) -> None:
        print("Starting verification process...")
        print("Gamma set to: ",GAMMA)
        self.grammar_file = grammar_file
        self.specification_file = specification_file
        self.verification_list = verification_list

        self.metamodel = metamodel_from_file(self.grammar_file)
        self.model = self.metamodel.model_from_file(self.specification_file)

        verification_setup()

        # print(image_focus_regions.keys())
        # print(class_embeddings.keys())
        # print(concept_embeddings.keys())

        self.result = self.interpret(self.model)

        print("Verification process completed, overall result: ",self.result)
    
    def interpret(self,model):
        self.elements = model.elements
        module_result = {}

        for element in model.elements:
            if element.__class__.__name__ == "Class":
                class_list.append(element.name)
            if element.__class__.__name__ == "Image":
                image_list.append(element.name)
            if element.__class__.__name__ == "Network":
                network_list.append(element.name)
            if element.__class__.__name__ == "ConRep":
                rep_list.append(element.name)
            if element.__class__.__name__ == "Module":
                print(self.verification_list, element.triple.inp.name)
                if element.triple.inp.name.replace("_"," ") in self.verification_list:
                    print(f"\nVerifying: {element.triple.inp.name}")
                    print("="*30)
                    mod = Module(element)
                    result = mod.result
                    print("Module result: ",result)
                    module_result[element.triple.inp.name] = result
                # else:
                #     print(f"\nSkipping: {element.triple.inp.name}")
                #     print("="*30)
                #     module_result[element.triple.inp.name] = True

        if all(module_result.values()):
            print(module_result)
            return True
        else:
            print("Verification of some classes failed. Please check the results.")
            print(module_result)
            print("="*50)
            return False

#=======================================================================================================
#===========================================Supporting classes++========================================
class Module:
    def __init__(self,module):
        self.module = module
        if DEBUG:
            print(f"Collecting specifications from {module.name}")
        self.specification_list = []
        for spec in self.module.specifications:
            self.specification_list.append(spec)
        self.result = self.execute()
    
    def execute(self):
        for s in self.specification_list:
            specifications_result = []
            specifications_result.append(Specification(s).result)
            if DEBUG:
                print(f"Execution result: {all(specifications_result)}\n")

        if all(specifications_result):
            return True
        else:
            return False

class Specification:
    def __init__(self,specification):
        self.specification = specification
        self.result = self.verify(self.specification)
        if DEBUG:
            print("Specification result: ",self.result)

    def verify(self,specification):
        print("="*30)
        print(f"\nVerifying spec {self.specification.name}\n")
        self.LHS_ONLY = True

        if self.specification.expression_rhs:
            self.LHS_ONLY = False

        if self.LHS_ONLY:
            result = self.OR_Eval(specification.expression_lhs)
        
        if DEBUG:
            print("Verification result: ",result)
        return result
    
    def OR_Eval(self,expression):
        OR_LHS_ONLY = True
        
        if expression[0].right:
                AND_LHS_ONLY= False
        
        if OR_LHS_ONLY:
            result = self.AND_eval(expression[0].left)

        if DEBUG:
            print("OR result: ",result)
        
        return result

    
    def AND_eval(self,expression):
        AND_LHS_ONLY = True
        
        if expression.right:
                AND_LHS_ONLY= False
        
        if AND_LHS_ONLY:
            result = self.primary_eval(expression.left)
        
        if DEBUG:
            print("AND result: ",result)
        
        return result
    
    def primary_eval(self,expression):

        if expression.not_exp:
            pass
        else:
            if expression.exp.__class__.__name__ == "Predict":
                cls = expression.exp.cls.name
                result = predict_predicate(cls)
                if DEBUG:
                    print("Primary result: ",result)
                return result
            elif expression.exp.__class__.__name__ == "StrengthPredicate":
                cls = expression.exp.cls.name
                con1 = expression.exp.concept_prior.name
                con2 = expression.exp.concept_after.name
                result = strength_predicate(cls,[con1,con2])
                if DEBUG:
                    print("Primary result: ",result)
                return result
            
#=======================================================================================================
        
    
        