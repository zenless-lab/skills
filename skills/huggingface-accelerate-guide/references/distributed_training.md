# Distributed Training Reference

This guide covers key techniques and strategies for distributed training using Hugging Face Accelerate, including Gradient Accumulation, Local SGD, DDP Communication Hooks, and FSDP.

## 1. Gradient Accumulation

Gradient accumulation allows training with larger effective batch sizes when memory is constrained by accumulating gradients over multiple micro-batches before stepping the optimizer.

### Best Practice: Basic Usage

Use the `accelerator.accumulate(model)` context manager. Accelerate automatically handles gradient synchronization and loss scaling. Ensure only one forward/backward pass occurs inside this context.

```python
accelerator = Accelerator(gradient_accumulation_steps=2)
model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)

for batch in dataloader:
    with accelerator.accumulate(model):
        outputs = model(**batch)
        loss = outputs.loss
        accelerator.backward(loss)
        optimizer.step()
        optimizer.zero_grad()
```

### Pitfall: Variable Sequence Lengths (e.g., Causal LM)

Standard gradient accumulation computes an incorrect loss for token-level tasks with variable sequence lengths (it averages per batch instead of across all tokens).

* **Fix**: Do **not** use `accelerator.accumulate(model)`. Instead, manually manage synchronization using `model.no_sync()` for all but the last micro-batch, and scale the loss by the total non-padded tokens gathered across all devices.

```python
# Manual accumulation for variable sequence lengths
for i, batch in enumerate(batch_samples):
    # Disable sync for all but the last micro-batch
    ctx = model.no_sync if i < len(batch_samples) - 1 else contextlib.nullcontext
    with ctx():
        outputs = model(**batch)
        # Scale loss by total tokens across all devices
        loss = outputs.loss / total_items_across_devices
        accelerator.backward(loss)
```

## 2. Local SGD

Local SGD is a distributed training technique where gradients are not synchronized every step. Instead, each process updates its own model weights, and after $N$ steps, weights are synchronized by averaging across all processes.

### Best Practice: Implementation

Use the `LocalSGD` context manager and call `local_sgd.step()` after every optimizer step. It improves communication efficiency, especially on systems lacking high-speed interconnects (like NVLink).

```python
from accelerate import LocalSGD

with LocalSGD(accelerator=accelerator, model=model, local_sgd_steps=8, enabled=True) as local_sgd:
    for batch in dataloader:
        with accelerator.accumulate(model):
            # ... forward and backward pass ...
            optimizer.step()
            optimizer.zero_grad()
            local_sgd.step() # Synchronize weights every 8 steps
```

### Pitfall: Framework Compatibility

Local SGD currently only works with basic multi-GPU/CPU training. It is **not** compatible with advanced frameworks like DeepSpeed.

## 3. DDP Communication Hooks

DDP Communication Hooks allow overriding the default gradient synchronization behavior during DistributedDataParallel (DDP) training, which is useful for reducing communication overhead via gradient compression.

### Best Practice: Configuration

Configure built-in hooks (e.g., FP16/BF16 compression, PowerSGD) by passing a `DDPCommunicationHookType` to `accelerator.state.kwargs.handlers`.

```python
from accelerate import Accelerator
from accelerate.utils import DDPCommunicationHookType, KwargsHandler

# Enable FP16 gradient compression
ddp_kwargs = KwargsHandler(ddp_communication_hook=DDPCommunicationHookType.FP16)
accelerator = Accelerator(kwargs_handlers=[ddp_kwargs])
```

## 4. Fully Sharded Data Parallel (FSDP)

FSDP shards model parameters, gradients, and optimizer states across all available GPUs, significantly reducing the memory footprint per GPU.

### Best Practice: FSDP2 over FSDP1

Always prefer FSDP2 (`--fsdp_version 2`) when possible. It uses `DTensor` instead of monolithic `FlatParameter`, enabling per-parameter metadata, easier partial freezing (e.g., LoRA), and simpler checkpointing (`SHARDED_STATE_DICT` by default).

### Pitfall: FSDP OOM with Gradient Accumulation

Disabling gradient syncs (`no_sync`) during accumulation in FSDP requires significant extra memory, often causing OOM on large LLMs.

* **Fix**: Set `sync_each_batch=True` in your `GradientAccumulationPlugin`. This disables `no_sync`, trading training speed for memory stability.

```python
from accelerate.utils import GradientAccumulationPlugin

# Prevent OOM during FSDP gradient accumulation
plugin = GradientAccumulationPlugin(num_steps=4, sync_each_batch=True)
accelerator = Accelerator(gradient_accumulation_plugin=plugin)
```

### Best Practice: Auto Wrapping

FSDP requires dividing the model into smaller units. Use Accelerate's auto-wrapping strategies based on size or specific layer types (e.g., Transformer blocks) to optimize communication and memory. Configure this via `accelerate config`.
