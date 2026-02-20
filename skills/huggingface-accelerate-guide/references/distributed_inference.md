# Distributed Inference Reference

Distributed inference generally falls into two realistic scenarios:

1. **Data Parallel Inference**: Loading an entire model onto each GPU and sending chunks of a batch through each GPU's model copy.
2. **Pipeline Parallel Inference**: Loading parts of a model onto each GPU and using scheduled Pipeline Parallelism to process inputs concurrently.

## 1. Data Parallel Inference (Sending Chunks of a Batch)

This is the most memory-intensive solution, requiring each GPU to keep a full copy of the model in memory.

### Best Practice: `split_between_processes`

Instead of manually checking ranks and slicing data, use the `Accelerator.split_between_processes()` context manager (also available in `PartialState` and `AcceleratorState`). It automatically splits data (prompts, tensors, dicts) across all processes.

```python
import torch
from accelerate import PartialState
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
distributed_state = PartialState()
pipe.to(distributed_state.device)

# Assume two processes. GPU 0 gets "a dog", GPU 1 gets "a cat"
with distributed_state.split_between_processes(["a dog", "a cat"]) as prompt:
    result = pipe(prompt).images[0]
    result.save(f"result_{distributed_state.process_index}.png")
```

### Pitfall: Uneven Data Distribution

If you have an odd distribution of prompts to GPUs (e.g., 3 prompts, 2 GPUs), the first GPU receives the first two, and the second receives the third.

* **Fix**: If you need to gather results later, pass `apply_padding=True`. This pads the lists of prompts to the same length (duplicating the last sample). **Crucial**: Remember to drop the final padded sample on the last process after gathering.

```python
# GPU 0: ["a dog", "a cat"], GPU 1: ["a chicken", "a chicken"] (padded)
with distributed_state.split_between_processes(["a dog", "a cat", "a chicken"], apply_padding=True) as prompt:
    result = pipe(prompt).images
```

## 2. Memory-Efficient Pipeline Parallelism (Experimental)

Pipeline parallelism utilizes `torch.distributed.pipelining` to split a large model across multiple GPUs (e.g., using `device_map="auto"`) and process multiple inputs concurrently. Unlike naive model parallelism (where only one GPU is active at a time), pipeline parallelism keeps all GPUs active, making it much faster and more efficient.

### Best Practice: `prepare_pippy`

Use the `accelerate.inference.prepare_pippy()` function to fully wrap the model for pipeline parallelism automatically.

```python
from accelerate.inference import prepare_pippy
from accelerate import PartialState
import torch

# 1. Create model on CPU
model = MyModel(...)
model.eval()

# 2. Create example inputs for tracing (determines relative batch size)
input_tensor = torch.randint(0, vocab_size, (2, 1024), device="cpu")

# 3. Prepare for pipeline parallelism
model = prepare_pippy(model, example_args=(input_tensor,))

# 4. Perform distributed inference
with torch.no_grad():
    output = model(input_tensor)
```

### Pitfall: Output Gathering

By default, `prepare_pippy` sets `gather_output=False` to avoid communication overhead. This means the output will **only** be available on the last process.

* **Fix**: Check `if PartialState().is_last_process:` before accessing the output, OR pass `gather_output=True` to `prepare_pippy` to send the output to all GPUs.

```python
# Accessing output safely when gather_output=False
if PartialState().is_last_process:
    print(output)
```

### Best Practice: `split_points` and `num_chunks`

You can customize pipeline parallelism by passing `split_points` (to determine where to split the model) and `num_chunks` (to determine how the batch is split and sent to the model) to `prepare_pippy`. By default, it uses `device_map="auto"` to find split points.
