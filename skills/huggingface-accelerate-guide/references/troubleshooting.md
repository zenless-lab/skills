# Accelerate Troubleshooting Guide

This guide addresses common distributed training failures, hanging code, and memory issues. Use these patterns to identify and fix bottlenecks.

## 1. Synchronized Logging

Standard Python logging can be chaotic in multi-process setups. Use `accelerate.logging` to ensure clean, synchronized output.

```python
from accelerate.logging import get_logger

# 1. Initialize (level can be set via ACCELERATE_LOG_LEVEL env var)
logger = get_logger(__name__, log_level="DEBUG")

# 2. Control process output
logger.debug("Only on main process")
logger.info("On all processes", main_process_only=False)
logger.info("In order across processes", main_process_only=False, in_order=True)
```

## 2. Hanging Code & Timeout Errors

Hanging usually indicates a synchronization mismatch where one process is waiting for another that has already finished or is stuck.

### A. Mismatched Tensor Shapes

Collective operations like `gather()` or `reduce()` require **identical tensor shapes** across all processes.

* **Solution:** Enable Debug Mode to catch tracebacks immediately.
  * **CLI:** `accelerate launch --debug {script.py}`
  * **Env Var:** `ACCELERATE_DEBUG_MODE="1"`
  * **Config:** Set `debug: true` in `config.yaml`.

### B. Early Stopping Synchronization

If only Process 0 meets the stopping condition and breaks the loop, other processes will wait indefinitely at the next barrier.

```python
# Use triggers to sync boolean flags across all processes
if should_stop_early(loss):
    accelerator.set_trigger()

if accelerator.check_trigger():
    break # All processes break simultaneously
```

### C. Infrastructure Issues

* **Linux Kernel:** Versions < 5.5 are known to hang; upgrade if possible.
* **MPI:** Ensure **passwordless SSH** is configured between all nodes.

## 3. Handling Out-of-Memory (OOM)

The `find_executable_batch_size` utility automatically retries training with halved batch sizes upon OOM.

```python
from accelerate.utils import find_executable_batch_size

def training_loop(args):
    accelerator = Accelerator()

    @find_executable_batch_size(starting_batch_size=args.batch_size)
    def inner_loop(batch_size):
        nonlocal accelerator
        accelerator.free_memory() # Clear lingering references
        
        # Declare memory-consuming objects INSIDE the inner function
        model = get_model()
        train_dataloader = get_dataloader(batch_size)
        ...
        train(model, train_dataloader)

    inner_loop()
```

## 4. Reproducibility & Performance Imbalance

* **Effective Batch Size:** Remember `Effective BS = Per-GPU BS * Num GPUs`. If results differ after changing hardware, verify the effective batch size and learning rate scaling.
* **Heterogeneous GPUs:** If using different GPU models, the cluster performance is throttled by the **slowest device**. Imbalanced VRAM will limit the entire cluster to the batch size of the smallest GPU.
