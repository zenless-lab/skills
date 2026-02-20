# Inference Reference

Accelerate provides powerful Big Model Inference capabilities, allowing you to run inference on models that exceed the memory capacity of a single GPU.

## 1. Big Model Inference Core Concepts

The core idea behind Big Model Inference is to distribute model weights across all available storage devices (GPU, CPU memory, and even disk) and dynamically load them onto the compute device only when needed.

### Typical Workflow

1. **Initialize Empty Model**: Use the `init_empty_weights` context manager to initialize a model skeleton without parameters. This requires zero memory.
2. **Load and Dispatch Weights**: Use the `load_checkpoint_and_dispatch` method to load the checkpoint into the empty model and distribute the weights across devices based on the `device_map`.

```python
import torch
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

# 1. Initialize empty model (zero memory footprint)
with init_empty_weights():
    model = MyModel(...)

# 2. Load and dispatch weights
model = load_checkpoint_and_dispatch(
    model, 
    checkpoint="path/to/checkpoint", 
    device_map="auto" # Automatically fills GPU -> CPU -> Disk
)

# 3. Perform inference
input_tensor = torch.randn(2, 3)
# Move input to the device of the first layer
device_type = next(iter(model.parameters())).device.type
input_tensor = input_tensor.to(device_type)

output = model(input_tensor)
```

## 2. Device Map (`device_map`)

`device_map="auto"` automatically calculates the optimal weight distribution:

1. Fills all available GPU memory first.
2. If GPU memory is insufficient, uses CPU memory.
3. If CPU memory is also insufficient, uses the disk (the absolute slowest option).

### Pitfall: Splitting Indivisible Layers

If certain layers (like Transformer blocks) shouldn't be split across different devices, specify them via the `no_split_module_classes` parameter.

* **Fix**: Pass a list of class names to `no_split_module_classes` in `load_checkpoint_and_dispatch`.

```python
model = load_checkpoint_and_dispatch(
    model, 
    checkpoint="path/to/checkpoint", 
    device_map="auto",
    no_split_module_classes=["GPT2Block"] # Prevent splitting these blocks
)
```

### Pitfall: Model Parallelism vs. Pipeline Parallelism

While `device_map="auto"` can utilize multiple GPUs, only one GPU is active at any given moment (waiting for the previous GPU's output). This is **not** Pipeline Parallelism.

* **Fix**: Launch your script normally with Python instead of tools like `torchrun` or `accelerate launch`. For true Pipeline Parallelism, refer to the Distributed Inference guide.

## 3. Usage in the Hugging Face Ecosystem

In libraries like Transformers or Diffusers, Big Model Inference is deeply integrated into the `from_pretrained` method.

Simply add `device_map="auto"` to enable it:

```python
from transformers import AutoModelForSeq2SeqLM
import torch

# Automatically dispatch weights and use half-precision to save more memory
model = AutoModelForSeq2SeqLM.from_pretrained(
    "bigscience/T0pp", 
    device_map="auto", 
    torch_dtype=torch.float16
)
```

## 4. Best Practices & Common Pitfalls

### Pitfall: Performance Overhead

Moving weights between CPU/Disk and GPU adds significant overhead to inference.

* **Best Practice**: Always prioritize GPU memory, then CPU memory, and only use disk offloading as a last resort.

### Best Practice: Sharded Checkpoints

If the `state_dict` itself doesn't fit in memory, shard the model weights into multiple checkpoints to save memory during loading. Accelerate handles sharded checkpoints natively.
