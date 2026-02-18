# Proximal Policy Optimization (PPO) Technical Guide

This guide provides technical specifications and operational insights for implementing Proximal Policy Optimization (PPO) in the context of Reinforcement Learning from Human Feedback (RLHF). PPO remains the industry standard for complex alignment tasks requiring high exploration and fine-grained reward signals.

## 1. Purpose and Principles

PPO aligns a model by maximizing expected rewards from a Reward Model (RM) while ensuring the updated policy does not deviate too far from the initial SFT distribution.

* **Core Advantages**:
* **Exploration**: As an on-policy algorithm, PPO explores the solution space beyond the fixed SFT data, which is critical for reasoning and coding tasks.
* **Stability**: The clipped surrogate objective prevents large, destructive updates that characterize vanilla policy gradient methods.

* **The 4-Model System**:
Standard PPO RLHF requires maintaining four distinct models in memory:

1. **Actor (Policy)**: The model being trained ().
2. **Critic (Value)**: Estimates the expected return () to calculate advantages.
3. **Reference (SFT)**: Frozen copy used to calculate KL-divergence penalties.
4. **Reward Model**: Frozen model that provides scalar scores for completions.

## 2. Key Hyperparameter Guidelines

PPO is highly sensitive to hyperparameter interaction. Below are recommended ranges for stable convergence:

| Parameter | Recommended Range | Notes |
| --- | --- | --- |
| **Learning Rate (Actor)** | 5e-7 to 2e-6 | Extremely low to prevent policy collapse. DeepSeek and Llama 3 often use **1e-6**. |
| **Learning Rate (Critic)** | 5e-6 to 1e-5 | Typically 5-10x higher than the Actor to ensure value estimation converges faster. |
| **KL Coefficient ($\beta$)** | 0.02 to 0.1 | Controls the penalty for deviating from the SFT model. Use Adaptive KL controllers to maintain a target divergence. |
| **Clip Range ($\epsilon$)** | 0.1 to 0.2 | Limits the probability ratio update. **0.2** is the standard for LLMs. |
| **GAE Lambda ($\lambda$)** | 0.95 | Decay factor for Generalized Advantage Estimation; balances bias and variance. |
| **Rollout Batch Size** | 128 to 1024 | Total samples generated before an update. Larger batches reduce gradient variance. |

## 3. Training Efficiency and Architecture

The primary bottleneck in PPO is the memory overhead of the 4-model architecture and the speed of the generation (rollout) phase.

### 3.1 Disaggregated / Hybrid Engines

* **Rollout vs. Update**: Decouple the generation phase (requires high throughput/inference optimization) from the update phase (requires high memory for gradients/optimizer states).
* **vLLM Integration**: Use inference engines like vLLM for the Rollout phase to significantly reduce training wall-clock time.

### 3.2 Memory Optimization

* **Model Offloading**: Since the Reference and Reward models are frozen, they can be offloaded to CPU or NVMe during the Actor/Critic backward pass.
* **Parameter Sharing**: The Actor and Critic can share the same Transformer backbone (Shared-Weights PPO), adding only a small MLP head for the Critic. This saves ~40% VRAM but requires careful tuning of the combined loss.
* **PEFT (LoRA)**: Train only LoRA adapters for the Actor and Critic while keeping the base weights shared across all four models.

## 4. Troubleshooting

| Symptom | Potential Root Cause | Solution |
| --- | --- | --- |
| **Reward Hacking** | Reward Model (RM) is "fooled" by length or repetitive patterns. | 1. Increase KL penalty ().<br>2. Add rule-based reward shaping (e.g., penalty for length/loops). |
| **KL Divergence Explosion** | Model deviates too fast; LR is too high. | 1. Lower Actor LR.<br>2. Increase KL penalty.<br>3. Ensure Actor/Ref start with identical weights. |
| **Value Loss is Flat** | Critic is not learning or is poorly initialized. | 1. Increase Critic LR.<br>2. Pre-train the Critic on the RM dataset before starting RL. |
| **OOM (Out of Memory)** | 4 models exceed GPU memory. | 1. Use Gradient Checkpointing.<br>2. Enable ZeRO-3 or FSDP.<br>3. Reduce `max_prompt_length`. |
| **Unstable Training/Spikes** | Advantage estimates have high variance. | 1. Use Advantage Normalization (mean=0, std=1) within each batch.<br>2. Increase batch size. |

## 5. Advanced Techniques

* **PPO-ptx**: Mix pre-training gradients into the RL update. This prevents the "alignment tax" where the model loses general knowledge while learning to follow instructions.
* **Whiten Advantages**: Normalizing advantages across the entire rollout batch (rather than just mini-batches) is crucial for stable policy updates.
* **Advantage Masking**: Ensure that padding tokens are strictly masked during both reward computation and advantage estimation to avoid noise in the gradient.
