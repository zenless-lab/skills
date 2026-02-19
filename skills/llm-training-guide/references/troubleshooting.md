# Troubleshooting

This document serves as the primary reference for agents to diagnose and resolve LLM and deep learning training failures. It categorizes errors into four domains and provides symptom-to-solution mappings.

## 1. Engineering & Environment Crashes (Critical)

Explicit errors halting the training process.

| Issue | Symptoms | Root Causes | Solutions |
| :--- | :--- | :--- | :--- |
| **Build/Env Incompatibility** | `ImportError`, segmentation faults, install failures. | API signature changes (e.g., PyTorch/CUDA mismatches); OS/Hardware limits (e.g., DeepSpeed on M2). | 1. Strict version locking (Docker/`requirements.txt` for PyTorch, CUDA, NCCL).<br>2. Replace incompatible APIs (e.g., `view()` -> `reshape()` for non-contiguous tensors). |
| **CUDA Out of Memory (OOM)** | `RuntimeError: CUDA out of memory`. | Excessive batch size; Unreleased gradients (memory leaks); VRAM fragmentation. | 1. Reduce Micro-Batch Size & use Gradient Accumulation.<br>2. Enable BF16/FP16 & Activation Checkpointing.<br>3. Profile for deadlocks causing VRAM hoarding. |
| **File System I/O Bottlenecks** *(Added)* | Extremely low GPU util (MFU), data loading timeouts. | Reading millions of small files; Slow network file systems (NFS). | 1. Pack data into binary formats (WebDataset, TFRecord).<br>2. Cache data to local NVMe SSDs before training. |

## 2. Silent Failures & Dynamics Anomalies

Training proceeds, but model metrics degrade or fail to improve.

| Issue | Symptoms | Root Causes | Solutions |
| :--- | :--- | :--- | :--- |
| **Loss Spikes & Gradient Explosion** | Sudden loss increase, NaNs, oscillating metrics. | High gradient norms (dirty data, numerical instability); Excessive LR/insufficient warmup. | 1. Monitor Gradient Norm & Gradient Spike Score (GSS > 50 is critical).<br>2. Apply Adaptive Gradient Clipping (AdaGC).<br>3. Implement automated checkpoint rollback & batch skipping. |
| **Non-Convergence / "Fake Learning"** | Loss plateaus near random chance (e.g., $Loss \approx -\log(1/C)$). | Bad weight initialization (vanishing/exploding gradients); Silent data drops (e.g., HF Trainer dropping un-tokenized inputs). | 1. **Overfit One Batch:** Ensure loss hits 0 on 2-10 samples.<br>2. **Zero-Input Baseline:** Train on zeroed inputs; if loss drops, the model is learning statistical bugs, not features. |
| **Representation Collapse** *(Added)* | All outputs converge to the same token/vector; Dead ReLUs. | High learning rates with ReLU architectures; Normalization layers failing. | 1. Switch to SwiGLU or GeLU.<br>2. Check LayerNorm/RMSNorm implementations for numerical underflow. |

## 3. Data Quality & Pipeline Issues

Silent errors capping model capability, often discovered post-training.

| Issue | Symptoms | Root Causes | Solutions |
| :--- | :--- | :--- | :--- |
| **Data Contamination** | Unusually high benchmark scores but poor zero-shot real-world ability; High CoDeC. | Test set leakage into training set; Massive duplication. | 1. Deduplication via MinHash/Bloom Filters.<br>2. Run CoDeC/Zlib ratio checks to detect memorization. |
| **Format & Preprocessing** | Mojibake (gibberish text), infinite generation, repetition. | Missing BOS/EOS tokens; UTF-8 decoding errors; Uncleaned HTML boilerplate. | 1. **Decode & Inspect:** Visually inspect decoded Token IDs before passing to the model.<br>2. Use structured HTML parsers, not just regex. |
| **Tokenizer Mismatches** *(Added)* | Good loss during training, absolute garbage during inference. | Training and inference environments use different tokenizer versions or configs (e.g., missing added vocab). | 1. Serialize tokenizer config alongside model weights.<br>2. Add strict assertion checks for `vocab_size` across pipelines. |

## 4. Distributed System Bugs

Hardware faults and synchronization errors across multi-node/multi-GPU setups.

| Issue | Symptoms | Root Causes | Solutions |
| :--- | :--- | :--- | :--- |
| **Silent Inconsistency** | Global loss normal, but model weights diverge across GPUs. | Unsynchronized random seeds (Dropout/Init); Desynced DistributedSampler. | 1. Monitor Direction Consistency & Loss Dispersion across ranks.<br>2. Force seed alignment for all stochastic operations at initialization. |
| **Hangs & Communication Timeouts** | Progress bar freezes, MFU drops to 0, no traceback. | NCCL deadlocks from node crash/packet loss; Zombie processes. | 1. Set `NCCL_COMM_ID_TIMEOUT` watchdog to force crash and trace.<br>2. Implement auto-isolation of dead nodes and resume from latest checkpoint. |
| **Straggler Effect** *(Added)* | Overall step time fluctuates wildly. | One degraded GPU or thermal throttling node delaying the All-Reduce barrier. | 1. Profile individual rank step times.<br>2. Use dynamic load balancing or replace underperforming hardware. |

## 5. Troubleshooting Flowchart (Summary)

* **If Crash:**
  * Check Logs: OOM -> Adjust Batch Size / Gradient Accumulation.
  * Check Traceback: Shape Error -> Verify API signatures (`view` vs `reshape`) / Data Collator.
* **If Loss Anomaly (Spikes/Flatline):**
  * *Always* perform "Overfit One Batch" first.
  * Check Gradient Norm / GSNR to differentiate explosion vs. vanishing.
  * Decode input tensors to check for silent dropping or encoding errors.
* **If Hang or Distributed Issue:**
  * Check Loss Dispersion (is loss identical across GPUs?).
  * Enable `NCCL_DEBUG=INFO` to check communication layer logs.
  * Identify and isolate straggler nodes.
