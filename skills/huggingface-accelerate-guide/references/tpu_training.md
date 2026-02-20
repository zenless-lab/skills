# TPU Training with Accelerate Reference

Training on TPUs introduces specific architectural differences compared to multi-GPU setups. This reference covers critical edge cases regarding process launching, mixed precision, and memory allocation overhead.

## 1. Notebook Launching & Memory Exhaustion (SIGSEGV)

When launching distributed training from a Jupyter Notebook (e.g., Colab, Kaggle), Accelerate's `notebook_launcher` uses process **forking** instead of **spawning** (which is used in command-line execution).

**The Problem:** In low-resource environments, instantiating the model *inside* the training function causes the system to create $N$ copies of the model (one per forked process), rapidly exhausting system RAM and resulting in a cryptic `ProcessExitedException: process 0 terminated with signal SIGSEGV` error.

**The Solution:** Instantiate the model exactly *once* outside the training function and pass it as an argument. The shared instance will be passed back and forth between nodes.

```python
from accelerate import Accelerator, notebook_launcher

# 1. Instantiate outside the training loop
model = AutoModelForSequenceClassification.from_pretrained(...)

# 2. Pass model as an argument
def training_function(model):
    accelerator = Accelerator()
    # Do NOT instantiate the model here
    ...
    model, optimizer, train_dataloader = accelerator.prepare(model, ...)
    ...

# 3. Launch by passing the model in the arguments tuple
notebook_launcher(training_function, (model,))
```

*Note: This workaround is strictly necessary for low-resource notebook environments. Scripts or high-resource servers do not strictly require this.*

## 2. Mixed Precision Configurations

TPUs support both `fp16` and `bf16`, but **`bf16` is highly recommended** for its extreme efficiency on TPU architecture.

Accelerate provides two layers of `bf16` configuration mapping to XLA environment variables:

* **Base Level (`mixed_precision="bf16"`):**
  * Sets `XLA_USE_BF16=1`.
  * Casts *both* `torch.float` and `torch.double` to `bfloat16`.
  * Usage: `accelerator = Accelerator(mixed_precision="bf16")`

* **Downcast Level (`downcast_bf16=True`):**
  * Sets `XLA_DOWNCAST_BF16=1`.
  * Casts `torch.float` to `bfloat16`, but casts `torch.double` to `float32`.
  * **Why use it?** Downcasting ensures that metric calculations, logging, and operations requiring higher precision remain usable, which raw `bf16` tensors might corrupt.
  * Usage: `accelerator = Accelerator(mixed_precision="bf16", downcast_bf16=True)`

## 3. TPU Memory Allocation & Training Speed

TPUs exhibit a unique warmup behavior.

* **Initial Slowdown:** When a script launches, the first few batches are exceptionally slow. The TPU is actively profiling the data to determine the optimal memory allocation before locking it in for high-efficiency processing.
* **The Evaluation Batch Size Trap:** If your evaluation dataloader uses a *larger* batch size than your training dataloader, the TPU will trigger a completely new memory reallocation step when evaluation begins, causing severe slowdowns.
* **Best Practice:** Keep the evaluation `batch_size` strictly equal to the training `batch_size` to prevent continuous memory reallocation overhead.
