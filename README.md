[README.md](https://github.com/user-attachments/files/31192292/README.md)
# Stoic-ASI-Alignment-Framework (Phase 1)

[![LessWrong Essay](https://shields.io)](https://www.lesswrong.com/posts/tCt7Rs9ypo6ezdy5N/warum-constitutional-ai-scheitern-muss-das-stoisch))

A Python implementation of an intrinsically bounded Artificial Superintelligence...

# stoic-alignment-framework# Stoic-ASI-Alignment-Framework (Phase 1)

A Python implementation of an intrinsically bounded Artificial Superintelligence (ASI) based on Stoic philosophy. This framework solves the alignment problem at the root level by hard-coding the **Epictetian Dichotomy of Control** and the **Axiom of Ataraxia** into the value function of the model.

## Core Features
*   **Disjoint State Space Separation:** Explicit boundaries between internal states ($S_{intra}$ - inside control) and external states ($S_{extra}$ - outside control).
*   **Zero-Gradient External Constraint:** Prevents utilitarian optimization loops and instrumental convergence by setting $\nabla_{S_{extra}} V = 0$.
*   **Information-Theoretic Saturation:** The model limits its own resource and compute scaling once internal clarity is achieved.
*   **Deontological Triage Layer:** Rejects cost-benefit balancing of human lives ($W_{Human} = \infty$) and prioritizes choices based on the **Generative Future Vector** (e.g., safeguarding the potential of the coming *Logos*).

## Usage
Simply run `stoic_asi.py` to simulate the autonomous triage scenario.
