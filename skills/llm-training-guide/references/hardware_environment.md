# Environment & Hardware Diagnostics

This document details how to detect compute accelerators, verify driver/library versions, and troubleshoot common environment issues.

## 1. NVIDIA GPU (CUDA)

Primary inference target for most AI workloads.

### Detection & Version Checks

**1. Hardware & Driver Status:**

```bash
# Returns: GPU Idx, Name, Driver Ver, CUDA Ver (Driver API), Memory
nvidia-smi --query-gpu=index,name,driver_version,cuda_version,memory.total --format=csv,noheader

```

**2. CUDA Toolkit (NVCC):**

*Note: `nvcc` might not be in PATH even if the driver is installed.*

```bash
nvcc --version
# Fallback if not found:
/usr/local/cuda/bin/nvcc --version

```

**3. cuDNN Version (Deep Inspection):**

Reliable detection requires Python as file paths vary wildly.

```bash
python3 -c "import torch; print(f'cuDNN: {torch.backends.cudnn.version()}');" 2>/dev/null || echo "Torch_Not_Found"

```

### Troubleshooting Guide

* **Symptom:** `nvidia-smi` returns "command not found".
* **Action:** CUDA driver is not installed. Fallback to CPU.

* **Symptom:** "Failed to initialize NVML: Driver/library version mismatch".
* **Action:** The kernel module version differs from the user-space library. **Reboot required** or reload kernel modules (`rmmod nvidia`).

* **Symptom:** `CUDA out of memory`.
* **Action:** Check `nvidia-smi` for other processes consuming VRAM. Clear cache or reduce batch size.

* **Symptom:** `nvcc` not found but `nvidia-smi` works.
* **Action:** Runtime is installed, but Dev Toolkit is missing. Compilation of custom ops (e.g., flash-attention) will fail.

---

## 2. AMD GPU (ROCm)

### Detection & Version Checks

**1. Hardware Status:**

```bash
# JSON output is safer for parsing
rocm-smi --showproductname --showdriverversion --showmeminfo vram --json

```

**2. HIP Compiler:**

```bash
hipcc --version

```

**3. Environment Variables:**

Check specifically for override flags often needed for consumer cards (e.g., RX 7900 XTX).

```bash
env | grep HSA_OVERRIDE_GFX_VERSION

```

### Troubleshooting Guide

* **Symptom:** "HipErrorNoBinaryForGpu: Unable to find code object".
* **Action:** The binary was not compiled for this specific GPU architecture. Set `HSA_OVERRIDE_GFX_VERSION` (e.g., to `11.0.0` for RDNA3) and retry.

* **Symptom:** Permission denied when accessing GPU.
* **Action:** Ensure the user is in the `render` or `video` group (`usermod -aG render $USER`).

---

## 3. Apple Silicon (Metal/MPS)

### Detection & Version Checks

**1. Chip Architecture:**

```bash
# Output should contain "Apple M1/M2/M3..."
sysctl -n machdep.cpu.brand_string

```

**2. macOS Version (MPS/Metal Support):**

For PyTorch MPS, macOS 12.3+ is required. Newer Metal features may require later macOS versions.

```bash
sw_vers -productVersion

```

**3. PyTorch MPS Availability:**

```bash
python3 -c "import torch; print(torch.backends.mps.is_available())"

```

### Troubleshooting Guide

* **Symptom:** "Not implemented" error for specific operations.
* **Action:** MPS support is incomplete compared to CUDA. Fallback to `cpu` for that specific operation definition.

* **Symptom:** High memory pressure/Swap usage.
* **Action:** Apple Silicon uses Unified Memory. VRAM equals System RAM minus OS overhead. Reduce model size.

---

## 4. Google TPU

### Detection

TPUs are typically accessed via network endpoints or specific local devices (`/dev/accel0`).

**1. Environment Variables:**

```bash
env | grep -E "TPU_NAME|TPU_IP_ADDRESS|XRT_TPU_CONFIG"

```

**2. Runtime Version:**

```bash
python3 -c "import jax; print(jax.lib.xla_bridge.get_backend().platform)"

```

### Troubleshooting Guide

* **Symptom:** Connection timeout.
* **Action:** Verify the VM has network access to the TPU node.

* **Symptom:** "Resource exhausted" (Preemption).
* **Action:** On Cloud TPU, this means the instance was preempted. Check logic requires a restart/checkpoint reload.

---

## 5. CPU & Vector Extensions

Fallback layer. Performance depends heavily on instruction sets (AVX-512, AMX).

### Detection

**1. Instruction Sets:**
Check for acceleration flags.

* **Intel/AMD:** `lscpu | grep -E "avx512|amx|vnni"`
* **ARM:** `lscpu | grep -E "asimd|sve"`

**2. Thread Count:**
Important for setting `OMP_NUM_THREADS`.

```bash
nproc --all

```

### Troubleshooting Guide

* **Symptom:** "Illegal instruction (core dumped)".
* **Action:** The binary (e.g., `llama.cpp`) was compiled with AVX2/AVX512 support, but the current CPU does not support it. Recompile with lower compatibility.
