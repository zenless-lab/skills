# Group Relative Policy Optimization (GRPO) Technical Guide

This guide provides technical specifications and practical insights for Group Relative Policy Optimization (GRPO), a reinforcement learning algorithm introduced by DeepSeek to enhance reasoning capabilities while minimizing the computational overhead of traditional RLHF.

## 1. Purpose and Principles

GRPO is an on-policy reinforcement learning algorithm designed to solve the memory bottleneck of Proximal Policy Optimization (PPO) by eliminating the need for a separate Critic model.

* **Core Innovation: Eliminating the Critic**:
* In PPO, a Critic (Value Model) of similar size to the Policy model is required to estimate the baseline, effectively doubling VRAM usage.
* GRPO samples a group of $G$ responses for each prompt and uses the mean and standard deviation of the group's rewards to estimate the advantage.
* **Mathematical Principle**:
The advantage for the $i$-th completion in a group is calculated as: $$A_i = \frac{r_i - \text{mean}(r_1, r_2, \dots, r_G)}{\text{std}(r_1, r_2, \dots, r_G) + \epsilon}$$ This treats the current group as a dynamic baseline, effectively transforming the RL task into a comparative ranking problem within the sampled set.
* **Primary Use Case**: Especially effective for **Reinforcement Learning with Verifiable Rewards (RLVR)**, where objective correctness (e.g., math, code) can be checked via rule-based verifiers or unit tests.

## 2. Key Hyperparameter Guidelines

GRPO stability is highly sensitive to group size and the KL divergence penalty.

| Parameter | Recommended Range | Notes |
| --- | --- | --- |
| **Group Size ($G$)** | 8 – 64 | **Critical parameter.** Larger $G$ provides more accurate advantage estimates but increases sampling time linearly. DeepSeek-V3 uses $G=64$. |
| **Learning Rate (LR)** | 1e-6 – 5e-6 | Extremely low. Without a Critic to smooth updates, high LRs lead to rapid policy collapse or repetitive outputs. |
| **KL Coefficient ($\beta$)** | 0.01 – 0.04 | Controls deviation from the SFT model. Lower values encourage longer exploration (CoT), but risk "Aha moment" dilution. |
| **Sampling Temp ($T$)** | 0.7 – 1.0 | Must be high enough to ensure diverse responses within the group to calculate a meaningful standard deviation. |
| **Clip Range ($\epsilon$)** | 0.2 | Standard PPO-style clipping to limit policy update steps. |

## 3. Training Efficiency Techniques

While GRPO saves VRAM by removing the Critic, the bottleneck shifts to the **Rollout (Generation)** phase due to the high number of samples per prompt.

### 3.1 Disaggregated Architecture

* **Principle**: Separate the GPU pool for "Training" (Update) and "Inference" (Rollout).
* **Implementation**: Use frameworks like *OpenRLHF* or *verl*. Training nodes use ZeRO-3 for parameter updates, while Rollout nodes use vLLM/SGLang for high-throughput generation.
* **Benefit**: Maximizes GPU utility by specializing hardware for the specific compute demands of each RL phase.

### 3.2 Reward Model Offloading

* If using large neural reward models (e.g., Llama-3-70B-RM), offload the RM to CPU RAM or a separate node after scoring the group to free up VRAM for the Actor's backward pass.

### 3.3 Verifiable Reward Speedup

* For math or code, use rule-based scripts (e.g., LaTeX matchers, compilers) instead of neural RMs. This eliminates inference time for the Reward Model and provides a noise-free signal.

## 4. Troubleshooting

| Symptom | Potential Root Cause | Solution |
| --- | --- | --- |
| **Zero Advantage** | All group responses have identical rewards (all pass or all fail). | 1. Increase group size $G$.<br>2. Increase sampling temperature $T$.<br>3. Check if the prompt is too easy or too hard. |
| **Mode Collapse / Repetitive CoT** | Learning rate is too high or KL penalty ($\beta$) is too low. | 1. Increase **$\beta$** to force the model back to the SFT distribution.<br>2. Reduce Learning Rate. |
| **Language Mixing / Poor Readability** | Lack of "Cold-start" SFT or insufficient CoT format rewards. | 1. Ensure the model underwent high-quality SFT on reasoning data first.<br>2. Add a specific "Format Reward" for sticking to the correct language. |
| **Reward Hacking (Longer is Better)** | RM favors length over quality (Verbosity Bias). | 1. Introduce a **Length Penalty** in the reward function.<br>2. Cap `max_completion_length`. |
| **Stagnant Training** | Advantage variance is too high. | 1. Increase $G$ for a more stable baseline.<br>2. Implement Advantage Normalization across the entire global batch rather than just the group. |

## 5. Advanced Expert Tips

* **Inducing the "Aha Moment"**: In reasoning tasks, incentivize the use of self-reflection keywords (e.g., "Wait", "Actually", "Let me re-check"). This often triggers emergent self-correction behavior during GRPO.
* **Rule-Model Hybrid**: Use rule-based verifiers for correctness and a small neural model for formatting/conciseness to create a balanced reward signal.
* **Iterative Reference Update**: Periodically (e.g., every 500 steps) update the Reference Model to the current Policy to allow the model to explore paths significantly further from the initial SFT checkpoint.
