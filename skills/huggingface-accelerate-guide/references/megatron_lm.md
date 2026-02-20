# Megatron-LM Reference

Megatron-LM is a powerful framework developed by NVIDIA for training large transformer models efficiently. It provides advanced parallelism techniques, including Tensor Parallelism (TP), Pipeline Parallelism (PP), and Sequence Parallelism (SP), which are essential for scaling models to hundreds of billions of parameters.

## 1. Core Parallelism Techniques

* **Tensor Parallelism (TP)**: Splits individual layers (e.g., attention heads, feed-forward networks) across multiple GPUs. This reduces the memory footprint of each layer and allows for larger models.
* **Pipeline Parallelism (PP)**: Divides the model into sequential stages, placing each stage on a different GPU. Activations are passed between stages, enabling the training of models that exceed the memory of a single GPU.
* **Sequence Parallelism (SP)**: Shards the sequence dimension of activations across GPUs, further reducing memory usage, especially for long-context tasks.

## 2. Integration with Accelerate

Accelerate integrates Megatron-LM to simplify the setup and execution of these complex parallelism strategies.

* **Configuration**: Use `accelerate config` to set up Megatron-LM parameters, such as TP degree, PP degree, micro-batch size, and global batch size.
* **Initialization**: Accelerate handles the initialization of the Megatron-LM distributed environment, including process groups and communication communicators.
* **Model Preparation**: `accelerator.prepare()` wraps the model with Megatron-LM's parallel layers and handles the distribution of parameters.

```python
from accelerate import Accelerator

# Accelerate handles Megatron-LM initialization based on the config
accelerator = Accelerator()

# Model is wrapped with Megatron-LM parallel layers
model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)
```

## 3. Best Practices & Common Pitfalls

### Pitfall: Hardware Requirements

Megatron-LM is highly optimized for NVIDIA GPUs and relies heavily on fast interconnects like NVLink and NVSwitch for efficient communication, especially for Tensor Parallelism.

* **Fix**: Do not use Tensor Parallelism across nodes. Keep TP within a single node (e.g., `tp_degree <= 8` on an 8-GPU node) and use Pipeline Parallelism or Data Parallelism across nodes.

### Pitfall: Checkpointing Formats

Megatron-LM uses a specific checkpoint format. Accelerate provides utilities to save and load these checkpoints, but converting them to standard Hugging Face formats may require additional steps.

* **Fix**: Use `accelerator.save_state()` to save Megatron-LM checkpoints. To convert back to Hugging Face format, use the provided conversion scripts in the Transformers library.

### Pitfall: Data Loading

Megatron-LM requires specialized data loaders that can handle the distributed nature of the training process, ensuring that each worker receives the correct data partition.

* **Fix**: Ensure your dataset is properly sharded across data parallel ranks. Accelerate's `prepare()` handles basic dataloader sharding, but complex Megatron-LM setups may require custom dataset implementations.

### Best Practice: Start Small

Begin with a smaller model and a simple parallelism setup (e.g., only TP) to ensure the environment is configured correctly before scaling up to 3D parallelism (TP + PP + DP).

### Best Practice: Monitor Communication

Use profiling tools (like PyTorch Profiler or NVIDIA Nsight) to monitor communication overhead, as excessive communication can bottleneck training performance.

### Best Practice: Leverage Sequence Parallelism

For tasks with long sequences (e.g., 32k+ tokens), enable Sequence Parallelism to significantly reduce activation memory. This is usually configured in the Megatron-LM config file or via `accelerate config`.
