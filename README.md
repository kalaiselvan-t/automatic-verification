# Automatic Formal Verification of AI Perception Systems

[![Paper](https://img.shields.io/badge/Paper-arXiv-b31b1b.svg)](https://arxiv.org/html/2403.19837v1)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Master's Thesis Research:**
> Automated concept-based verification of vision classifiers using CLIP and formal methods.

## Overview

This research prototype demonstrates an **automated formal verification pipeline** for vision-based neural networks in safety-critical systems. Unlike traditional simulation-based testing required by standards like ISO 26262 and ISO 21448, this tool provides **mathematical guarantees** about model behavior using concept-based specifications.

Beyond pass/fail testing, this tool provides **diagnostic insights** into WHY models fail, revealing systematic issues like concept confusion patterns and architectural biases that are invisible to conventional testing methods. Validated on both generic object classification (RIVAL-10) and safety-critical traffic sign recognition (GTSRB).

**Based on:** [Concept-based Analysis of Neural Networks via Vision-Language Models](https://arxiv.org/html/2403.19837v1)

### Key Innovation

The main contribution is **full automation** of the verification workflow from domain knowledge to verification results:

1. 🔄 **Ontology-to-Specification Generation**: Automatically converts OWL ontologies (e.g., Operational Design Domains) into formal ConSpec specifications
2. 🧠 **CLIP-Powered Concept Extraction**: Zero-shot concept representation using vision-language models (no manual labeling required)
3. 🔍 **MILP-based Verification**: Encodes specifications as Mixed Integer Linear Programming problems solved with SCIP
4. ✅ **Formal Guarantees**: Proves properties hold across focus regions or finds counterexamples

## Architecture

```
Domain Ontology (OWL/RDF)
         ↓
[Specification Generator]
         ↓
ConSpec Formal Specs
         ↓
[CLIP Embedding Extractor]
         ↓
Concept Representations
         ↓
[MILP Constraint Encoder]
         ↓
[SCIP Solver]
         ↓
Verification Result (Pass/Fail + Counterexamples)
```

### Components

- **`specification_generator/`**: Parses ontologies and generates ConSpec specifications
  - Custom DSL grammar defined in `conspec.tx`
  - Template-based specification generation
  - Automatic extraction of object-concept relationships

- **`verifier/`**: Core verification engine
  - CLIP-based concept and class embedding extraction
  - Focus region computation (statistical bounding of embedding space)
  - MILP formulation and solving via PySCIPOpt
  - Strength predicate and prediction verification

- **`automator/`**: End-to-end pipeline orchestration

## Current Capabilities

**What This Prototype Does:**
- Verifies image classification models using CLIP embeddings
- Automatically generates specifications from domain ontologies
- Checks strength predicates: `concept_A > concept_B` for a given class
- Validates prediction correctness within statistical focus regions
- **Validated on two datasets:**
  - RIVAL-10: 10 generic object classes, 18 concepts
  - GTSRB: 8 traffic sign classes (safety-critical domain)
- **Diagnostic capabilities**: Reveals WHY models fail, not just that they fail
- Quantifies violation strength (ε) for targeted improvements

**Current Limitations:**
- Works with CLIP embeddings directly (no custom model alignment yet)
- Classification only (not full object detection with bounding boxes)
- Requires training data to compute focus regions
- Scalability depends on SCIP solver performance for 512-dim problems

## Installation

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (recommended for CLIP)
- SCIP optimization suite

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/automatic-verification.git
cd automatic-verification
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install SCIP** (required for PySCIPOpt)
```bash
# Ubuntu/Debian
sudo apt-get install scip

# Or build from source: https://www.scipopt.org/
```

4. **Install CLIP**
```bash
pip install git+https://github.com/openai/CLIP.git
```

## Usage

### Quick Start

Run the complete verification pipeline:

```bash
python automator/main.py
```

This will:
1. Load the ontology from `specification_generator/AutomationOntology.rdf`
2. Generate ConSpec specifications
3. Extract CLIP embeddings for classes and concepts
4. Verify specifications and output results

### Configuration

Edit paths and parameters in configuration files:

**`specification_generator/config.py`**:
```python
grammar_file = 'specification_generator/conspec.tx'
spec_file = "specification_generator/auto_generated.cspec"
ontology_file_path = 'specification_generator/AutomationOntology.rdf'
```

**`verifier/config.py`**:
```python
GAMMA = 0.40  # Focus region multiplier (mean ± γ×std)
DIM_SIZE = 512  # CLIP embedding dimension
```

**`verifier/common.py`**:
```python
train_data_path = "/path/to/your/training/data"
verification_labels = ["cat", "car", "dog", "truck", "airplane"]
```

### Using Your Own Data

1. **Prepare training images** in the following structure:
```
train_data/
├── class1/
│   ├── img1.jpg
│   ├── img2.jpg
├── class2/
│   ├── img1.jpg
│   └── img2.jpg
```

2. **Create an ontology** (OWL/RDF format) defining:
   - Object classes (e.g., `Airplane`, `Car`)
   - Concepts (e.g., `Wings`, `Wheels`)
   - Object-concept relationships (e.g., `airplaneWings`)

3. **Update paths** in configuration files

4. **Run the pipeline**:
```bash
python automator/main.py
```

## Example: Generated Specification

From the ontology, the tool automatically generates ConSpec specifications:

```
class airplane
con wings
con wheels

Module module_airplane (yolo,airplane,clip) {
    E e1 ::> predict(airplane)
    E e2 ::> hasCon(wings)
    E e3 ::> >(airplane,wings,wheels)  # Wings should be stronger than wheels for airplanes
}
```

The verifier then checks if these properties hold across the embedding space focus region.

## Verification Process Details

### 1. Focus Region Computation
For each class, compute the statistical region in CLIP embedding space:
```
focus_region[i] = [mean[i] - γ×std[i], mean[i] + γ×std[i]]
```
where `i` indexes the 512 embedding dimensions.

### 2. Concept Representation
Concepts are extracted from CLIP's text encoder (single token) or averaged over diverse captions for classes.

### 3. MILP Formulation
For strength predicate `>(class, concept_A, concept_B)`, find if ∃ embedding `z` in focus region where:
```
cos_sim(z, concept_B) ≥ cos_sim(z, concept_A)
```

If SCIP finds a solution → **verification fails** (counterexample found)
If SCIP returns infeasible → **verification succeeds** (property holds)

## Repository Structure

```
.
├── automator/
│   ├── __init__.py
│   └── main.py              # End-to-end pipeline orchestration
├── specification_generator/
│   ├── __init__.py
│   ├── generator.py         # Ontology parser & spec generator
│   ├── config.py            # Paths configuration
│   ├── conspec.tx           # ConSpec grammar (TextX)
│   ├── AutomationOntology.rdf  # Example ontology
│   └── auto_generated.cspec # Generated specifications
├── verifier/
│   ├── __init__.py
│   ├── main.py              # Verification entry point
│   ├── optimization_functions.py  # MILP formulation & solving
│   ├── integrator_functions.py    # ConSpec interpreter
│   ├── common.py            # Shared utilities
│   └── config.py            # Verification parameters
├── tests/
│   └── zero-shot.py         # CLIP zero-shot classification tests
├── requirements.txt
├── setup.py
└── README.md
```

## Results & Validation

This tool has been validated on two complementary datasets demonstrating both accuracy and diagnostic capabilities:

### RIVAL-10 Dataset (Generic Object Classification)
- **10 object classes**: airplane, bird, car, cat, deer, dog, horse, frog, ship, truck
- **18 visual concepts**: wings, wheels, ears, metallic, hairy, etc.
- **Generated specifications**: ~30-60 strength predicates per class
- **Performance**: 88-98% verification accuracy across tested classes

**Example Verification Output:**
```
Verifying: dog
==============================
Strength Verification of concept: ears & wings
No optimal solution found. Status: infeasible
Verification Successful

Module result: True
```

### GTSRB Dataset (Traffic Sign Recognition - Safety-Critical Application)
Tested on 8 German traffic sign classes to evaluate performance in a real-world safety-critical domain:
- **Classes**: Stop, Yield, Speed Limit (30/50/80 kmph), Children Crossing, Pedestrians, Wild Animals Crossing
- **Focus regions tested**: γ = 0.20, 0.30, 0.40
- **Best performer**: Stop sign (89% accuracy, 98% precision, fully verified at γ=0.20)

### Key Discoveries & Diagnostic Insights

The GTSRB validation revealed the tool's **diagnostic power** beyond simple pass/fail verification:

1. **Content-Type Hierarchy**: Discovered that CLIP-based classifiers learn a consistent priority:
   - **Text-based signs** (Stop, Yield) → Highest accuracy & verification rates
   - **Number-based signs** (Speed limits) → Moderate performance
   - **Graphic-based signs** (Children, Pedestrians, Animals) → Lower performance

   *This pattern was unknown before verification and has implications for safety-critical deployment.*

2. **Concept Confusion Patterns**: Strength predicate verification identified systematic issues:
   - Speed limit signs confuse numbers with each other (e.g., "30" vs "50" vs "80")
   - Some signs learned shape features more strongly than semantic content
   - *Actionable insight*: Safety-critical systems should prioritize content over shape in training

3. **Quantitative Failure Analysis**: The violation measure (ε) quantifies *how badly* specifications fail:
   - Not just "this property doesn't hold"
   - But "the wrong concept is X times stronger than it should be"
   - Enables targeted model improvements

### Why GTSRB Results Matter

While accuracy varied (0-89% across classes), the **diagnostic capability proved invaluable**:
- Traditional testing would only report classification failures
- This tool reveals **WHY** failures occur (wrong concept priorities, shape vs. content confusion)
- Provides **actionable feedback** for model refinement in safety-critical contexts
- Aligns with ISO 26262 / ISO 21448 requirements for understanding failure modes

**Conclusion**: The tool successfully bridges the gap between black-box testing and interpretable formal verification, particularly valuable for safety-critical AI systems where understanding failure modes is as important as measuring accuracy.

## Future Work & Extensions

Potential improvements for production readiness:

- [ ] **Affine space alignment**: Map custom model embeddings to CLIP space (as in original paper)
- [ ] **Object detection support**: Extend to bounding box predictions and multi-object scenarios
- [ ] **Artifact generation**: Export certification reports, counterexample visualizations
- [ ] **Scalability optimizations**: Constraint simplification, incremental verification
- [ ] **ODD templates**: Pre-built ontologies for common domains (highway, urban, etc.)
- [ ] **Adversarial analysis**: Integrate with robustness verification

## Citation

If you use this work, please cite the thesis:

```bibtex
@mastersthesis{thangaraj2024automatic,
  title={Automatic Generation Of Formal Specifications Using Ontology For Verification Of CNN Based Object Detection Modules},
  author={Thangaraj, Kalaiselvan},
  year={2024},
  school={University of Trento, Technical University of Berlin},
  type={Master's Thesis},
}
```

This work is based on the concept-based analysis approach from:

```bibtex
@article{conceptbasedanalysis2024,
  title={Concept-based Analysis of Neural Networks via Vision-Language Models},
  journal={arXiv preprint arXiv:2403.19837},
  year={2024}
}
```

## Related Links

- 📄 [Original Paper (arXiv)](https://arxiv.org/html/2403.19837v1)
- 📝 [Blog Post](https://kalaiselvan-t.github.io/work/formal-ai-verification/)
- 🔗 [CLIP Repository](https://github.com/openai/CLIP)
- 🔗 [PySCIPOpt Documentation](https://github.com/scipopt/PySCIPOpt)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

This work was developed as part of a Master's thesis exploring automated formal methods for AI safety in autonomous systems. Special thanks to the authors of the concept-based analysis paper for the foundational research.