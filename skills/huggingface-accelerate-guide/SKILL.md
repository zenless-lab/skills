---
name: huggingface-accelerate-guide
description: A specialized assistant for using Hugging Face Accelerate for distributed training, inference, and large model handling. It provides guidance on environment setup, best practices, and troubleshooting.
---
# Accelerate Guide

## Skill Overview
This skill focuses on using the **Hugging Face Accelerate** library.
Use this skill to:
1.  **Setup**: Install and configure Accelerate in various environments (e.g., `uv`, `pip`).
2.  **Train**: Implement distributed training patterns (FSDP, DeepSpeed, Megatron-LM).
3.  **Infer**: Handle large model inference and distributed inference.
4.  **Troubleshoot**: Debug distributed setups and optimize performance.

## External Resources
* **Hugging Face MCP Server**:
  If the `hf-mcp-server` is available, use it to search and fetch documentation. The agent can install the `hf-mcp-server` MCP via:
  ```json
  {
    "servers": {
      "hf-mcp-server": {
        "url": "https://huggingface.co/mcp?login"
      }
    }
  }
  ```
* **Accelerate Reference Documentation**:
  If the `hf-mcp-server` is not available, access the documentation via the following URLs:
  * [Accelerator](https://huggingface.co/docs/accelerate/package_reference/accelerator.md)
  * [State](https://huggingface.co/docs/accelerate/package_reference/state.md)
  * [CLI](https://huggingface.co/docs/accelerate/package_reference/cli.md)
  * [Torch Wrappers](https://huggingface.co/docs/accelerate/package_reference/torch_wrappers.md)
  * [Tracking](https://huggingface.co/docs/accelerate/package_reference/tracking.md)
  * [Launchers](https://huggingface.co/docs/accelerate/package_reference/launchers.md)
  * [DeepSpeed](https://huggingface.co/docs/accelerate/package_reference/deepspeed.md)
  * [Logging](https://huggingface.co/docs/accelerate/package_reference/logging.md)
  * [Big Modeling](https://huggingface.co/docs/accelerate/package_reference/big_modeling.md)
  * [Inference](https://huggingface.co/docs/accelerate/package_reference/inference.md)
  * [Kwargs](https://huggingface.co/docs/accelerate/package_reference/kwargs.md)
  * [FP8](https://huggingface.co/docs/accelerate/package_reference/fp8.md)
  * [Utilities](https://huggingface.co/docs/accelerate/package_reference/utilities.md)
  * [Megatron-LM](https://huggingface.co/docs/accelerate/package_reference/megatron_lm.md)
  * [FSDP](https://huggingface.co/docs/accelerate/package_reference/fsdp.md)

## Guide to Writing Accelerate Code

This section provides a step-by-step guide on how to adapt your PyTorch code to use Accelerate, based on official Hugging Face documentation.

### 1. Initialization & Device Placement
Always start by creating an `Accelerator` instance. Let Accelerate handle device placement by using `accelerator.device` instead of hardcoding `"cuda"`.

```python
from accelerate import Accelerator

accelerator = Accelerator()
device = accelerator.device

# Move your model to the correct device
model.to(device)
```

### 2. Preparing Objects
Use `accelerator.prepare()` to wrap your model, optimizer, dataloaders, and scheduler. This ensures they are properly distributed across the available hardware.

```python
model, optimizer, train_dataloader, scheduler = accelerator.prepare(
    model, optimizer, train_dataloader, scheduler
)
```

### 3. The Training Loop
Remove manual `.to(device)` calls for inputs and targets, as Accelerate's DataLoader handles this automatically. Replace `loss.backward()` with `accelerator.backward(loss)`.

```python
for batch in train_dataloader:
    optimizer.zero_grad()
    inputs, targets = batch
    
    outputs = model(inputs)
    loss = loss_function(outputs, targets)
    
    # Use accelerator.backward instead of loss.backward()
    accelerator.backward(loss)
    
    optimizer.step()
    scheduler.step()
```

### 4. Advanced Training Features
Accelerate makes it easy to add features like gradient accumulation and mixed precision.

```python
# Initialize with gradient accumulation and mixed precision
accelerator = Accelerator(gradient_accumulation_steps=2, mixed_precision="fp16")

for batch in train_dataloader:
    # Use the accumulate context manager
    with accelerator.accumulate(model):
        inputs, targets = batch
        outputs = model(inputs)
        loss = loss_function(outputs, targets)
        
        accelerator.backward(loss)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
```

### 5. Execution Control & Synchronization
Manage how and when processes are executed across GPUs.

```python
# Print only on the main process
accelerator.print("Training started!")

# Block processes until all have reached this point
accelerator.wait_for_everyone()

# Execute code only on the main process (e.g., pushing to the Hub)
if accelerator.is_main_process:
    repo.push_to_hub()
```

### 6. Saving and Loading
Always unwrap your model using `accelerator.unwrap_model(model)` before saving to avoid saving distributed-specific wrappers.

```python
accelerator.wait_for_everyone()

# Unwrap the model before saving
unwrapped_model = accelerator.unwrap_model(model)
unwrapped_model.save_pretrained(
    "path/to/save", 
    is_main_process=accelerator.is_main_process, 
    save_function=accelerator.save
)

# Save full state (optimizer, scheduler, random generators) for resuming
accelerator.save_state("path/to/checkpoint")
```

### 7. TPU Considerations
When training on TPUs, ensure all tensors in batches have the same length (avoid dynamic padding) and keep code static to prevent slow graph recompilations. If using weight tying, retie weights after preparation.

```python
from accelerate.utils import DistributedType

if accelerator.distributed_type == DistributedType.TPU:
    model.tie_weights()
```

### 8. Launching Scripts and Notebooks
Always configure your environment first using `accelerate config`. 

**From the CLI:**
```bash
accelerate launch script.py --arg1 --arg2
```

**From a Jupyter Notebook:**
Ensure CUDA-specific code is inside the launched training function.
```python
from accelerate import notebook_launcher

def training_loop(mixed_precision="fp16", seed=42, batch_size=64):
    # Training code here...
    pass

args = ("fp16", 42, 64)
notebook_launcher(training_loop, args, num_processes=2)
```

## Local Assets

### Reference Guides
*   **Accelerators**: See [the reference guide](references/accelerators.md) for details on supported hardware accelerators.
*   **Best Practices**: See [the reference guide](references/best_practices.md) for additional best practices and optimization tips.
*   **Big Model Loading**: See [the reference guide](references/big_mode_loadling.md) for details on loading models that exceed single-device memory.
*   **Compilation**: See [the reference guide](references/compilation.md) for details on graph compilation (e.g., `torch.compile`).
*   **DeepSpeed**: See [the reference guide](references/deepspeed.md) for details on integrating DeepSpeed.
*   **Distributed Architecture**: See [the reference guide](references/distributed_architecture.md) for details on the underlying distributed architecture.
*   **Distributed Inference**: See [the reference guide](references/distributed_inference.md) for details on splitting models across devices for inference.
*   **Distributed Training**: See [the reference guide](references/distributed_training.md) for details on distributed training concepts.
*   **Examples**: See [the reference guide](references/examples.md) for details on various usage examples.
*   **Gradient Accumulation**: See [the reference guide](references/gradient_accumulation.md) for details on accumulating gradients over multiple steps.
*   **Inference**: See [the reference guide](references/inference.md) for details on running inference with Accelerate.
*   **Internals**: See [the reference guide](references/internals.md) for details on Accelerate's internal mechanisms.
*   **Low Precision Training**: See [the reference guide](references/low_precision_training.md) for details on FP16, BF16, and FP8 training.
*   **Megatron-LM**: See [the reference guide](references/megatron_lm.md) for details on Megatron-LM integration.
*   **TPU Training**: See [the reference guide](references/tpu_training.md) for details on TPU-specific training practices.
*   **Troubleshooting**: See [the reference guide](references/troubleshooting.md) for details on debugging and resolving common issues.

### Code Templates & Examples
*   **Big Model Inference Dispatch**: See [the template](assets/big_model_inference_dispatch.py) for dispatching large models across multiple devices.
*   **Complete CV Classification Example**: See [the example](assets/complete_cv_classification_example.py) for a full computer vision classification training script.
*   **Complete NLP MRPC Example**: See [the example](assets/complete_nlp_mrpc_example.py) for a full NLP sequence classification training script.
*   **DeepSpeed Training Template**: See [the template](assets/deepspeed_training_template.py) for a starting point when using DeepSpeed.
*   **Distributed Inference Split**: See [the template](assets/distributed_inference_split.py) for splitting models for distributed inference.
*   **Distributed Training Patterns**: See [the template](assets/distributed_training_patterns.py) for common distributed training patterns.
*   **FP8 Mixed Precision Template**: See [the template](assets/fp8_mixed_precision_template.py) for implementing FP8 mixed precision training.
*   **Gradient Accumulation Basic**: See [the template](assets/gradient_accumulation_basic.py) for a basic implementation of gradient accumulation.
*   **Megatron-LM Pretraining Template**: See [the template](assets/megatron_lm_pretraining_template.py) for a starting point when pretraining with Megatron-LM.
*   **NLP Causal LM Template**: See [the template](assets/nlp_causal_lm_no_trainer_template.py) for a custom training loop for causal language models.
*   **Troubleshooting Debug Tools**: See [the template](assets/troubleshooting_debug_tools.py) for tools and snippets to help debug distributed setups.
