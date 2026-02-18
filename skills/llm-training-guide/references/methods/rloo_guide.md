# RLOO (REINFORCE Leave-One-Out) Reference

**Purpose:** A memory-efficient Reinforcement Learning (RL) algorithm for LLM alignment that eliminates the need for a separate critic (value) model while maintaining training stability through variance reduction.

## 1. Core Concept

RLOO is a variant of the REINFORCE algorithm designed to align LLMs using prompt-specific baselines. Unlike PPO, which uses a learned value network to estimate the expected reward (baseline), RLOO estimates the baseline using the average reward of *other* samples generated from the *same* prompt.

### The Objective

For a prompt $x$, generate $K$ responses $\{y_1, ..., y_K\}$. The advantage $A(x, y_i)$ for response $y_i$ is calculated as:

$$A(x, y_i) = R(x, y_i) - \frac{1}{K-1} \sum_{j \neq i} R(x, y_j)$$

* **Unbiased Baseline:** By excluding the sample itself ($j \neq i$) from the average, RLOO provides an unbiased estimator of the advantage.
* **Critic-Free:** Reduces VRAM usage by ~30-50% compared to PPO (no value model parameters or optimizer states).

## 2. Key Hyperparameters

| Parameter | Recommended Range | Description |
| :--- | :--- | :--- |
| `num_generations` ($K$) | **4 - 8** (Minimum) | The number of completion samples per prompt. Higher $K$ significantly reduces gradient variance but increases compute cost per step. For complex reasoning, $K=8$ or $16$ is preferred. |
| `learning_rate` | **5e-7 - 2e-6** | Generally lower than SFT rates. Start low (e.g., 1e-6) to prevent policy collapse. |
| `kl_coeff` ($\beta$) | **0.01 - 0.1** | Controls the strength of the KL penalty to prevent drifting too far from the reference model. RLOO often integrates this directly into the reward: $R_{total} = R_{score} - \beta \cdot KL$. |
| `train_batch_size` | **128 - 512** | Larger global batch sizes (across devices) help average out the high variance inherent in policy gradient methods. |
| `max_grad_norm` | **0.5 - 1.0** | Essential for clipping gradients to prevent spikes, especially in the absence of a value function. |

## 3. Implementation Variants & Tricks

Modern implementations (often termed **REINFORCE++**) combine RLOO with PPO-style optimizations to enhance stability:

* **PPO-Style Clipping:** Even without a critic, applying the $\epsilon$-clipping (e.g., $\epsilon=0.1$ or $0.2$) to the policy ratio $\pi_\theta / \pi_{ref}$ prevents destructively large updates.
* **Token-Level KL:** Applying the KL penalty at every token step (rather than just the end) improves dense supervision.
* **Reward Normalization:** Normalizing rewards within a batch (or moving average) is crucial for convergence, especially when reward model scores are uncalibrated.

## 4. Efficiency & Scaling

### Advantages

* **Memory:** Ideal for large models (e.g., 70B+) or long-context training (reasoning traces) where PPO OOMs.
* **Throughput:** Faster forward/backward passes per token than PPO due to fewer active networks.

### Trade-offs

* **Sample Efficiency:** May require more total rollout samples ($K$) to match PPO's convergence speed per epoch, as the baseline is stochastic rather than learned.
* **Context Length:** The memory savings are often reinvested to support longer context (e.g., 8k-16k+ tokens) for "Thinking" process training (CoT).

## 5. Troubleshooting

### High Variance / Unstable Loss

* **Symptom:** Loss fluctuates wildly or spikes.
* **Fix:** Increase `num_generations` ($K$). The baseline becomes more accurate as $K \to \infty$. If GPU poor, use gradient accumulation to simulate larger batches.

### Reward Hacking (Over-optimization)

* **Symptom:** Reward goes up, but evaluation metrics (e.g., benchmarks, win-rate) drop.
* **Fix:** Increase `kl_coeff`. If using RLOO for reasoning (RLVR), ensure the verifiable reward function (e.g., code execution) is strict and not easily gamed by format tricks.

### Training Collapse (Length Explodes or Zero Output)

* **Symptom:** Model generates infinite repetition or empty strings.
* **Fix:**
    1. Check `kl_coeff` (too low allows drift).
    2. Enable `response_length` regularization.
    3. Restart with a lower `learning_rate`.

### "Cold Start" Issues

* **Symptom:** Model fails to learn anything in the first few steps.
* **Fix:** Ensure the SFT model is sufficiently converged before RL. RLOO struggles to explore if the base policy has near-zero probability of generating a high-reward response.
