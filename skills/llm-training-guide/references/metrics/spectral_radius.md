# Spectral Radius Reference Manual

Spectral Radius, in the context of Large Language Model (LLM) training, refers to the spectral norm ($\|W\|_2$) of a weight matrix, which is its largest singular value ($\sigma_{max}$). It is a fundamental structural metric for monitoring signal gain, training stability, and adherence to the Maximal Update Parametrization ($\mu P$) principles.

## 1. Principles and Definition

The spectral radius defines the maximum amplification factor that a weight matrix applies to an input signal. It serves as the upper bound of the RMS-to-RMS operator norm.

### Mathematical Formulation

For a weight matrix $W$, the spectral norm $\|W\|_2$ is equal to the largest singular value $\sigma_{max}$:

$$
\|W\|_2 = \max_{x \neq 0} \frac{\|Wx\|_2}{\|x\|_2} = \sigma_{max}(W)
$$

### $\mu P$ Scaling Principle

According to the Maximal Update Parametrization ($\mu P$) theory, to maintain feature learning stability as model width increases, the spectral norm of weights should satisfy:

$$
\|W\|_2 = \Theta\left(\sqrt{\frac{d_{out}}{d_{in}}}\right)
$$

* **Physical Meaning**: This scaling ensures that activations remains at a constant $\Theta(1)$ scale regardless of model width, preventing signal explosions or vanishing in deep architectures.

## 2. Low-Overhead Implementation

Since computing a full Singular Value Decomposition (SVD) is computationally prohibitive ($O(N^3)$), the **Power Iteration** method is used for efficient online estimation.

### PyTorch Implementation Pattern

By maintaining a pair of persistent left ($u$) and right ($v$) singular vectors, we can approximate the spectral radius with just a few matrix-vector multiplications per step.

```python
import torch
import torch.nn.functional as F

@torch.no_grad()
def estimate_spectral_radius(weight, u, v, n_iters=1):
    """
    Estimates the spectral radius using Power Iteration.
    weight: The target weight matrix (e.g., param.data)
    u, v: Persistent singular vectors stored in optimizer state.
    """
    # Use BFloat16 to reduce overhead; compute in FP32 for symbols if needed
    w_flat = weight.view(weight.size(0), -1)
    
    for _ in range(n_iters):
        # v <- W^T * u / ||W^T * u||
        v = F.normalize(torch.mv(w_flat.t(), u), p=2, dim=0)
        # u <- W * v / ||W * v||
        u = F.normalize(torch.mv(w_flat, v), p=2, dim=0)
        
    # Rayleigh Quotient approximation
    sigma = torch.dot(u, torch.mv(w_flat, v)).item()
    return sigma, u, v
```

## 3. Operational Utility Analysis

Spectral Radius acts as the "master valve" for controlling signal gain across the model.

### 3.1 Activation Scale Control

Restricting the spectral radius forces activations to maintain a constant RMS magnitude across deep layers. This suppresses outliers in Attention Logits and prevents numerical overflows in mixed-precision training (FP16/BF16).

### 3.2 Mitigation of Weight Drift

During long training runs, standard weight decay often fails to precisely contain the growth of parameter magnitudes. Monitoring spectral radius reveals the decay of the "effective step size" (Update-to-Weight Ratio), ensuring sustained feature learning.

### 3.3 MoE Load Balancing

In Mixture-of-Experts (MoE) models, shared experts often accumulate higher signal gain than routed experts, leading to routing collapse. Aligning spectral radii across experts helps balance signal strength and improve expert utilization.

## 4. Training Health Diagnostics

| Anomaly Pattern | Symptom | Root Cause | Remediation |
| :--- | :--- | :--- | :--- |
| **Activation Explosion** | Spectral radius grows uncontrollably; Logits exceed $\Theta(1)$ scale, causing NaNs. | **Unconstrained Drift**: Optimizers like AdamW allow weights to drift in flat directions, leading to uncontrolled gain. | **Retraction**: Use optimizers like SSO or Muon to project weights back onto a target spectral sphere (radius $R$). |
| **Vanishing Signals** | Spectral radius is too small; activations in deep layers trend toward zero. | **Initialization Mismatch**: In bottleneck layers ($d_{out} \ll d_{in}$), standard scaling causes the initial radius to be $< 1$. | **Spectral Kaiming Scaler**: Adopt a scaling factor of $\sqrt{\max(1, d_{out}/d_{in})}$ to prevent signal collapse in bottlenecks. |
| **Layer-wise Imbalance**| Drastic volatility in radius for some layers while others remain stagnant. | **LR Alignment Failure**: Weights with different shapes use a global LR, violating $\mu P$ consistency assumptions. | **$\mu P$ LR Scaling**: Scale local learning rates by $\Theta(\sqrt{d_{out}/d_{in}})$ for each tensor. |
| **Routing Polarization**| Huge variance in spectral radius across MoE experts. | **Magnitude Mismatch**: High-frequency experts accumulate larger radii, creating a "winner-takes-all" effect. | **Spectral Constraint**: Enforce identical spectral radius limits across all experts to level the signal gain. |

## 5. Summary

For Large-scale LLM pre-training, **Spectral Radius** can be treated as a primary structural health metric.
When facing deep numerical instability or frequent loss spikes, rely on spectral radius audits rather than just gradient clipping. Ensuring the model follows the $\mu P$ manifold trajectory throughout its lifecycle is essential for achieving both convergence speed and long-term stability.
