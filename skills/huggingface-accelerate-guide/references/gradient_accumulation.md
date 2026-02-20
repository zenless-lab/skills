# Accelerate Gradient Accumulation Reference

Gradient accumulation enables training with larger batch sizes than memory normally allows by accumulating gradients over several batches before stepping the optimizer.

## 1. Basic Implementation

Accelerate simplifies this process and automatically handles gradient synchronization and loss scaling.

```python
from accelerate import Accelerator

# 1. Initialize with steps
accelerator = Accelerator(gradient_accumulation_steps=2)
model, optimizer, dataloader, scheduler = accelerator.prepare(...)

for batch in dataloader:
    # 2. Wrap the forward/backward pass in the accumulate context
    with accelerator.accumulate(model):
        ... # Forward pass and loss calculation
        
        # 3. Accelerate automatically scales the loss and handles syncs
        accelerator.backward(loss)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
```

**CRITICAL:** Ensure **only one forward/backward pass** is performed inside the `with accelerator.accumulate(model):` context manager.

## 2. Handling Variable Size Training Samples (e.g., Causal LM)

For token-level tasks with variable sequence lengths, standard gradient accumulation computes an incorrect loss (averaging per batch instead of across all tokens in the accumulation step).

You must manually handle the accumulation logic and token counting. Do **not** use `accelerator.accumulate(model)` here; instead, use `model.no_sync()` to manage Distributed Data Parallel (DDP) synchronization manually.

```python
...
for update_step in range(total_updates):
    ... # Load `gradient_accumulation_steps` batches into `batch_samples` list
    
    # 1. Gather total non-padded tokens across ALL devices for the full accumulated batch
    local_num_items = sum([(b["labels"].ne(-100)).sum() for b in batch_samples])
    total_items = accelerator.gather(local_num_items).sum().item()
    
    for i, batch in enumerate(batch_samples):
        # 2. Disable sync for all but the last micro-batch to prevent slowdowns
        ctx = model.no_sync if i < len(batch_samples) - 1 else contextlib.nullcontext
        
        with ctx():
            ... # Forward pass
            loss = criterion(outputs, batch["labels"]) # Note: criterion reduction="sum"
            
            # 3. Scale loss by num_processes and gradient_accumulation_steps, 
            # then divide by the true total number of non-padded tokens
            loss = (loss * gradient_accumulation_steps * accelerator.num_processes) / total_items
            accelerator.backward(loss)
            
    optimizer.step()
    ... # Scheduler step and zero_grad
```

## 3. Important Caveats & Edge Cases

### Distributed Setup Slowdowns

Without `accelerator.accumulate` or `model.no_sync()`, DDP synchronizes gradients on *every* backward pass, which can cause a >2x slowdown. Always use the provided context managers to skip unnecessary synchronizations during accumulation.

### FSDP Out-Of-Memory (OOM) Overhead

When using Fully Sharded Data Parallel (FSDP), the `no_sync` context manager requires significant additional memory. In memory-intensive situations, `no_sync` will quickly cause an OOM error.

**Fix:** Disable `no_sync` by configuring the `GradientAccumulationPlugin` to sync each batch. *Note: This resolves OOM but will incur a training slowdown due to the extra communication.*

```python
from accelerate.utils import GradientAccumulationPlugin

# Disable no_sync to save memory in FSDP
plugin = GradientAccumulationPlugin(sync_each_batch=True)
accelerator = Accelerator(..., gradient_accumulation_plugin=plugin)
```
