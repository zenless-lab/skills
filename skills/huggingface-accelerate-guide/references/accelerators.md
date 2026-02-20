# Accelerators Reference

Hugging Face Accelerate supports a variety of hardware accelerators, making it simple to train and infer models across different platforms. This guide covers Amazon SageMaker, Apple Silicon (MPS), Intel CPU, and Intel Gaudi.

## 1. Amazon SageMaker

Accelerate provides seamless integration with Amazon SageMaker, allowing you to easily launch training jobs on the AWS cloud using Hugging Face Deep Learning Containers (DLCs).

### Best Practice: Saving Models

In SageMaker, you must save your model to `/opt/ml/model` or `os.environ["SM_MODEL_DIR"]` so that artifacts are automatically uploaded to S3 after training.

```python
import os
from accelerate import Accelerator

accelerator = Accelerator()
# ... training loop ...

# Save to SageMaker's expected directory
save_dir = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
accelerator.save_state(save_dir)
```

### Pitfall: Argparse Booleans

SageMaker doesn't support `argparse` boolean actions natively.

* **Fix**: Specify `type=bool` in your script and provide an explicit `True` or `False` value for hyperparameters.

### Best Practice: Local Mode

Set `ec2_instance_type: local` in your config to run your training script locally inside a Docker container. This is invaluable for debugging before launching expensive cloud jobs.

## 2. Apple Silicon (MPS)

With PyTorch's Metal Performance Shaders (MPS) backend, Accelerate supports hardware-accelerated training on Macs equipped with Apple Silicon (M1/M2/M3, etc.).

### Best Practice: Out-of-the-Box (MPS)

If an MPS device is detected, Accelerate enables it by default. It allows local prototyping and fine-tuning, leveraging unified memory to reduce data retrieval latency.

```bash
# Launching on MPS (automatically detected)
accelerate launch my_script.py
```

### Pitfall: Distributed Training

Distributed setups (`gloo` and `nccl`) are **not** supported with the `mps` device. Currently, only a single GPU (single MPS device) can be used.

## 3. Intel CPU

Accelerate fully supports optimized training on Intel CPUs, including single-machine and multi-machine distributed training.

### Best Practice: Distributed Setup

Use Intel oneCCL and the Intel MPI library for efficient cluster messaging.

* You must configure a `hostfile` containing the IP addresses of all nodes.
* Before launching, you must source the oneCCL bindings environment (`setvars.sh`).

```bash
# Example: Sourcing oneCCL and launching
oneccl_bindings_for_pytorch_path=$(python -c "from oneccl_bindings_for_pytorch import cwd; print(cwd)")
source $oneccl_bindings_for_pytorch_path/env/setvars.sh

accelerate launch my_script.py
```

### Pitfall: `accelerator.prepare` Limitations

`accelerator.prepare` can currently only handle simultaneously preparing multiple models (with no optimizer) OR a single model-optimizer pair.

* **Fix**: If you have multiple model-optimizer pairs, call `accelerator.prepare` separately for each pair to avoid verbose errors.

```python
# Correct preparation for multiple pairs on Intel CPU
model_A, optimizer_A = accelerator.prepare(model_A, optimizer_A)
model_B, optimizer_B = accelerator.prepare(model_B, optimizer_B)
```

## 4. Intel Gaudi (HPU)

Intel Gaudi AI accelerators provide high-performance and cost-effective model training and inference.

### Best Practice: Out-of-the-Box (HPU)

If an Intel Gaudi device is detected, Accelerate enables it by default.

### Pitfall: Advanced Features Require Optimum

Certain advanced features are not part of the core Accelerate library and require the `optimum-habana` library. These include:

* `fast_ddp`: Implements DDP via all-reduce on gradients instead of the Torch DDP wrapper.
* `minimize_memory`: Used for FP8 training to keep weights in memory between passes.
* `context_parallel_size`: Used for Context/Sequence Parallelism (CP/SP) to reduce memory footprint.
