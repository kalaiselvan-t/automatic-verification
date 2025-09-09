## Automatic Formal Verification of AI Perception

Based on [Concept-based Analysis of Neural Networks via Vision-Language Model](https://arxiv.org/html/2403.19837v1)

This is an automated tool to verify the functional properties of object detection modules in safety-critical systems. Current practices, according to standards such as ISO 26262 and ISO 21448, do not involve verification of AI modules, reducing the effort to only simulation-based validation methods. Reliance on simulation-based validation is time-consuming and requires us to design simulation scenarios. On the other hand, formal verification methods provide mathematical guarantees and eliminate the need for extensive simulation-based testing. But they have not been practical due to their lack of scalability.

Identifying many of the pain points in the existing verification process, this tool has been designed to automate the formal verification process of object detection modules completely. The core of the tool is its verification engine, powered by the OpenAI CLIP model and the SCIP solver.

### Working
- The tool takes in a domain ontology modelling the deployment environment of the AI module. In the case of autonomous vehicles, it can be their Operational Design Domain (ODD)
- The ontology is parsed, and formal specifications (natural language based) for the verification process are created
- The specifications are encoded as a MILP problem and solved using the SCIP solver

At the end of the verification process, the tool generates verification artifacts and insights that can be used to improve the model or as evidence for the homologation and certification process.

More details can be found in my [blog](https://kalaiselvan-t.github.io/projects/2024-07-17-automatic-verification/)
