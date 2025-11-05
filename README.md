# Automatic Formal Verification for Traffic Sign Recognition (GTSRB)

[![Paper](https://img.shields.io/badge/Paper-arXiv-b31b1b.svg)](https://arxiv.org/html/2403.19837v1)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Dataset](https://img.shields.io/badge/Dataset-GTSRB-green.svg)](https://benchmark.ini.rub.de/gtsrb_news.html)

> **Master's Thesis Research - Safety-Critical Application:**
> Automated concept-based verification of traffic sign classifiers for autonomous driving systems.
> This branch demonstrates the verification framework applied to the **German Traffic Sign Recognition Benchmark (GTSRB)**.

## Overview

This branch extends the automated formal verification framework to **safety-critical traffic sign recognition**, targeting real-world autonomous driving applications. Unlike the generic object classification in the main branch (RIVAL-10), this implementation focuses on **ISO 26262/21448-compliant verification** for traffic sign detection modules.

The tool provides **mathematical guarantees** and **diagnostic insights** about CLIP-based traffic sign classifiers, revealing systematic failure patterns like:
- Content-type hierarchy (text-based > number-based > graphic-based signs)
- Shape vs. semantic content confusion
- Cross-class concept interference (e.g., number confusion in speed limits)

**Based on:** [Concept-based Analysis of Neural Networks via Vision-Language Models](https://arxiv.org/html/2403.19837v1)

### Key Features for Traffic Signs

1. 🚦 **Domain-Specific Ontology**: Traffic sign structure (shape + content decomposition)
2. 🎯 **Context-Aware Embeddings**: CLIP concepts grounded with "traffic sign" context
3. 📊 **GTSRB Validation**: Tested on real-world German traffic sign dataset
4. 🔍 **Diagnostic Analysis**: Reveals WHY models fail on specific sign types
5. ✅ **Safety-Critical Focus**: Aligned with automotive safety standards

## What's Different from Main Branch?

| Aspect | Main Branch | Traffic Sign Branch |
|--------|-------------|---------------------|
| **Domain** | Generic objects (RIVAL-10) | Traffic signs (GTSRB) |
| **Classes** | airplane, car, cat, dog, etc. | Stop, speed limits, pedestrian warnings, etc. |
| **Concepts** | Generic visual (wings, wheels, ears) | Traffic sign specific (octagon shape, "STOP" text, numbers) |
| **Ontology** | AutomationOntology.rdf | TrafficSignOntology.rdf |
| **Context** | None | "a road traffic sign with..." prefix for concepts |
| **Application** | Research prototype | Safety-critical automotive validation |
| **Test Data** | Not included | 8 test images from GTSRB included |

**→ For generic object verification, see the [main branch](../../tree/main)**

## Architecture

```
Traffic Sign Ontology (OWL/RDF)
         ↓
[Specification Generator]
    (Shape + Content decomposition)
         ↓
ConSpec Traffic Sign Specs
         ↓
[CLIP Embedding Extractor]
    (with "traffic sign" context)
         ↓
Domain-Specific Concept Representations
         ↓
[MILP Constraint Encoder]
         ↓
[SCIP Solver]
         ↓
Verification Result + Diagnostic Analysis
```

## Dataset: GTSRB (German Traffic Sign Recognition Benchmark)

- **Purpose**: Real-world traffic sign recognition for autonomous vehicles
- **Training Images**: 51,839 images across 43 classes
- **Image Format**: PPM (Portable Pixmap)
- **Classes Tested**: 7-8 safety-critical signs
- **Validation Context**: Automotive safety standards (ISO 26262, ISO 21448)

### Traffic Sign Classes Verified

```python
verification_labels = [
    "stop and give way traffic sign",
    "speed limit 30kmph traffic sign",
    "speed limit 60kmph traffic sign",
    "children crossing ahead traffic sign",
    "end of speed limit 80kmph traffic sign",
    "pedestrians in road ahead traffic sign",
    "wild animals traffic sign"
]
```

### Traffic Sign Concepts (16 Total)

**Shape Concepts:**
- circle shape, octagon shape, square shape, triangle shape, inverted triangle shape

**Content Concepts:**
- word STOP in white letters
- number 30 in black, number 60 in black, number 80 in black
- diagonal black stripes
- two black figures of children
- black figure of a pedestrian walking
- black symbol of a deer leaping
- black symbol of a person digging
- white arrow pointing to the left/right

## Installation

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (recommended for CLIP)
- SCIP optimization suite
- GTSRB dataset (download from [official source](https://benchmark.ini.rub.de/gtsrb_news.html))

### Setup

1. **Clone the repository and switch to traffic_sign branch**
```bash
git clone https://github.com/yourusername/automatic-verification.git
cd automatic-verification
git checkout traffic_sign
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

5. **Download GTSRB Dataset**
```bash
# Download from: https://benchmark.ini.rub.de/gtsrb_news.html
# Extract training images to a local directory
# Update path in verifier/common.py
```

## Configuration

### Update Dataset Path

**`verifier/common.py`**:
```python
# Update to your GTSRB training images path
train_data_path = "/path/to/GTSRB_Final_Training_Images/GTSRB/Final_Training/Images"

# Classes to verify
verification_labels = [
    "stop and give way traffic sign",
    "speed limit 30kmph traffic sign",
    # ... etc
]

# Traffic sign concepts
concepts = [
    "circle shape", "octagon shape", "triangle shape",
    "word STOP in white letters", "number 30 in black",
    # ... etc
]
```

### Verification Parameters

**`verifier/config.py`**:
```python
GAMMA = 0.40  # Focus region multiplier (mean ± γ×std)
                # Tested values: 0.20, 0.30, 0.40
DIM_SIZE = 512  # CLIP ViT-B/32 embedding dimension
```

### Ontology Configuration

**`specification_generator/config.py`**:
```python
ontology_file_path = 'specification_generator/TrafficSignOntology.rdf'
spec_file = "specification_generator/auto_generated.cspec"
```

## Usage

### Quick Start: Run Verification

```bash
python automator/main.py
```

This will:
1. Load TrafficSignOntology.rdf
2. Generate ConSpec specifications for traffic signs
3. Extract CLIP embeddings with traffic sign context
4. Verify specifications and output diagnostic results

### Zero-Shot Classification Testing

Test CLIP's zero-shot performance on GTSRB:

```bash
python tests/zero-shot.py
```

This tests CLIP against **43 traffic sign classes** including:
- Speed limits (20, 30, 50, 60, 70, 80, 100, 120 km/h)
- Prohibitory signs (no passing, no entry, etc.)
- Warning signs (dangerous curves, road work, pedestrians, children, animals)
- Mandatory signs (ahead only, keep right/left, roundabout)

### Test Dataset

Sample test images included in `dataset/test/`:
- pedestrian.ppm
- road work (3 variants)
- speed limits (20, 50, 100 km/h)
- stop.ppm

## Key Technical Innovations for Traffic Signs

### 1. Context-Aware Concept Embeddings

**Problem**: CLIP's concept representations can be ambiguous (e.g., "circle" could mean many things).

**Solution**: Prefix all concepts with domain context:

```python
# Standard approach (main branch):
con = "circle shape"

# Traffic sign approach (this branch):
con = f"a road traffic sign with circle shape"
```

**Impact**: Improved concept grounding and reduced false positives.

### 2. Domain-Specific Caption Templates

All 72 caption templates include "traffic sign":

```python
captions_template = [
    f"a bad photo of a {cls} traffic sign",
    f"the cartoon {cls} traffic sign",
    f"art of a {cls} traffic sign",
    f"a photo of a small {cls} traffic sign",
    # ... 68 more variations
]
```

**Impact**: Better CLIP text embeddings for traffic sign classification.

### 3. Traffic Sign Ontology Structure

**`TrafficSignOntology.rdf`** models traffic signs with properties:
- `hasShape`: Geometric shape (circle, octagon, triangle, etc.)
- `hasContent`: Semantic content (text, numbers, graphics)
- `hasBorder`, `hasBackgroundColor`, `hasBorderColor`

**Design Rationale**: Matches real-world traffic sign design principles and enables shape vs. content analysis.

## Example: Generated Specification

From TrafficSignOntology.rdf, the tool generates specifications like:

```
class stop_and_give_way_traffic_sign
con octagon_shape
con word_STOP_in_white_letters

Module module_stop (yolo, stop_and_give_way_traffic_sign, clip) {
    E e1 ::> predict(stop_and_give_way_traffic_sign)
    E e2 ::> hasCon(octagon_shape)
    E e3 ::> hasCon(word_STOP_in_white_letters)

    # Strength predicates: relevant concepts > irrelevant concepts
    E e4 ::> >(stop_and_give_way_traffic_sign, octagon_shape, circle_shape)
    E e5 ::> >(stop_and_give_way_traffic_sign, octagon_shape, triangle_shape)
    E e6 ::> >(stop_and_give_way_traffic_sign, word_STOP_in_white_letters, number_30_in_black)
    # ... more predicates
}
```

## Results & Validation

### GTSRB Experimental Results

**Classes Tested**: 7-8 traffic sign types
**Focus Regions**: γ = 0.20, 0.30, 0.40
**Baseline**: CLIP ViT-B/32 zero-shot classification

### Performance Highlights

**Best Performer: Stop Sign**
- Classification Accuracy: 89%
- Precision: 98%
- Verification Status: **Fully verified** at γ=0.20
- Analysis: Clear octagon shape + distinct "STOP" text → strong CLIP representations

**Moderate Performance: Speed Limit Signs**
- Classification Accuracy: 40-60%
- Key Issue: **Number confusion** (30 vs 50 vs 60 vs 80)
- Diagnostic: Shape concepts (circle) verified correctly, but number concepts confused
- Actionable: Fine-tune on digit discrimination for speed limit subnetwork

**Lower Performance: Graphic-Based Signs**
- Examples: Children crossing, pedestrians, wild animals
- Classification Accuracy: 20-50%
- Key Issue: **Graphic concept ambiguity** in CLIP embeddings
- Diagnostic: Triangle shape verified, but graphic content (children, deer, pedestrian) weak

### Key Discoveries

#### 1. Content-Type Hierarchy

The tool revealed a previously unknown pattern in CLIP's traffic sign understanding:

| Content Type | Verification Rate | Explanation |
|--------------|-------------------|-------------|
| **Text-based** (STOP) | 85-89% | Strong text recognition in CLIP |
| **Number-based** (Speed limits) | 40-60% | Moderate, but inter-number confusion |
| **Graphic-based** (Pedestrians, animals) | 20-50% | Weak semantic understanding of pictograms |

**Implication for Deployment**: Text-based signs can be verified reliably; graphic-based signs need additional training or human oversight.

#### 2. Shape vs. Content Analysis

**Finding**: For most signs, **shape concepts verify successfully** (circle, triangle, octagon), but **content concepts fail** (numbers, graphics).

**Example**: Speed limit 30 km/h sign
- Verified: Circle shape > Triangle shape
- Failed: Number 30 > Number 50 (confused)

**Safety Impact**: Shape-based classification alone is insufficient for safety-critical decisions. Content verification is essential.

#### 3. Quantitative Failure Diagnosis

The violation strength measure (ε) quantifies failure severity:

```
Speed Limit 30 km/h verification:
- Optimal solution found: ε = 0.15
- Interpretation: Within focus region, "number 50" is 0.15 stronger than "number 30"
```

**Actionable**: Prioritize retraining on high-ε failures for maximum improvement.

## Example Verification Output

```
Starting verification process...
Gamma set to: 0.40

Verifying: stop and give way traffic sign
==============================

==============================
Strength Verification of concept: octagon shape & circle shape

No optimal solution found. Status: infeasible
Verification Successful

==============================
Strength Verification of concept: word STOP in white letters & number 30 in black

No optimal solution found. Status: infeasible
Verification Successful

Module result: True
```

## Safety-Critical Considerations

### ISO 26262 / ISO 21448 Alignment

This tool addresses requirements for:
- **Formal verification** of perception functions (ISO 26262-6)
- **ODD specification** using ontologies (ISO 21448 SOTIF)
- **Failure mode analysis** through diagnostic capabilities
- **Validation evidence** for safety certification

### Limitations for Production Use

**Current Limitations:**
- Verifies CLIP directly (not production traffic sign detectors)
- Classification only (no bounding box verification)
- Requires focus region computation from training data
- Scalability challenges with 512-dim MILP problems

**Recommended Use Cases:**
- Early-stage safety analysis of perception architectures
- Comparative evaluation of model designs
- Failure mode discovery during development
- Training data quality assessment

## Verification Process Details

### 1. Focus Region Computation

For each traffic sign class, compute statistical embedding region:

```python
focus_region[i] = [mean[i] - γ×std[i], mean[i] + γ×std[i]]
```

where:
- `i` indexes 512 CLIP embedding dimensions
- `γ` controls region tightness (0.20, 0.30, or 0.40 tested)

### 2. Context-Aware Concept Extraction

```python
# Concept with traffic sign context
concept_text = f"a road traffic sign with {concept_name}"
text_token = clip.tokenize([concept_text]).cuda()
concept_embedding = model.encode_text(text_token)
```

### 3. MILP Formulation

For strength predicate `>(sign_class, relevant_concept, irrelevant_concept)`:

**Find**: embedding `z` in focus region where:
```
cos_sim(z, irrelevant_concept) ≥ cos_sim(z, relevant_concept)
```

**Maximize**: violation strength `ε`

**Results**:
- Optimal solution found → Verification **fails** (counterexample exists, ε > 0)
- Infeasible → Verification **succeeds** (property holds everywhere)

## Repository Structure

```
. (traffic_sign branch)
├── automator/
│   └── main.py                          # Pipeline orchestration
├── specification_generator/
│   ├── generator.py                     # Ontology → ConSpec generator
│   ├── common.py                        # Alternative manual spec generator
│   ├── config.py                        # Paths configuration
│   ├── conspec.tx                       # ConSpec grammar
│   ├── TrafficSignOntology.rdf          # Traffic sign domain ontology (688 lines)
│   └── auto_generated.cspec             # Generated specifications
├── verifier/
│   ├── main.py                          # Verification entry point
│   ├── optimization_functions.py        # MILP formulation (context-aware)
│   ├── integrator_functions.py          # ConSpec interpreter
│   ├── common.py                        # GTSRB-specific configuration
│   └── config.py                        # GAMMA, DIM_SIZE parameters
├── tests/
│   ├── zero-shot.py                     # 43-class CLIP evaluation
│   └── config.py                        # Test dataset paths
├── dataset/test/                        # Sample GTSRB test images
│   ├── stop.ppm
│   ├── pedestrian.ppm
│   ├── sl_20.ppm, sl_50.ppm, sl_100.ppm
│   └── road work (3 variants)
├── requirements.txt
├── setup.py
└── README.md                            # This file
```

## Comparison with Main Branch

### Switch Between Branches

```bash
# Generic object verification (RIVAL-10)
git checkout main

# Traffic sign verification (GTSRB)
git checkout traffic_sign
```

### When to Use Each Branch

**Main Branch (`main`)**:
- Learning how the tool works
- Generic object classification
- Exploring ontology-to-specification automation
- RIVAL-10 dataset experiments

**Traffic Sign Branch (`traffic_sign`)**:
- Safety-critical automotive applications
- Traffic sign recognition analysis
- GTSRB dataset experiments
- ISO 26262 / ISO 21448 case studies
- Domain-specific concept analysis

## Future Work & Extensions

Potential improvements for production-ready traffic sign verification:

- [ ] **Custom model alignment**: Affine space mapping from YOLOv5/8 to CLIP space
- [ ] **Bounding box verification**: Extend to full object detection outputs
- [ ] **Multi-sign scenarios**: Handle images with multiple traffic signs
- [ ] **Adversarial robustness**: Verify under occlusion, weather, lighting variations
- [ ] **ODD template library**: Pre-built ontologies for highway, urban, rural scenarios
- [ ] **Certification reports**: Generate ISO 26262-compliant verification artifacts
- [ ] **Real-time verification**: Optimize MILP solving for online use
- [ ] **Expanded GTSRB coverage**: Verify all 43 classes systematically

## Citation

If you use this work, please cite the thesis:

```bibtex
@mastersthesis{thangaraj2024automatic,
  title={Automatic Generation Of Formal Specifications Using Ontology For Verification Of CNN Based Object Detection Modules},
  author={Thangaraj, Kalaiselvan},
  year={2024},
  school={University of Trento, Technical University of Berlin},
  type={Master's Thesis},
  note={Traffic sign verification branch: GTSRB application}
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
- 🚦 [GTSRB Dataset](https://benchmark.ini.rub.de/gtsrb_news.html)
- 🔗 [CLIP Repository](https://github.com/openai/CLIP)
- 🔗 [PySCIPOpt Documentation](https://github.com/scipopt/PySCIPOpt)
- 📋 [ISO 26262 Overview](https://www.iso.org/standard/68383.html)
- 📋 [ISO 21448 (SOTIF)](https://www.iso.org/standard/77490.html)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

This traffic sign verification branch was developed as part of a Master's thesis exploring automated formal methods for AI safety in autonomous driving systems. Special thanks to:
- The GTSRB dataset creators at INI, Ruhr University Bochum
- The authors of the concept-based analysis paper for foundational research
- The CLIP and PySCIPOpt communities for excellent tools
