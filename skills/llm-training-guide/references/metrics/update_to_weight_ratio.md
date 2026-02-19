# Update-to-Weight Ratio Reference Manual

Update-to-Weight Ratio (U/W Ratio) is a scale-invariant metric that quantifies the "relative step size" of parameter updates. It serves as the primary standard for validating Learning Rate (LR) configuration and monitoring optimization health in LLMs.

## 1. Principles and Definition

The metric measures the magnitude of the update vector relative to the magnitude of the parameter vector itself, providing a normalized view of training speed across layers with different scales.

### Mathematical Expression

For a parameter tensor $\theta$ and its update step $\Delta \theta$ (computed by the optimizer, e.g., AdamW):

$$ \text{Ratio} = \frac{\|\Delta \theta\|_2}{\|\theta\|_2 + \epsilon} $$

* **$\Delta \theta$ in Adam**: $\Delta \theta = -\eta \cdot \frac{m_t}{\sqrt{v_t} + \epsilon}$ (where $\eta$ is LR, $m_t$ is momentum, $v_t$ is variance).
* **Scale Invariance**: Unlike raw Gradient Norm, this ratio is independent of the layer's depth or width, making it comparable across Embedding layers (large numerical values) and Attention layers (small numerical values).

## 2. Monitoring Implementation

Calculating exact updates requires accessing the optimizer's internal state.

### 2.1 PyTorch Implementation Pattern

To monitor this without significant overhead, compute it periodically (e.g., every 100 steps) or on a subset of layers.

```python
def log_update_ratio(model, optimizer, scheduler):
    # Note: accurate calculation requires accessing the *actual* step 
    # applied by the optimizer, not just grad * lr
    
    for name, param in model.named_parameters():
        if param.grad is None: continue
        
        # Approximate step for AdamW (simplified)
        # Real implementation should read optimizer.state[param]
        lr = scheduler.get_last_lr()[0]
        update_approx = lr * param.grad # This is a proxy for SGD; Adam differs
        
        param_norm = param.data.norm(2)
        update_norm = update_approx.norm(2)
        
        ratio = update_norm / (param_norm + 1e-9)
        
        # Log critical layers (Embeddings, Final Layer)
        if "embed" in name or "layers.0" in name:
            logger.log({f"ratios/{name}": ratio.item()})
```

### 2.2 Layer-wise Granularity

It is crucial to differentiate between layer types:

* **Embeddings**: Often have smaller ratios due to sparse updates.
* **LayerNorm**: Ratios can be volatile; often excluded from aggregate statistics.
* **Attention/FFN**: The primary indicators for training stability.

## 3. Diagnostic Thresholds

The U/W Ratio provides a "Health Check" for the Learning Rate.

| Status | Numerical Range | Diagnosis | Root Cause | Actionable Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Critical High** | $> 10^{-2}$ (1%) | **Unstable / Explosion Risk** | Learning Rate (LR) is too high; Gradient Clipping failed; Initialization variance too low. | **Decrease LR**: Reduce by factor of 2-5x.<br>**Re-init**: Check if weights are initialized too small ($\sigma$ too low). |
| **Optimal** | $\approx 10^{-3}$ | **Healthy Training** | "Golden Ratio". Parameters update by ~0.1% per step. | **Maintain**: The configuration is likely optimal. |
| **Stagnant** | $< 10^{-4}$ | **Slow Convergence** | LR too low; Gradient Vanishing in deep layers. | **Increase LR**: Aggressively scale up LR.<br>**Check Architecture**: Verify Pre-LN or residual scaling. |
| **Sudden Spike** | Jump $> 10x$ | **Instability Event** | "Bad Data" batch; Loss landscape curvature singularity. | **Rollback**: Revert checkpoint and skip batch.<br>**AdaGC**: Enable adaptive gradient clipping. |

## 4. Application in Scaling ($\mu P$)

In the context of **Maximal Update Parametrization ($\mu P$)**, the U/W Ratio is the key observable for transferring hyperparameters from small proxy models to large target models.

* **Transfer Logic**: If a 1B model trains stably with a U/W ratio of $10^{-3}$, the 100B model should be initialized and configured (LR scaled by width) to maintain this exact same $10^{-3}$ ratio.
* **Verification**: During the first 100 steps of a large run, if the U/W ratio deviates significantly from the small model's ratio, the initialization or LR scaling formula is incorrect.
