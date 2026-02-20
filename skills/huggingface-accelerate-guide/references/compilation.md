# Compilation Reference

PyTorch 2.0 introduced `torch.compile`, a powerful feature that makes PyTorch code run faster by JIT-compiling PyTorch code into optimized kernels. Accelerate provides seamless integration, allowing you to benefit from both distributed execution and compilation optimizations simultaneously.

## 1. Using `torch.compile` with Accelerate

Accelerate provides the `TorchDynamoPlugin` to easily integrate `torch.compile` into your training scripts.

```python
from accelerate import Accelerator
from accelerate.utils import TorchDynamoPlugin

# Configure the compilation backend
dynamo_plugin = TorchDynamoPlugin(
    backend="inductor",  # Options: "inductor", "aot_eager", "aot_nvfuser", etc.
    mode="default",      # Options: "default", "reduce-overhead", "max-autotune"
    fullgraph=True,
    dynamic=False
)

# Initialize accelerator with the plugin
accelerator = Accelerator(dynamo_plugin=dynamo_plugin)

# This will apply torch.compile to your model
model = accelerator.prepare(model)
```

### Best Practice: Compatibility

It is compatible with all other features and plugins of Accelerate, including mixed precision, distributed training (DDP, FSDP, DeepSpeed), etc.

### Pitfall: Cold Start Overhead

The first execution of compiled code typically takes significantly longer as it includes the compilation time. Subsequent runs are much faster. Do not benchmark performance on the first iteration.

## 2. Regional Compilation

Instead of trying to compile the whole model, which usually has a large problem space for optimization, regional compilation targets repeated blocks of the same class (e.g., Transformer layers) and compiles them sequentially to hit the compiler's cache.

### Best Practice: Speeding Up Cold Starts

Regional compilation drastically reduces the compilation overhead/cold start time of models like LLMs and Transformers, while delivering performance speedups similar to full compilation.

### Best Practice: Large Models & Batch Sizes

The benefits of regional compilation are most pronounced in larger models and larger batch sizes, where the compilation time savings are substantial and the runtime performance difference is minimal.

### How to Use Regional Compilation

Enable it by setting `use_regional_compilation=True` in the `TorchDynamoPlugin` configuration:

```python
from accelerate import Accelerator
from accelerate.utils import TorchDynamoPlugin

# Enable regional compilation
dynamo_plugin = TorchDynamoPlugin(
    use_regional_compilation=True,
    backend="inductor"
)

accelerator = Accelerator(dynamo_plugin=dynamo_plugin)
model = accelerator.prepare(model)
```

Alternatively, you can use the `accelerate.utils.compile_regions` utility directly, just as you would use `torch.compile`.

```python
from accelerate.utils import compile_regions

# Compile specific repeated regions manually
model = compile_regions(model)
```
