# Accelerate Best Practices & Feature Guide

This guide covers advanced configurations for memory estimation, quantization, tracking, profiling, and checkpointing.

---

## 1. Model Memory Estimation

Used to determine if a model fits on a specific hardware configuration before downloading full weights.

| Practice | Details |
| :--- | :--- |
| **Best Practice** | Use the CLI: `accelerate estimate-memory [MODEL_ID]`. It uses the `meta` device to simulate loading without consuming actual RAM. |
| **Caveat** | The estimate only covers **loading weights**. For **inference**, add ~20% overhead. For **training** (Adam), the footprint is significantly larger (~4x the model size). |
| **Dtypes** | Supports `float32`, `float16`, `int8`, and `int4`. Specify via `--dtypes`. |

---

## 2. Model Quantization (`bitsandbytes`)

Enables loading massive models (e.g., 80B parameters) on consumer hardware using 8-bit or 4-bit precision.

### Workflow & Best Practices

1. **Initialize Empty:** Use `with init_empty_weights():` to prevent the OS from allocating RAM for the initial model.
2. **Quantize on Load:** Use `load_and_quantize_model()` with a `BnbQuantizationConfig`.
3. **PEFT Training:** You cannot perform standard training on quantized weights. Use the `peft` library to train adapters (LoRA) on top.

### Critical Caveats

* **4-bit Serialization:** Currently **not supported**. You can save/load 8-bit models, but 4-bit models must be re-quantized on every load.
* **Offloading:** You can offload layers to CPU/Disk using a `device_map`.
  * *8-bit:* Offloaded modules are quantized.
  * *4-bit:* Offloaded modules stay in the original `torch_dtype`.

---

## 3. Experiment Trackers

A unified API for logging metrics across multiple processes.

| Feature | Implementation / Best Practice |
| :--- | :--- |
| **Supported** | WandB, TensorBoard, CometML, Aim, MLFlow, ClearML, DVCLive. |
| **Init** | Use `accelerator.init_trackers("project_name", config=hps)` at the start. |
| **Manual Access** | Use `accelerator.get_tracker("wandb")` to access the underlying run object for specific API calls (e.g., `log_artifact`). |
| **Custom Trackers** | Inherit from `GeneralTracker` and implement `log`, `store_init_configuration`, and `name`. |

**Alternative:** If a library is not supported (e.g., Neptune), wrap your logging in `if accelerator.is_main_process:` to avoid duplicate logs from multiple GPUs.

---

## 4. Performance Profiling

Analyze execution time, memory consumption, and FLOPS.

* **Best Practice:** Use `ProfileKwargs` inside the `Accelerator` constructor to configure the PyTorch Profiler.
* **Long Jobs:** For training loops, use the `schedule_option` (wait, warmup, active, repeat) to avoid generating massive, unreadable trace files.
* **Tracing:** Export results using `prof.export_chrome_trace("trace.json")` and view in `chrome://tracing`.

---

## 5. Checkpointing & State Management

Reliably saving and resuming training in distributed environments.

### Key Utilities

* `accelerator.save_state()`: Saves model, optimizer, scheduler, and RNG states.
* `accelerator.register_for_checkpointing(obj)`: Use this for custom objects (like a custom LR scheduler) so they are included in the state.
* `accelerator.skip_first_batches(dataloader, num_batches)`: **Crucial** for resuming an epoch mid-way.

**Caveat:** Checkpoints are generally not portable between different hardware configurations (e.g., changing the number of GPUs) as the state of the optimizer/sharded parameters may differ.
