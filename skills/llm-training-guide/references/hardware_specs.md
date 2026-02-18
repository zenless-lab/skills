# Hardware Specifications Reference

This document serves as a lookup table for compute power (TFLOPS), VRAM capacity, and memory bandwidth across Data Center and Consumer hardware.

## 1. Data Center & Cloud Accelerators

Designed for high-throughput training and serving. Includes both current flagships and cost-effective legacy options often found in secondary markets.

| Model | Architecture | VRAM | Bandwidth | FP16/BF16 (TFLOPS) | FP8 (TFLOPS) | Notes / Key Feature |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NVIDIA B200** | Blackwell | 192GB HBM3e | 8.0 TB/s | 2,250 | 4,500 | **FP4 Support** (9,000 TFLOPS). The new training/inference standard. |
| **NVIDIA H200** | Hopper | 141GB HBM3e | 4.8 TB/s | 1,979 | 3,958 | Massive bandwidth upgrade over H100; reduces inference latency. |
| **NVIDIA H100** | Hopper | 80GB HBM3 | 3.35 TB/s | 1,979 | 3,958 | Current standard. First with Transformer Engine. |
| **AMD Instinct MI355X** | CDNA 4 | 288GB HBM3e | 8.0 TB/s | ~5,000 | ~10,000 | **Capacity King**. Fits massive models unquantized. |
| **AMD Instinct MI325X** | CDNA 3 | 256GB HBM3e | 6.0 TB/s | 1,307 | 2,614 | Refreshed MI300 with higher capacity and bandwidth. |
| **AMD Instinct MI300X** | CDNA 3 | 192GB HBM3 | 5.3 TB/s | 653 (1,307*) | 2,614 | *Sparse TFLOPS. Competitive H100 alternative. |
| **Google TPU v7** | TPU v7 | *High BW* | - | *Proprietary* | - | "Ironwood". Optimized for massive scale-out pods. |
| **Google TPU v5p** | TPU v5 | 95GB HBM | 2.76 TB/s | 459 | 918 (Int8)| Excellent perf/dollar in Google Cloud ecosystem. |
| **NVIDIA A100** | Ampere | 80GB HBM2e | 2.0 TB/s | 312 | 624 (Int8)| **Gold Standard (Legacy)**. Excellent software support. No native FP8. |
| **NVIDIA A100** | Ampere | 40GB HBM2 | 1.6 TB/s | 312 | 624 (Int8)| Good for training <30B models. |
| **NVIDIA V100** | Volta | 32GB HBM2 | 900 GB/s | 125 | - | Still viable for FP16/FP32 training. Good resale value. |
| **NVIDIA T4** | Turing | 16GB G6 | 320 GB/s | 65 | 130 (Int8)| Inference workhorse. Slow for training. |
| **NVIDIA P40** | Pascal | 24GB G5 | 346 GB/s | *0.18* | 47 (Int8) | **Budget Trap**: Fast Int8 inference, but useless for FP16 training. |

> **Metric Note**: TFLOPS figures are generally "Dense" tensor core performance where applicable. "Sparse" values are typically 2x higher but require specific model pruning.

## 2. Consumer & Workstation GPUs

Suitable for local "Home Labs," prototyping, and fine-tuning smaller models. Bandwidth is usually the bottleneck before compute.

| Model | Architecture | VRAM | Bandwidth | FP16/Tensor (TFLOPS) | Bus Width | Use Case & Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RTX 5090** | Blackwell | 32GB G7 | ~1,792 GB/s| ~165+ | 512-bit | **Local Flagship**. Best for training <30B models locally. |
| **RTX 4090** | Lovelace | 24GB G6X | 1,008 GB/s | 83 (330 Tensor)| 384-bit | Previous King. Excellent CUDA support. |
| **RTX 4080 Super**| Lovelace | 16GB G6X | 736 GB/s | 52 (200 Tensor)| 256-bit | Good inference, tight VRAM for training. |
| **RTX 4060 Ti** | Lovelace | 16GB G6 | **288 GB/s** | 22 | 128-bit | **Bandwidth Bottleneck**. 16GB VRAM is good, but speed is slow. |
| **RTX 3090 / Ti** | Ampere | 24GB G6X | 936 GB/s | 71 (142 Tensor)| 384-bit | **Best Used Value**. Similar to 4090 capacity at 1/2 price. |
| **RTX 3060** | Ampere | 12GB G6 | 360 GB/s | 13 (51 Tensor) | 192-bit | Entry-level 12GB. Better bandwidth than 4060 Ti 16GB. |
| **RX 9070 XT** | RDNA 4 | 16GB G6 | ~640 GB/s | ~195 (Matrix) | 256-bit | Strong AI math improvements in RDNA 4. ROCm required. |
| **RX 7900 XTX** | RDNA 3 | 24GB G6 | 960 GB/s | 123 | 384-bit | High VRAM alternative to 4090. Requires ROCm/Linux. |
| **Mac M3 Ultra** | Apple Silicon| 64-192GB | 800 GB/s | ~57 | Unified | **Inference Only**. Fits massive models (100B+) locally. Slow training. |

## 3. Quick Resource Estimator

Use these heuristics to determine if a hardware setup is viable.

**Training (Full Fine-Tune, FP16/BF16)**

* Formula: `Model_Params (B) * 16 GB` (Rough upper bound including optimizer states + gradients)
* *Example*: Llama-3-8B -> Requires ~128GB VRAM (Needs A100 80GB x2 or massive offloading).

**Training (LoRA/QLoRA)**

* Formula: `Model_Params (B) * 1.2 GB` (Significant savings)
* *Example*: Llama-3-8B -> Requires ~10-12GB VRAM (Fits on RTX 3060/4070).

**Inference (4-bit Quantization)**

* Formula: `Model_Params (B) * 0.7 GB` + `Context Window Buffer`
* *Example*: Llama-3-70B -> Requires ~48GB VRAM (Fits on 2x RTX 3090/4090 or 1x Mac Studio).
