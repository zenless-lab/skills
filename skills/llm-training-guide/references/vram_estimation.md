# VRAM Estimation Guide for LLMs

This document provides a technical framework for calculating Video RAM (VRAM) requirements for Large Language Model (LLM) training and inference, following the principle of modular resource analysis.

## 1. VRAM Consumption Formulas

### 1.1 Model Weights (Static)

The memory required to load the model parameters.

$$
\text{Memory}_{\text{weights}} = \Phi \times Q
$$

* **$\Phi$:** Number of parameters (in billions).
* **$Q$:** Precision factor (Bytes per parameter).
  * FP32: 4 bytes
  * FP16/BF16: 2 bytes
  * INT8: 1 byte
  * INT4: 0.5 bytes
  * FP4 (NVFP4): 0.5 bytes

### 1.2 Training States (Optimizer & Gradients)

Additional memory required during the training process.

$$
\text{Memory}_{\text{states}} = \Phi \times (\text{Grad} + \text{Opt})
$$

* **Grad**: Gradients (usually same as weight precision, e.g., 2 bytes for FP16).
* **Opt**: Optimizer states.
* **Standard AdamW**: 12 bytes (Master Weights [4] + Momentum [4] + Variance [4]).
* **8-bit AdamW**: 2 bytes (Quantized states).
* **Adam-mini**: ~4-5 bytes (Block-sharded states).
* **SGD**: 0 bytes (or 4 bytes with momentum).
* **Paged Optimizers**: 0 VRAM (States are offloaded to CPU RAM/NVMe).

### 1.3 KV Cache (Inference Context)

Memory used to store Key and Value tensors for autoregressive generation.

$$
\text{Memory}_{\text{KV}} = 2 \times B \times L \times H_{kv} \times D_{head} \times S \times P
$$

* **2**: For Key and Value matrices.
* **$B$**: Batch size.
* **$L$**: Number of layers.
* **$H_{kv}$**: Number of KV heads (Note: $H_{kv} < H_{attn}$ in GQA/MQA).
* **$D_{head}$**: Head dimension (e.g., 128).
* **$S$**: Sequence length (Context + Generation).
* **$P$**: Precision bytes (e.g., 2 for FP16).

### 1.4 Activations (Dynamic Training)

Intermediate tensors stored during the forward pass for backpropagation.

$$
\text{Memory}_{\text{act}} \approx \text{Layers} \times \text{SeqLen} \times \text{Batch} \times \text{HiddenSize} \times \text{Bytes} \times \text{ArchitectureFactor}
$$

* **Activation Checkpointing**: Reduces consumption to $O(\sqrt{\text{Layers}})$ or a constant per layer by recomputing values during the backward pass.

---

## 2. Quick Reference Tables

### Table 1: Parameter Weight Memory (Static)

*Estimates for loading the model into VRAM (No KV Cache/Activations).*

| Model Size | FP16 / BF16 (2B) | INT8 (1B) | INT4 / FP4 (0.5B) | Full AdamW States (12B) |
| --- | --- | --- | --- | --- |
| **1B** | 2.0 GB | 1.0 GB | 0.5 GB | 12.0 GB |
| **7B / 8B** | 16.0 GB | 8.0 GB | 4.0 GB | 96.0 GB |
| **14B** | 28.0 GB | 14.0 GB | 7.0 GB | 168.0 GB |
| **70B** | 140.0 GB | 70.0 GB | 35.0 GB | 840.0 GB |
| **405B** | 810.0 GB | 405.0 GB | 202.5 GB | 4.8 TB |

---

### Table 2: KV Cache Memory per 1,000 Tokens (Inference)

*Memory usage at Batch Size = 1. Scales linearly with Batch and SeqLen.*

| Architecture Type | Examples | Per 1k Tokens (FP16) | 32k Context (FP16) | 128k Context (FP16) |
| --- | --- | --- | --- | --- |
| **MHA** (Standard) | Llama-1 (7B) | ~0.50 GB | 16.0 GB | 64.0 GB |
| **GQA** (Grouped) | Llama-3 (8B) | ~0.06 GB | 1.9 GB | 7.7 GB |
| **GQA** (Large) | Llama-3 (70B) | ~0.16 GB | 5.1 GB | 20.5 GB |
| **MLA** (Latent) | DeepSeek-V3 | ~0.02 GB | 0.6 GB | 2.4 GB |

---

### Table 3: Activation Memory (Training)

*Assumes Single Batch, Hidden Size proportional to model size.*

| Model Config | Sequence Length | Standard (FP16) | With Gradient Checkpointing |
| --- | --- | --- | --- |
| **Llama-3 (8B)** | 2,048 | ~12.0 GB | ~1.5 GB |
| **Llama-3 (8B)** | 8,192 | ~48.0 GB | ~4.2 GB |
| **Llama-3 (70B)** | 4,096 | ~110.0 GB | ~16.0 GB |
| **Llama-3 (70B)** | 32,768 | ~880.0 GB (OOM) | ~80.0 GB |

---

### Table 4: Buffer & System Overhead

*Reserved memory that is not directly tied to model parameters.*

| Component | VRAM Usage | Description |
| --- | --- | --- |
| **CUDA Context** | 0.6 GB - 1.2 GB | Base memory taken by the driver and runtime. |
| **NCCL Buffers** | 0.5 GB - 2.0 GB | Communication buffers for distributed training (Multi-GPU). |
| **Fragmentation** | 5% - 10% | Unusable gaps in VRAM caused by allocator behavior. |
| **Temporary Buffers** | 0.2 GB - 1.0 GB | Scratch space for operations like Softmax or Norms. |

---

## 3. Impact of Optimization Techniques

### 3.1 Parameter Efficient Fine-Tuning (PEFT/LoRA)

* **Model Weights**: Base model is frozen (can be INT4/INT8 via QLoRA).
* **Trainable Weights**: Usually <1% of model size.
* **Optimizer States**: Only required for the trainable parameters.
* **Benefit**: Reduces Optimizer/Gradient VRAM by >99%, but Activation memory remains high.

### 3.2 Quantized Optimizers (8-bit / Paged)

* **8-bit Adam**: Reduces optimizer state footprint by 75% (from 12 bytes to 3 bytes per param).
* **Paged Adam**: Offloads states to CPU RAM. VRAM usage for optimizer states drops to **0**, allowing models to fit that otherwise would not, at the cost of 2x-4x slower training.

### 3.3 Model Parallelism (ZeRO)

* **ZeRO-1**: Shards Optimizer States across GPUs.
* **ZeRO-2**: Shards Optimizer States + Gradients.
* **ZeRO-3**: Shards Optimizer States + Gradients + Model Parameters.
* **ZeRO-Infinity**: Offloads all states and parameters to NVMe, theoretically supporting trillion-parameter models on a single GPU.
