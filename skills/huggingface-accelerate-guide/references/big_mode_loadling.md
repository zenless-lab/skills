# Accelerate Big Model Loading Reference

When loading massive models (e.g., 6B+ parameters), standard PyTorch `torch.load` loads the model into RAM twice (random initialization + checkpoint weights), quickly causing OOM errors. Accelerate solves this using "Meta Device" initialization and Sharded Checkpoints.

## 1. The Core Workflow

Use `init_empty_weights` to instantiate a parameterless skeleton on the PyTorch `meta` device, then use `load_checkpoint_and_dispatch` to map weights onto available hardware (GPU -> CPU RAM -> Disk).

```python
from accelerate import init_empty_weights, load_checkpoint_and_dispatch
from transformers import AutoConfig, AutoModelForCausalLM

# 1. Load config (no weights loaded yet)
config = AutoConfig.from_pretrained("checkpoint_name")

# 2. Instantiate an empty model skeleton (consumes 0 RAM)
with init_empty_weights():
    model = AutoModelForCausalLM.from_config(config)

# 3. Load weights and automatically distribute them
model = load_checkpoint_and_dispatch(
    model, 
    checkpoint="path/to/sharded_checkpoint", 
    device_map="auto", 
    no_split_module_classes=["BlockName"] # e.g., "GPT2Block"
)
```

## 2. Key Parameters & Configuration

* **`device_map="auto"`**: Automatically fills available GPU space first, overflows to CPU RAM, and finally spills to Disk as memory-mapped tensors if necessary.
* **`no_split_module_classes`**: **Highly recommended.** Pass a list of block names (e.g., `['Block']`) that contain residual connections. Splitting these across devices will break the model's forward pass.
* **Custom `max_memory`**: You can cap the memory usage per device.

```python
from accelerate import infer_auto_device_map

# CRITICAL: Always leave 1-2GB of headroom per GPU because PyTorch CUDA kernels consume memory upon initialization.
max_memory = {0: "10GiB", 1: "15GiB", "cpu": "30GiB"}

device_map = infer_auto_device_map(
    model, 
    max_memory=max_memory,
    no_split_module_classes=["BlockName"]
)

model = load_checkpoint_and_dispatch(
    model, checkpoint="path/to/checkpoint", device_map=device_map
)
```

## 3. Explicit Offloading (Optional)

If you only want to offload to a specific device instead of using `device_map="auto"`:

* `cpu_offload(model, execution_device)`: Keeps weights in CPU RAM, moving them to the GPU only during the forward pass.
* `disk_offload(model, offload_dir, execution_device)`: Keeps weights on the hard drive (NVMe highly recommended).

## 4. Limitations & Edge Cases ⚠️

* **Inference Only:** This API is strictly for inference. It does **not** support training. Computations should happen behind a `torch.no_grad()` context manager.
* **Naive Parallelism:** The model pipeline across GPUs is sequential. Only one GPU works at a time while the others sit idle waiting for activations.
* **Generation Memory on GPU 0:** If you use Transformers' `.generate()` method, the output generation and tensor processing usually happen on GPU 0. Give GPU 0 *less* memory in `max_memory` to leave room for the generation context (e.g., for an 8-GPU setup, give GPU 0 ~30GB and the rest ~46GB).
* **Disk Offload Speed:** Relying on the disk (via `device_map="auto"` overflowing to disk or `disk_offload`) will be extremely slow unless using a high-speed NVMe drive.
