# CoDeC Score (Contamination Detection via Context) Reference Manual

The CoDeC (Contamination Detection via Context) score is a lightweight diagnostic metric used to detect data contamination in Large Language Models (LLMs). It leverages the mechanics of In-Context Learning (ICL) to identify whether a model has "memorized" a specific evaluation dataset during its training phase.

## 1. Principles and Mathematical Definition

The core logic of CoDeC is based on **Information Gain Disparity**.

### The Mechanism

* **Unseen Data**: When provided with few-shot examples (context) from the same distribution, a model's prediction confidence (Log-Likelihood) for the target sample typically **increases** as the context provides helpful task-specific information.
* **Contaminated Data**: If the model has already memorized the data, the distribution priors and specific sequences are already internalized. In this case, additional context offers no new information and may even interfere with the model's rigid "rote memory" patterns, causing the prediction confidence to **decrease** or stagnate.

### Mathematical Formulation

Let $\text{LL}(x)$ be the log-likelihood of target sample $x$ without context, and $\text{LL}(x|c)$ be the conditional log-likelihood with context $c$.
The confidence delta is $\Delta = \text{LL}(x|c) - \text{LL}(x)$.
The **CoDeC Score** is defined as the fraction of samples in a dataset where the confidence drops after adding context ($\Delta < 0$):

$$ \text{Score} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}(\Delta_i < 0) $$

## 2. Low-Overhead Implementation

CoDeC requires only "gray-box" access (logits output) and does not require access to the original training corpus or additional shadow models.

### Implementation Pattern (Python/PyTorch)

```python
import torch

@torch.no_grad()
def calculate_codec_step(model, tokenizer, target_text, context_text):
    # 1. Baseline Log-Likelihood
    inputs_base = tokenizer(target_text, return_tensors="pt").to(model.device)
    labels_base = inputs_base.input_ids.clone()
    ll_base = -model(**inputs_base, labels=labels_base).loss.item()
    
    # 2. Contextualized Log-Likelihood
    full_prompt = f"{context_text}\n\n{target_text}"
    inputs_ctx = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    
    # Only calculate loss for the target_text portion of the sequence
    outputs_ctx = model(**inputs_ctx)
    logits = outputs_ctx.logits[0, -(inputs_base.input_ids.size(1)+1):-1, :]
    labels = inputs_ctx.input_ids[0, -inputs_base.input_ids.size(1):]
    
    ll_ctx = -torch.nn.functional.cross_entropy(logits, labels).item()
    
    return 1 if (ll_ctx - ll_base) < 0 else 0
```

## 3. Operational Utility Analysis

CoDeC acts as a "lie detector" for model evaluation and generalization audits.

* **Benchmark Auditing**: Verifying if a model "cheated" on test sets (e.g., GSM8K, MMLU). High accuracy paired with a high CoDeC score ($>0.8$) strongly indicates memorization rather than reasoning.
* **Generalization vs. Memorization**: In models with similar accuracy, the one with a lower CoDeC score is considered superior as it relies more on general reasoning (ICL) than on specific data fitting.
* **Leakage Monitoring**: Periodically auditing private validation sets during pre-training to detect early signs of accidental data exposure in the training pipeline.

## 4. Diagnostic Scenarios

| Anomaly Pattern | Numerical Feature | Root Cause | Remediation |
| :--- | :--- | :--- | :--- |
| **High Contamination** | Score $> 80\%$ | **Direct Memorization**: The test data was included verbatim in the training corpus. Context acts as noise to the model's fixed internal sequence. | **Audit Sharding**: Invalidate the benchmark result. Investigate de-duplication logic in the data pipeline. |
| **Partial Leakage** | Score $60\% - 80\%$ | **Indirect Contamination**: The model has not seen the exact test items but was trained on massive amounts of highly similar synthetic data or paraphrases. | **Contextual Analysis**: Compare scores across different models. Increase data diversity to reduce "template fitting." |
| **Healthy / Unseen** | Score $< 50\%$ | **Normal State**: The model has not encountered the data. ICL provides positive information gain, increasing prediction confidence. | **Validation**: Confirms that the model's performance on this task is likely due to generalization. |
| **Adversarial Low** | Score $\approx 0\%$ | **Format Sensitivity**: The test set uses a very specific template that the training set lacked. The context merely provides a "format hint," artificially boosting ICL gains. | **Format Cleaning**: Recalculate the score using raw text without artificial prompt markers to find the true baseline. |

## 5. Summary

For any claim of SOTA (State-of-the-Art) performance on public benchmarks, the **CoDeC Score** should be audited first.

* **Warning**: A high CoDeC score indicates that the model's capabilities may be an illusion created by "reciting" the test set.
* **Ideal Profile**: High benchmark accuracy + Low CoDeC score = Robust Generalization.
