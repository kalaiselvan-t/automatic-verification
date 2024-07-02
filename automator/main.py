from specification_generator.generator import generate_specifications
from specification_generator.config import *
from verifier.integrator_functions import Verification


if __name__ == "__main__":
    generate_specifications()
    result = Verification(grammar_file,spec_file,["dog"]).result
    print(result)
