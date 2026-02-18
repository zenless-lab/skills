# Supervised Fine-Tuning (SFT) Technical Guide

This guide details the core concepts, critical hyperparameter selection, training efficiency optimization techniques, and common troubleshooting methods for Supervised Fine-Tuning (SFT).

## 1. Purpose and Principles

SFT is the critical step of transforming a pre-trained Large Language Model (LLM) into an "assistant" model capable of following instructions and adhering to specific formats.

* **Core Objectives**:
  * **Instruction Following**: Activates the model's ability to understand and execute user intents.
  * **Format Alignment**: Standardizes output formats (e.g., JSON, Markdown, specific coding styles).
  * **Style Transfer**: Adjusts the model's tone and persona.
* **Working Principle**:
  * Based on the Causal Language Modeling (CLM) objective.
  * Given input sequence $X$ (Prompt) and target sequence $Y$ (Response), maximize the likelihood $P(Y|X)$.
  * **Key Difference**: Unlike pre-training, SFT typically employs **Data Masking** (Completion-Only Loss), calculating loss only on the Response part while ignoring the Prompt part to prevent the model from overfitting to the instruction distribution or forgetting pre-trained knowledge.

## 2. Key Hyperparameter Guidelines

SFT is sensitive to hyperparameters. Below are recommended ranges based on empirical evidence:

| Hyperparameter | Recommended Range/Value | Notes |
| :--- | :--- | :--- |
| **Learning Rate (LR)** | 5e-6 ~ 5e-5 | Typically 1-2 orders of magnitude smaller than pre-training. LoRA allows slightly larger values (1e-4 ~ 3e-4). Use Warmup + Cosine Decay. |
| **Epochs** | 1 ~ 3 | SFT datasets are usually smaller and higher quality; excessive epochs lead to overfitting. |
| **Batch Size** | 64 ~ 512 | Larger batch sizes help stabilize gradients. Use Gradient Accumulation if VRAM is limited. |
| **Max Sequence Length** | 2048 ~ 8192 | Should cover >95% of data. Truncating too short destroys semantics; too long wastes compute (unless Packing is used). |
| **Weight Decay** | 0.01 ~ 0.1 | Prevents overfitting, usually paired with AdamW optimizer. |

## 3. Training Efficiency Optimization

In large-scale SFT, data processing and computational efficiency are crucial. Three mainstream techniques include:

### 3.1 Sequence Packing (Sample Packing)

* **Principle**: Concatenates multiple short examples into a single sequence to fill the `max_seq_length` buffer. For instance, three samples of length 1000 are combined into one input of length 3000.
* **Advantages**:
  * **Eliminates Padding**: Traditional padding wastes compute on invalid `[PAD]` tokens. Packing achieves near 100% token utilization.
  * **Throughput**: Significantly increases GPU compute density, often speeding up training by >2x.
* **Requirements**:
  * **Attention Masking**: Must use Block Diagonal Masking (or modified attention kernels) to prevent attention leakage between different samples within the same sequence.
  * **EOS Token**: Explicit `EOS` tokens are required to separate samples.

### 3.2 Padding-Free (Variable Length Processing)

* **Principle**: Processes variable-length sequences directly without padding to a fixed length. Leverages kernels like FlashAttention that support `cu_seqlens` (cumulative sequence lengths) to compute attention only on valid tokens.
* **Advantages**:
  * **Memory Optimal**: Zero VRAM wasted on padding tokens.
  * **Precision**: Avoids potential edge-case truncation issues seen in simplistic packing implementations.
* **Comparison**: Packing "assembles" data into fixed lengths; Padding-Free adapts operators to variable lengths. Both solve the padding waste problem. Modern frameworks (Unsloth, Axolotl) often default to one of these.

### 3.3 Completion-Only Loss (Data Masking)

* **Principle**: Masks the tokens corresponding to the Prompt/Instruction (usually setting labels to -100) during Cross-Entropy Loss calculation.
* **Advantages**:
  * **Task Focus**: Forces the model to learn "how to answer" rather than "how to ask".
  * **Prevents Degeneration**: Reduces the tendency for the model to merely repeat user inputs or memorize instruction templates.
* **Implementation Snippet**:

    ```python
    # Logic illustration
    labels = inputs.clone()
    prompt_len = len(tokenizer(prompt))
    labels[:, :prompt_len] = -100 # Mask the prompt part
    ```

## 4. Troubleshooting

| Symptom | Possible Cause | Solution |
| :--- | :--- | :--- |
| **Loss Not Decreasing** | LR too high/low; Data format error | Check LR Scheduler; **Verify Data Masking hasn't masked the entire sequence**; Validate tokenization. |
| **Val Loss Increasing (Overfitting)** | Too many epochs; Duplicate data | Reduce Epochs (1-2 is often enough); Increase Dropout; Improve dataset diversity. |
| **Repetitive Output (Loops)** | Missing EOS Token | Ensure training data ends with `EOS` token; Check inference `repetition_penalty`. |
| **Catastrophic Forgetting** | LR too high; Narrow data distribution | Lower LR; Mix in a small portion of general pre-training data (Replay Buffer). |
| **Empty or Gibberish Output** | Template mismatch | Strictly verify Chat Template (e.g., ChatML, Alpaca) matches the base model; Check Special Token handling. |
| **Refusal / Safety Overkill** | Excessive safety alignment | Check ratio of refusal samples in dataset; Balance "Helpful" vs "Harmless" data. |

## 5. Data Strategy

* **Quality > Quantity**: 1k - 10k high-quality, diverse samples often outperform 100k+ low-quality ones.
* **Diversity**: Ensure coverage of reasoning, coding, creative writing, and role-playing tasks.
* **De-duplication**: Strict semantic de-duplication is necessary to prevent rote memorization.
