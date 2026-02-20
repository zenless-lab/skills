# Update-to-Weight Ratio Reference Manual

Update-to-Weight Ratio (U/W Ratio) is a scale-invariant metric that quantifies the "relative step size" of parameter updates. It is a practical indicator for validating Learning Rate (LR) configuration and monitoring optimization health in LLMs.

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

## 3. Diagnostic Thresholds (Heuristics)

The U/W Ratio provides a practical "health check" for the learning rate. Exact ranges vary by model family, optimizer details, data curriculum, and training stage.

| Status | Numerical Range | Diagnosis | Root Cause | Actionable Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Critical High** | $> 10^{-2}$ (1%) | **High Instability Risk** | LR too high; clipping ineffective; initialization scale mismatch. | **Decrease LR**: Reduce by factor of 2-5x.<br>**Recheck Init**: Verify initialization variance and normalization. |
| **Reference Zone** | around $10^{-3}$ | **Often Stable in Practice** | Relative update size is typically moderate for many transformer runs. | **Maintain/Track**: Keep monitoring trend rather than one-step value. |
| **Very Low** | $< 10^{-4}$ | **Possible Slow Progress** | LR too low; effective gradient too weak in deeper blocks. | **Increase LR Carefully**: Scale up gradually and re-evaluate validation metrics. |
| **Sudden Spike** | Jump $> 10x$ | **Instability Event** | Outlier batch, transient numerical issue, or abrupt curvature shift. | **Triage**: Inspect batch/logs, then decide whether to skip step or roll back. |

## 4. Application in Scaling ($\mu P$)

In the context of **Maximal Update Parametrization ($\mu P$)**, the U/W Ratio is the key observable for transferring hyperparameters from small proxy models to large target models.

* **Transfer Logic**: If a 1B proxy model trains stably near a specific U/W range (often around $10^{-3}$), the larger model can target a similar range after width-aware scaling.
* **Verification**: During early steps of a large run, major deviation from the proxy range is a useful signal to re-check initialization or LR scaling.
