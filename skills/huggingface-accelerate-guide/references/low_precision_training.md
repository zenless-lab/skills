# Low Precision (FP8) Training Methods Reference

Training in 8-bit precision (FP8) instead of 16-bit (BF16/FP16) reduces memory footprint and increases throughput without degrading final performance.

## 1. Hardware Requirements

FP8 training is only enabled on specific NVIDIA hardware:

* Consumer graphics cards after the 3000 series (e.g., RTX 4090).
* Hopper-based GPU architectures (e.g., H100, H200).

## 2. Core API Configuration

To enable FP8, pass `mixed_precision="fp8"` to the `Accelerator`. You can specify the backend using `RecipeKwargs` dataclasses: `MSAMPRecipeKwargs`, `TERecipeKwargs`, or `AORecipeKwargs`.

```python
from accelerate import Accelerator
from accelerate.utils import MSAMPRecipeKwargs, TERecipeKwargs, AORecipeKwargs

# Example using default settings (Accelerate auto-selects MS-AMP if installed)
accelerator = Accelerator(mixed_precision="fp8")

# Example specifying a backend explicitly
kwargs = [MSAMPRecipeKwargs(optimization_level="O2")]
accelerator = Accelerator(mixed_precision="fp8", kwarg_handlers=kwargs)
```

## 3. Supported Backends

### A. MS-AMP

MS-AMP provides optimization levels (`opt_level`) to convert specific operations into FP8 or FP16. It is generally the easiest to configure.

* **`"O1"`**: Casts weight gradients and `all_reduce` communications to FP8; weights stored in FP16; optimizer states in FP32. Reduces communication bandwidth by half.
* **`"O2"`**: Includes `"O1"` benefits, plus casts first-order optimizer states into FP8 and second-order states into FP16. (Currently, only the `Adam` optimizer is supported). Maximizes memory savings with minimal accuracy degradation.
* *(Note: `"O3"` exists for DeepSpeed DDP scenarios but is not currently supported in the Accelerate integration).*

### B. TransformersEngine (TE)

TE acts as a drop-in replacement for specific model layers, replacing `nn.LayerNorm` with `te.LayerNorm` and `nn.Linear` with `te.Linear`.

* **Use Case:** Performance gains are typically only visible on large models (billions of parameters) where these two layers make up the majority of the architecture.
* **Memory vs Accuracy:** Computations are cast to FP8, but everything else remains in FP32. This uses the most memory among FP8 methods but guarantees the least accuracy loss.
* **Configuration:** Can be customized via `TERecipeKwargs` (or `FP8RecipeKwargs(backend="te")`) with parameters like `margin`, `interval`, `fp8_format` (usually `HYBRID` for training, `E4M3` for eval), `amax_history_len`, and `amax_compute_algo`.

### C. torchao (Experimental)

A hackable, PyTorch-native backend. For numerical stability, `torchao` keeps the **first and last layers** of the model at regular precision (FP32 or BF16) and quantizes the remaining intermediate layers to FP8.

* Configured using `AORecipeKwargs()`.

## 4. Backend Comparison Chart

The following chart details the bit-precisions used across different states for each solution during training:

| Method / Level | Computation (GEMM) | Comm | Weight | Master Weight | Weight Gradient | Optimizer States |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FP16 AMP** | FP16 | FP32 | FP32 | N/A | FP32 | FP32+FP32 |
| **Nvidia TE** | FP8 | FP32 | FP32 | N/A | FP32 | FP32+FP32 |
| **MS-AMP O1** | FP8 | FP8 | FP16 | N/A | FP8 | FP32+FP32 |
| **MS-AMP O2** | FP8 | FP8 | FP16 | N/A | FP8 | FP8+FP16 |
| **MS-AMP O3** | FP8 | FP8 | FP8 | FP16 | FP8 | FP8+FP16 |

*\*MS-AMP O3 is shown for reference but is restricted to specific DeepSpeed versions and not currently integrated directly into Accelerate.*

> **💡 Pro-Tip:** Early experiments suggest that combining **MS-AMP** (to reduce memory overhead) with **TransformersEngine** (to leverage NVIDIA's optimized FP8 operators) can yield the highest overall throughput.
