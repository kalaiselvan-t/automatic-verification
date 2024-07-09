from verifier.common import *
from verifier.optimization_functions import *
from verifier.integrator_functions import *  
from specification_generator.config import *

if __name__ == "__main__":
    grammar_file = "/home/kalai/Development/Conspec_automation/specification_generator/conspec.tx"
    specification_file = "/home/kalai/Development/Conspec_automation/specification_generator/auto_generated.cspec"

    result = Verification(grammar_file,test_file,["airplane"]).result