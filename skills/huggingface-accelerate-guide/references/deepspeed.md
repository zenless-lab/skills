# DeepSpeed Reference

DeepSpeed is a deep learning optimization library that makes distributed training and inference highly efficient. Accelerate integrates DeepSpeed to enable training and inference of massive models via the Zero Redundancy Optimizer (ZeRO).

## 1. Core Concepts (ZeRO)

* **ZeRO Stage 1**: Shards optimizer states across data parallel workers/GPUs.
* **ZeRO Stage 2**: Shards optimizer states + gradients.
* **ZeRO Stage 3**: Shards optimizer states + gradients + model parameters.
* **ZeRO-Offload**: Offloads gradients and optimizer states to CPU/Disk (builds on Stage 2).
* **ZeRO-Infinity**: Offloads model parameters to CPU/Disk (builds on Stage 3).
* **ZeRO++ (Hierarchical Partitioning)**: Enables efficient multi-node training with data-parallel training across nodes and ZeRO-3 sharding within a node.

## 2. Integration Methods

Accelerate provides two ways to use DeepSpeed:

1. **DeepSpeed Plugin (`accelerate config`)**: Generates a basic configuration via CLI prompts. Good for default settings. Requires no code changes.
2. **DeepSpeed Config File**: Provide a custom JSON config file via `accelerate config`. Supports all core features of DeepSpeed and provides maximum flexibility.

```bash
# Example: Launching with a custom DeepSpeed config
accelerate launch --deepspeed_config_file ds_config.json my_script.py
```

## 3. Best Practices & Common Pitfalls

### Pitfall: ZeRO-3 Initialization OOM

When using ZeRO-3, initializing a massive model on the main node before sharding will cause an Out-Of-Memory (OOM) error.

* **Fix**: Models must be initialized within the `accelerator.prepare()` context or using the `zero.Init()` context manager to ensure parameters are partitioned immediately upon creation.

```python
# Correct ZeRO-3 Initialization
from accelerate import Accelerator
accelerator = Accelerator()

# Model is partitioned as it is created
with accelerator.prepare():
    model = MyMassiveModel()
```

### Pitfall: Multiple Models (e.g., GANs)

DeepSpeed requires each model to have its own DeepSpeed engine.

* **Fix**: Pass all models, optimizers, and schedulers to `accelerator.prepare()` simultaneously. Accelerate will initialize a separate DeepSpeed engine for each model automatically.

```python
# Correct preparation for multiple models
model_A, optimizer_A, model_B, optimizer_B = accelerator.prepare(
    model_A, optimizer_A, model_B, optimizer_B
)
```

### Best Practice: NVMe for Offloading

When using ZeRO-Offload or ZeRO-Infinity to disk, always use NVMe drives. Standard HDDs or slow SSDs will severely bottleneck training speeds. Configure the offload path in your DeepSpeed config:

```json
"zero_optimization": {
    "stage": 3,
    "offload_param": {
        "device": "nvme",
        "nvme_path": "/local_nvme"
    }
}
```

### Best Practice: Mixed Precision Alignment

DeepSpeed handles mixed precision internally. Ensure your Accelerate config (`fp16` or `bf16`) strictly matches the DeepSpeed config to avoid dtype mismatch errors.

## 4. DeepSpeed ZeRO-3 for Inference

While ZeRO-2 is primarily for training, ZeRO-3 can be used for inference to load huge models across multiple GPUs that wouldn't fit on a single GPU. It uses the same ZeRO protocol but without the optimizer and learning rate scheduler.
