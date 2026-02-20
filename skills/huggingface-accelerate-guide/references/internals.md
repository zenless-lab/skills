# Accelerate Internal Mechanisms Reference

Understanding Accelerate's internal state management and object wrapping is crucial for debugging distributed training setups.

## 1. Initialization and State Management

When `Accelerator()` is instantiated, it analyzes the launch environment to determine the distributed setup, total processes, and current process rank.

* All environment data is stored in `AcceleratorState` (or its barebones parent, `PartialState`).
* This state is uniquely shared across all instances of the class (acting as a singleton).

## 2. The `prepare()` Method

Calling `accelerator.prepare(...)` transforms standard PyTorch objects into their distributed-aware counterparts:

* **Models**: Wrapped in the appropriate container for the active distributed setup (e.g., DDP, FSDP).
* **Optimizers**: Wrapped in `AcceleratedOptimizer`.
* **Schedulers**: Wrapped in `AcceleratedScheduler`.
* **DataLoaders**: **Re-created** (not just wrapped) into either `DataLoaderShard` or `DataLoaderDispatcher`.
  * *Why re-created?* PyTorch does not allow modifying a DataLoader's `batch_sampler` after creation. Accelerate must swap it out to handle data sharding across processes.

## 3. DataLoader Implementations

Accelerate handles distributed data loading via two primary subclasses:

* **`DataLoaderShard`**:
  * Shards data at the *dataset level* (changes the `batch_sampler` to yield alternating batches per process).
  * Automatically synchronizes the appropriate Random Number Generator (RNG) across processes at each new iteration.
  * Handles automatic device placement (`device_placement=True`).
* **`DataLoaderDispatcher`**:
  * Unlike `DataLoaderShard`, data starts entirely on process 0, and is *then* split and explicitly dispatched to each worker process during iteration.
* **Stateful DataLoaders**: If `torchdata>=0.8.0` and `DataLoaderConfiguration(use_stateful_dataloader=True)` is passed, these classes inherit from `StatefulDataLoader` and maintain a trackable `state_dict`.

## 4. Random Number Generator (RNG) Synchronization

To ensure operations like dataset shuffling match across processes, Accelerate synchronizes RNGs.

**Critical Warnings for Custom Datasets/Samplers:**

* **PyTorch >= 1.6**: Accelerate syncs the `generator` attribute of a given sampler (e.g., `RandomSampler`).
* **PyTorch < 1.6**: Accelerate syncs the *main* PyTorch RNG.
* **Side Effects**: If the main PyTorch RNG is synchronized, **all processes will apply the exact same random data augmentations** if they rely on the main `torch` RNG.
* **Best Practice**: Always use a local `torch.Generator` object for randomization inside custom samplers, batch samplers, or iterable datasets to avoid unwanted identical augmentations across GPUs.
