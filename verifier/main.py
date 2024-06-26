from verifier.common import *
from verifier.optimization_functions import *
from verifier.integrator_common import *
from verifier.integrator_functions import *  

if __name__ == "__main__":
    grammar_file = "/home/kalai/Development/Conspec_automation/specification_generator/conspec.tx"
    specification_file = "/home/kalai/Development/Conspec_automation/specification_generator/auto_generated.cspec"

    result = Verification(grammar_file,specification_file,["cat"]).result