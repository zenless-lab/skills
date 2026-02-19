# Singular Entropy Reference Manual

Singular Entropy is a spectral metric based on Singular Value Decomposition (SVD). It diagnoses the **representation capacity** and **spectral health** of the model's weight matrices (particularly the Output Head and Embeddings). It quantifies whether the model utilizes its full feature space or suffers from "Rank Collapse," relying on only a few dominant features.

## 1. Principles and Mathematical Definition

The physical essence of Singular Entropy is to measure the uniformity of the singular value distribution. It reveals the energy distribution shape of the weight matrix in the feature space.

### Mathematical Formulation

Given a weight matrix $W \in \mathbb{R}^{V \times r}$ (e.g., the Logits Head), perform SVD to obtain singular values $\{\sigma_i\}$. Normalize these to a probability distribution $p_i = \sigma_i / \sum_j \sigma_j$.

Singular Entropy $H_{sing}(W)$ is typically defined as the **Kullback-Leibler (KL) Divergence** between the distribution $p$ and a uniform distribution $\mathcal{U}$:

$$H_{sing}(W) = D_{KL}(p \parallel \mathcal{U}) = \sum_{i=1}^r p_i \log(r \cdot p_i) = \log r - H_{Shannon}(p)$$

### Interpretation

* **Low Value ($\approx 0$)**: **High Effective Rank**. The singular value distribution is close to uniform. The model utilizes all dimensions effectively to represent diverse features.
* **High Value**: **Rank Collapse / Spectral Saturation**. The distribution is highly skewed (spiked). Energy is concentrated in a few dominant directions, leaving most dimensions idle. This often indicates the model is hitting the **Softmax Bottleneck**.

*Note: In some contexts, Shannon Entropy is used directly. This document uses the KL Divergence definition (common in Curriculum Learning literature), where a higher value indicates a less healthy (more collapsed) state.*

## 2. Implementation & Monitoring

Since SVD complexity is $O(\min(m^2n, mn^2))$, it is computationally expensive for large matrices.

### 2.1 Low-Frequency / Offline Monitoring

Do not calculate this at every step.

* **Checkpoint Analysis**: Load saved checkpoints offline to perform SVD on `lm_head` or embedding layers.
* **Interval Sampling**: Calculate every 1000-5000 steps during training.

### 2.2 PyTorch Implementation

```python
def calculate_singular_entropy(weight_matrix):
    """
    Calculates KL-divergence based Singular Entropy.
    High value = Rank Collapse (Bad).
    """
    # 1. SVD
    # Note: Use float32 to avoid underflow in singular values
    _, S, _ = torch.linalg.svd(weight_matrix.float(), full_matrices=False)
    
    # 2. Normalize to probability distribution
    S_norm = S / (S.sum() + 1e-12)
    
    # 3. Calculate KL Divergence from Uniform
    # D_KL(P || U) = log(N) - H(P)
    r = S_norm.numel()
    entropy = -torch.sum(S_norm * torch.log(S_norm + 1e-12))
    kl_div = torch.log(torch.tensor(r)) - entropy
    
    return kl_div.item()
```

### 2.3 Proxy Metric: Stable Rank

For more frequent monitoring, **Stable Rank** is a cheaper proxy that is strongly (negatively) correlated with Singular Entropy:
$$\text{StableRank}(W) = \frac{\|W\|_F^2}{\|W\|_2^2}$$

## 3. Operational Utility

Singular Entropy serves as a "Capacity Health Check."

### 3.1 Detecting Late-Stage Degradation

In late training, models may shift from "generalizing" to "memorizing." This is often marked by a sharp rise in Singular Entropy (spectrum peaking) as the model overfits to high-frequency patterns in the data.

### 3.2 Evaluating Data Curriculum

* **Random Ordering**: Often leads to early spectral saturation (high entropy) in smaller models because the model struggles with difficult samples too early.
* **Curriculum Learning**: Sorting data (e.g., by "Age of Acquisition") typically keeps Singular Entropy low, maintaining feature diversity for longer.

### 3.3 Guiding Pruning (AlphaPruning)

Layers with consistently high Singular Entropy (low effective rank) are redundant. They can be identified as candidates for pruning without significant performance loss.

## 4. Diagnostic Scenarios

| Anomaly Pattern | Symptom | Root Cause | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Spectral Saturation** | **High KL Divergence**. Stable Rank drops precipitously. | 1. **Softmax Bottleneck**: Output dimension $d_{model}$ is too small to represent the diversity of the target distribution.<br>2. **Data Difficulty**: Random data ordering causes "indigestion" in small models. | **Curriculum**: Sort training data (Easy $\to$ Hard).<br>**Scaling**: Increase model width ($d_{model}$).<br>**Regularization**: Add Spectral Regularization or Weight Decay. |
| **Isotropy (Whitening)** | **Near-Zero KL Divergence**. Spectrum is perfectly flat. | 1. **Under-training**: Weights remain close to random initialization (Gaussian).<br>2. **Bad Initialization**: Variance is too high, drowning out updates. | **Initialization**: Check std dev (e.g., $1/\sqrt{N}$).<br>**Learning Rate**: Increase LR to break initial symmetry. |
| **Layer Imbalance** | Shallow layers evolve (entropy changes), but **deep layers stay isotropic**. | **Curse of Depth**: Signal attenuation prevents deep layers from learning structured features. | **Scaling**: Apply $1/\sqrt{L}$ scaling to residual branches.<br>**Adaptive LR**: Use layer-wise learning rates. |

## 5. Summary

**Singular Entropy** is critical when training resources are constrained (e.g., small models or distillation).

* **Warning Sign**: A sudden spike in Singular Entropy suggests the model is **"Capacity Constrained"** or suffering from **"Data Difficulty Mismatch."**
* **Action**: Consider Early Stopping or switching to a higher-quality data curriculum.
