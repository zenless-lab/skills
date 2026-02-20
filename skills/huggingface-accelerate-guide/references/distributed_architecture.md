# Distributed Training Architecture & Performance Reference

When migrating or comparing model performance across different distributed setups (Single GPU, Multi-GPU, TPU), results will not naturally align unless specific variables are controlled. This document outlines the best practices, critical API usages, and common pitfalls in distributed training with Accelerate, FSDP, and DeepSpeed.

## 1. Hyperparameter Alignment & Reproducibility

To achieve identical convergence across setups, three core factors must be strictly managed:

* **Universal Seed Setting:** Always use `accelerate.utils.set_seed(42)` instead of standard library seeds. This automagically synchronizes random, numpy, torch, cuda, and XLA states.
* **Observed Batch Sizes:** Accelerate passes the **batch size per device** to the dataloader.
  * *Effective Batch Size = Per-Device Batch Size × Number of Processes.*
  * If you move from 1 GPU (bs=128) to 2 GPUs, you must halve the per-GPU batch size (bs=64) to maintain the same effective batch size.
* **Learning Rate Linear Scaling:** As effective batch sizes grow with more devices, the learning rate generally needs to be scaled *linearly* (`lr = base_lr * accelerator.num_processes`).

> **Note:** When using mixed precision or gradient accumulation, expect slight batch-wise loss variance due to precision truncation and gradient averaging math, but overall convergence should remain roughly the same.

## 2. Process Synchronization (Execution & Deferring)

In a distributed environment, processes execute asynchronously. You must prevent race conditions (e.g., one GPU starts training before another finishes downloading weights).

* **`accelerator.wait_for_everyone()`:** Blocks all processes that arrive first until all other processes reach this line.
* **`accelerator.main_process_first()`:** A context manager that forces the main process to execute a block of code before the others (uses `wait_for_everyone` under the hood).

**Best Practices for Synchronization:**

* **Downloading Datasets:** Use `with accelerator.main_process_first():` to cache the dataset on the main process first.
* **Loading Checkpoints:** Wait for all workers to load `state_dict` before resuming training.
* **Early Stopping:** Use `accelerator.set_trigger()` when a condition is met locally, and `accelerator.check_trigger()` to broadcast the break command globally.

## 3. Gradient Synchronization & Accumulation

In Distributed Data Parallel (DDP), processes synchronize gradients on the `backward()` pass. When accumulating gradients, synchronizing on every micro-batch causes massive slowdowns (>2x).

* **The Fix:** Use `with accelerator.accumulate(model):` which automatically utilizes PyTorch's `no_sync()` context manager to skip communication until the final accumulation step.
* **⚠️ FSDP Out-Of-Memory (OOM) Pitfall:** Disabling gradient syncs (`no_sync`) in Fully Sharded Data Parallel (FSDP) requires significant extra memory. In memory-intensive scenarios (like training large LLMs), this causes OOM.
  * *Solution:* Set `sync_each_batch=True` in your `GradientAccumulationPlugin` to disable `no_sync`. This trades training speed (slower) for memory stability (prevents OOM).

## 4. FSDP vs. DeepSpeed Frameworks

Accelerate integrates both FSDP and DeepSpeed. While they both partition model states, they handle memory and data precision differently:

* **Data Precision Handling (The Upcasting Pitfall):** * *DeepSpeed* disregards `torch_dtype` during model preparation and creates local "flat params" in `float32`. This can cause **significant memory overhead** during initialization on a small number of GPUs.
  * *FSDP* creates flat params adhering to the loaded `torch_dtype` (e.g., `bf16`), saving memory.
* **FSDP1 vs. FSDP2:** FSDP2 replaces the monolithic `FlatParameter` with `DTensor` (Distributed Tensor).
  * *Why FSDP2 is better:* It allows per-parameter metadata, enabling partial parameter freezing (LoRA works out of the box), mixing `fp8` and other dtypes, and faster/simpler checkpointing (`SHARDED_STATE_DICT` is now default).
  * *Migration:* Use `--fsdp_version 2`. `--fsdp_use_orig_params` and `--fsdp_sync_module_states` are now obsolete and removed.

## 5. Long Sequence Training (Context vs. Sequence Parallelism)

When sequence lengths explode (e.g., 128k+ tokens), standard attention memory requirements scale quadratically. Accelerate offers two solutions to shard inputs across the sequence dimension.

### Context Parallelism (CP)

Shards the `Q, K, V` matrices and computes attention across multiple GPUs using Ring Attention.

* **Prerequisites:** Requires FSDP2 and SDPA (Scaled Dot Product Attention) without causal masks.
* **Communication Strategy:** Default is `allgather`. While `all-to-all` sounds better theoretically, `allgather` usually outperforms it in practice due to lower idle bubble times.
* **Label Shifting:** You MUST manually shift labels *before* passing them into the model. Standard transformers causal shifting fails under CP because the labels are sharded.

### Sequence Parallelism (SP) - Ulysses

Shards inputs along the sequence dimension but computes attention by slicing the *attention heads* across GPUs.

* **Backend:** Powered by DeepSpeed (ALST integration).
* **Constraints:** The number of attention heads must be divisible by the SP degree (`sp_size`).
* **Usage:** Requires manual, differentiable loss aggregation across ranks (e.g., `torch.distributed.nn.functional.all_gather(loss, group=sp_group)`) to ensure gradients compute correctly across the sequence shards.
* **Tip:** Combine with Liger-Kernel to natively handle `shift_labels` and fuse logit-loss computations for maximum memory efficiency.
