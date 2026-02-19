# Gradient Spike Score (GSS) Reference Manual

The Gradient Spike Score (GSS) is a relative deviation metric used to quantify the anomaly level of gradients. Unlike absolute gradient norms, GSS measures the "suddenness" of a gradient update relative to its historical trajectory, making it scale-invariant and highly effective for detecting instability caused by data outliers.

## 1. Principles and Definition

GSS identifies outliers by comparing the current gradient magnitude against a historical baseline.

### Mathematical Definition

For a parameter vector $\theta$ at step $t$ with gradient $g_t$:

$$ \text{GSS}(g_t) = \frac{\|g_t\|}{\text{EMA}(\|g\|_{0:t-1})} $$

* **Scale Invariance**: GSS remains robust across different layers (e.g., Embeddings vs. MLP layers) regardless of their varying parameter magnitudes.
* **Physical Meaning**: A high GSS indicates that the current update vector is statistically inconsistent with the optimization trajectory established by previous steps.

## 2. Low-Overhead Implementation

Storing full gradient history is computationally prohibitive for LLMs. In practice, GSS is approximated using the **Second Moment ($v_t$)** from the Adam/AdamW optimizer state, which already tracks the exponential moving average of squared gradients.

### Approximation Strategy (Zero-Memory Cost)

Since $v_t \approx \mathbb{E}[g^2]$, we can derive an instantaneous score:

```python
# Pseudo-code for GSS calculation within an optimizer step
# Access the second moment (exp_avg_sq) from AdamW state
v_t = optimizer.state[param]['exp_avg_sq']

# Calculate approximate GSS
# epsilon is added for numerical stability
gss = param.grad.abs() / (v_t.sqrt() + epsilon)

# Monitor the maximum GSS across tensor elements
max_gss = gss.max().item()
```

## 3. Diagnostic Scenarios

GSS is the primary signal for distinguishing between healthy high-learning-rate updates and pathological data shocks.

| Anomaly Pattern | Numerical Feature | Root Cause | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Transient Spike** | $GSS \gg 10$ (e.g., 100-1000) for a single step. | **Data Outlier**: Corrupted tokens, formatting errors, or extreme length in the current batch.<br>**Overflow**: FP16 numerical instability in LayerNorm. | **Spike-Aware Clipping**: Clip gradients based on GSS threshold rather than global norm.<br>**Nullifying**: Zero out the gradients for this step (often better than clipping for extreme outliers). |
| **Persistent High GSS** | GSS remains elevated; Loss oscillates or diverges. | **Momentum Pollution**: A previous massive spike was integrated into Adam's $v_t$ and $m_t$, causing the optimizer to "chase" a bad direction for hundreds of steps. | **Momentum Reset**: Forcibly reset optimizer states ($m_t=0, v_t=0$) and perform a short learning rate warm-up. |
| **Layer-Specific Anomaly** | High GSS only in Embedding or Output Head. | **Sparse Features**: Rare tokens appearing after long intervals (common in multilingual data). | **Adaptive Scaling**: Use element-wise clipping (e.g., AdaGC) instead of global clipping to accommodate sparse updates. |

## 4. Operational Usage

### 4.1 Automated Intervention (SPAM Strategy)

Implementing **S**pike-**P**erceived **A**dam with **M**omentum Reset:

1. **Detect**: If $\text{max}(GSS) > \tau$ (e.g., $\tau=10$).
2. **Block**: Skip the update or clip aggressively.
3. **Reset**: If spikes cluster (e.g., >5 spikes in 100 steps), revert to the last checkpoint and reset optimizer momentum.

### 4.2 Data Filtration

Retrospective analysis of GSS spikes allows for "Dataset Debugging." Batches causing high GSS should be logged, and their source documents removed from the training corpus to prevent future instability.
