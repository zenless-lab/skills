# Advanced Model Tuning & Alignment Strategies

This document serves as a comprehensive reference for Agent Skills regarding post-training methodologies. It details the spectrum of techniques from foundational Supervised Fine-Tuning (SFT) to cutting-edge Reinforcement Learning (RL) and Preference Optimization paradigms used to align Large Language Models (LLMs) with human intent, safety standards, and complex reasoning capabilities.

## 1. The Post-Training Landscape

Post-training has evolved from a simple "fine-tuning" step into a multi-stage pipeline designed to specialize pre-trained models. The modern hierarchy includes:

1. **Behavioral Cloning (SFT)**: Establishing the format and basic instruction-following capabilities.
2. **Preference Alignment (DPO/PPO/KTO)**: Aligning the model's output distribution with human values (Helpful, Honest, Harmless).
3. **Reasoning Reinforcement (GRPO/RLVR)**: Incentivizing deep reasoning chains (Chain-of-Thought) through exploration and verifiable feedback.

---

## 2. Supervised Fine-Tuning (SFT) & Data Strategies

SFT remains the critical initialization step. Recent research emphasizes data selection over data volume.

* **Standard SFT**: Training on "gold" `(prompt, response)` pairs.
  * *Key Insight*: SFT primarily teaches "style" and "format" (Superficial Alignment Hypothesis).
* **Rejection Sampling / Expert Iteration**: A bridge between SFT and RL. The model generates $N$ responses; the best ones (scored by a Reward Model or Verifier) are filtered and added back to the SFT dataset.
  * *Usage*: Crucial for "Cold Start" in reasoning models (e.g., DeepSeek-R1 recipe) to seed the model with high-quality reasoning traces before RL.
* **Data Selection**: Techniques like "Instruction Mining" or probability-based selection (e.g., selecting responses that fit the model's pre-trained distribution) prevent degradation often caused by training on out-of-distribution data.

---

## 3. Preference Optimization Techniques

These methods align the model using preference data (e.g., "Response A is better than Response B").

### Offline Methods (Stable & Efficient)

* **DPO (Direct Preference Optimization)**:
  * *Mechanism*: Optimizes the policy directly to satisfy preferences without an explicit reward model trained in memory. Uses the reference model itself as an implicit reward estimator.
  * *Pros*: High stability, lower memory footprint than PPO.
  * *Cons*: Limited exploration; prone to overfitting on static datasets.
* **ORPO (Odds Ratio Preference Optimization)**:
  * *Mechanism*: Integrates alignment directly into the SFT process by adding an odds-ratio penalty to the loss.
  * *Pros*: Single-stage training (No reference model required in memory).
* **SimPO (Simple Preference Optimization)**:
  * *Mechanism*: A variant of DPO that removes the reference model entirely and uses a margin-based objective derived from self-consistency.
  * *Pros*: Extremely lightweight; "Reference-free".
* **KTO (Kahneman-Tversky Optimization)**:
  * *Mechanism*: Uses unpaired binary feedback (thumbs up/down) rather than comparison pairs.
  * *Pros*: Easier data collection (real-world user logs are often unpaired).

### Online / Hybrid Methods (High Performance)

* **PPO (Proximal Policy Optimization)**:
  * *Mechanism*: The classic Actor-Critic RL method. Generates new samples (rollouts) during training and updates based on a separate Reward Model.
  * *Pros*: Enables true exploration; effectively handles granular, token-level rewards.
  * *Cons*: High "Alignment Tax" (potential regression in other capabilities); computationally expensive (4 models in memory).
* **Iterative DPO / Online DPO**:
  * *Mechanism*: Periodically generates new responses using the current policy, labels them with an external Reward Model, and updates the policy using DPO.
  * *Pros*: Bridges the gap between offline stability and online exploration.

---

## 4. Reasoning & Verifiable RL (The "System 2" Shift)

For complex tasks (Math, Coding, Logic), simple preference alignment is insufficient. Models need to learn *how* to think, not just mimic answers.

* **GRPO (Group Relative Policy Optimization)**:
  * *Mechanism*: Samples a group of outputs for a single prompt. Optimizes based on the relative performance within that group. Eliminates the need for a value function (Critic model).
  * *Key Feature*: Particularly effective with **Verifiable Rewards** (e.g., passing unit tests, correct math answers) combined with **Format Rewards** (enforcing `<thinking>` tags).
* **Cold Start Data**:
  * *Concept*: Before RL, the model must be SFT-tuned on a small, high-quality set of reasoning examples (long Chain-of-Thought) to ensure stable RL convergence. Without this, the model may collapse into gibberish or bypass reasoning.
* **The "Aha" Moment**:
  * *Phenomenon*: Under pure RL with verifiable rewards, models can spontaneously develop self-correction and reflection behaviors (e.g., "Wait, I made a mistake here...").

---

## 5. Text-Based Decision Tree

Use the following logic flow to determine the optimal tuning strategy for a given requirement.

**START: Define the Primary Capability Target**

1. **SCENARIO A: The model needs to learn new domain knowledge or strict formats.**
    * *Condition*: Do you have high-quality instruction-response pairs?
        * **YES**: Use **SFT (Supervised Fine-Tuning)**.
        * **NO**: Use **Synthetic Data Generation** (via a stronger model) -> Filter -> **SFT**.

2. **SCENARIO B: The model knows facts but is toxic, verbose, or stylistically wrong.**
    * *Condition*: Do you have pairwise preference data (A > B)?
        * **YES**:
            * *Sub-condition*: Is VRAM/Compute severely limited?
                * **YES**: Use **ORPO** or **SimPO** (Reference-free).
                * **NO**: Use **DPO** (Standard Choice).
        * **NO** (Only have Thumbs Up/Down data):
            * Use **KTO**.

3. **SCENARIO C: The model struggles with complex Math, Coding, or Logic problems.**
    * *Condition*: Can you automatically verify the correctness of the answer (e.g., compiler, ground truth value)?
        * **YES (Verifiable Environment)**:
            * *Step 1*: **Cold Start SFT** (Train on long-CoT examples).
            * *Step 2*: **GRPO** (Sample groups, reward correct answers + reasoning format).
        * **NO (Open-Ended Reasoning)**:
            * *Step 1*: **SFT** on diverse reasoning traces.
            * *Step 2*: **Iterative DPO** or **PPO** (Requires a robust, learned Reward Model).

4. **SCENARIO D: You want to maximize performance regardless of cost.**
    * *Strategy*: **PPO** or **Iterative DPO**.
    * *Reasoning*: Online generation allows the model to explore boundaries and fix specific weaknesses that offline data (static DPO) misses.

**END: Evaluation**

* Always validate using a "Judge" model or specific benchmarks (e.g., GSM8K for math, IFEval for formatting) to check for "Alignment Tax" (regression in pre-training capabilities).
