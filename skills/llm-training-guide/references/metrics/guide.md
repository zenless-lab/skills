# LLM Training Health Monitoring Indicators

This document defines key technical indicators for monitoring the health and stability of Large Language Model (LLM) training. These metrics provide insights into the internal dynamics of the model beyond the standard loss curve.

## 1. Gradient Dynamics

Monitors optimization stability and signal quality.

| Metric | Definition / Property | Diagnostic Logic |
| :--- | :--- | :--- |
| **Global Gradient Norm** | $\|\nabla L\|_2$ (L2 norm of all gradients) | **Typical Healthy Pattern**: Stable or slowly decreasing after initial fluctuations.<br>**Anomaly Signal**: Sudden spikes may suggest bad data or numerical overflow; near-zero values may suggest gradient vanishing. |
| **Gradient Spike Score (GSS)** | Ratio of current gradient norm to its moving average | **Heuristic**: Sustained high values (e.g., around or above 2.0 under a given setup) can indicate optimizer-state contamination or instability risk. |
| **Update-to-Weight Ratio** | $\frac{\|\Delta w\|}{\|w\|}$ (Update step vs. weight magnitude) | **Rule of Thumb**: Often near $10^{-3}$ in stable runs.<br>**Anomaly Signal**: Much higher (e.g., $>10^{-2}$) can indicate unstable updates; much lower (e.g., $<10^{-4}$) can indicate slow progress. |
| **Gradient Signal-to-Noise Ratio (GSNR)** | $\frac{\mathbb{E}[g]^2}{Var(g)}$ | **Diagnostic**: Measures effective signal strength. Low GSNR in deeper layers suggests architectural flaws in residual connections or normalization. |
| **Direction Consistency** | Cosine similarity of gradients across workers | **Anomaly**: Low consistency in distributed training indicates unsynchronized seeds, data loading issues, or communication faults. |

## 2. Entropy and Attention Dynamics

Refers to the model's certainty and representational focus.

| Metric | Definition / Property | Diagnostic Logic |
| :--- | :--- | :--- |
| **Attention Head Entropy** | $H(q_i) = -\sum \alpha \log \alpha$ | **Typical Pattern**: Often decreases as the model learns to focus.<br>**Anomaly Signal**: Persistently high entropy may suggest weak focus; extremely low entropy may suggest over-concentration or overfitting. |
| **Singular Entropy** | Entropy of the singular value distribution of weights | **Anomaly**: A sharp decline indicates "Spectral Saturation" or "Rank Collapse," limiting the model's capacity. |
| **Token Entropy** | Shannon entropy of the output probability distribution | **Diagnostic**: High entropy correlates with uncertainty and potential hallucinations. Essential for balancing exploration in RLHF. |

## 3. Weight Structure Evolution

Monitors the topology and capacity utilization of the parameter space.

| Metric | Definition / Property | Diagnostic Logic |
| :--- | :--- | :--- |
| **Alpha Index (HT-SR Alpha)** | Power-law tail index $\alpha$ of the weight matrix spectrum | **Diagnostic**: Smaller $\alpha$ indicates stronger feature correlation and higher layer quality. Used to guide pruning or identify under-trained layers. |
| **Layer-wise Std** | Standard deviation of parameters per layer | **Typical Pattern**: Shallow layers often expand quickly; deep layers often stabilize later.<br>**Anomaly Signal**: Synchronized oscillations across many layers can indicate normalization or optimization issues. |
| **Spectral Radius** | Maximum singular value of the weight matrix | **Diagnostic**: Monitoring is useful for controlling activation growth; combining with $\mu P$-style scaling can improve stability in deep architectures. |

## 4. Loss and Data Consistency

Detects anomalies in loss trajectories and potential data integrity issues.

| Metric | Definition / Property | Diagnostic Logic |
| :--- | :--- | :--- |
| **Collapse Residual** | Deviation of actual loss from the Scaling Law curve | **Early Warning**: Even if loss is decreasing, a high residual suggests poor data quality or sub-optimal hyperparameters. |
| **Loss Dispersion** | Standard deviation of loss across distributed workers | **Anomaly Signal**: Persistently elevated values (relative to baseline) can indicate data-sharding, seed, or system-consistency issues. |
| **CoDeC Score** | Change in loss before and after In-Context Learning (ICL) | **Diagnostic**: Failure of ICL to reduce loss suggests the model has already memorized the data (contamination). |
| **Zlib Compression Ratio** | Zlib entropy vs. Model Perplexity | **Diagnostic**: Used to detect mechanical memorization and mitigate privacy leakage risks. |
