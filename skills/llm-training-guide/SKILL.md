---
name: llm-training-guide
description: Use this skill as a reference-first knowledge base for LLM training strategy, hardware diagnostics, VRAM planning, alignment method selection, and training-health metric interpretation with on-demand document loading.
---

# LLM Training Guide Skill

Use this skill when you need technical background for LLM training decisions, troubleshooting, and evaluation.

## Skill Type

This is a **reference skill**.

- It is not a fixed step-by-step workflow.
- Load only the documents required for the current question.
- Start broad, then zoom into one method or metric as needed.

## Scope

This skill covers:

1. Hardware and runtime environment diagnostics.
2. VRAM estimation and memory trade-off analysis.
3. Training-stage strategy (CPT, SFT, DPO, PPO, GRPO, RLOO).
4. Alignment and reasoning-RL method comparison.
5. Failure diagnosis across environment, data, optimization, and distributed systems.
6. Training health monitoring via advanced metrics.

## Reference Map (Load on Demand)

### Foundation References

- Environment checks and accelerator troubleshooting:
  [references/hardware_environment.md](references/hardware_environment.md)
  - Summary: Hardware detection commands, driver/runtime checks, and common CUDA/ROCm/MPS/TPU/CPU failure diagnostics.
- VRAM formulas, tables, and optimization trade-offs:
  [references/vram_estimation.md](references/vram_estimation.md)
  - Summary: Weight/optimizer/KV/activation memory formulas with practical tables and effects of LoRA, quantization, and ZeRO.
- End-to-end tuning and alignment strategy:
  [references/tuning_and_alignment.md](references/tuning_and_alignment.md)
  - Summary: Stage-level strategy map (CPT → SFT → preference optimization → reasoning RL), method selection logic, and typical dataset scales.
- Unified failure diagnosis playbook:
  [references/troubleshooting.md](references/troubleshooting.md)
  - Summary: Symptom-to-cause-to-fix mappings for crashes, silent failures, data/pipeline defects, and distributed training bugs.

### Method Deep Dives

- SFT:
  [references/methods/sft_guide.md](references/methods/sft_guide.md)
  - Summary: SFT objective, key hyperparameters, packing/padding-free/completion-only-loss techniques, and common failure fixes.
- DPO:
  [references/methods/dpo_guide.md](references/methods/dpo_guide.md)
  - Summary: Preference-pair optimization without separate RM training, with practical guidance on `beta`, LR, and drift control.
- PPO:
  [references/methods/ppo_guide.md](references/methods/ppo_guide.md)
  - Summary: Full RLHF PPO setup (actor/critic/reference/reward), stability controls, and memory/performance architecture patterns.
- GRPO:
  [references/methods/grpo_guide.md](references/methods/grpo_guide.md)
  - Summary: Critic-free group-relative advantage RL for verifiable reasoning tasks, including group-size and rollout bottleneck tuning.
- RLOO:
  [references/methods/rloo_guide.md](references/methods/rloo_guide.md)
  - Summary: Leave-one-out REINFORCE baseline, low-memory RL alignment, and variance/stability trade-offs vs PPO-like methods.

### Metric System

- Monitoring taxonomy and interpretation entry point:
  [references/metrics/guide.md](references/metrics/guide.md)
  - Summary: High-level map of gradient/entropy/weight-structure/loss-consistency metrics and how to combine them diagnostically.
- Individual metric references:
  - [references/metrics/alpha_indicator.md](references/metrics/alpha_indicator.md): Spectral heavy-tail alpha for layer quality, redundancy, and pruning guidance.
  - [references/metrics/attention_head_entropy.md](references/metrics/attention_head_entropy.md): Attention focus spread; detects under-learning vs over-concentration.
  - [references/metrics/codec_score.md](references/metrics/codec_score.md): In-context-learning gain signal; helps spot contamination/memorization behavior.
  - [references/metrics/collapse_residual.md](references/metrics/collapse_residual.md): Deviation from scaling-law trajectory for early structural training failure detection.
  - [references/metrics/gradient_direction_consistency.md](references/metrics/gradient_direction_consistency.md): Cross-worker gradient cosine consistency for distributed sync/data issues.
  - [references/metrics/gradient_norms.md](references/metrics/gradient_norms.md): Global gradient magnitude tracking for explosion/vanishing/oscillation diagnosis.
  - [references/metrics/gradient_signal_to_noise_ratio.md](references/metrics/gradient_signal_to_noise_ratio.md): Effective gradient signal strength, especially useful for deep-layer optimization quality.
  - [references/metrics/gradient_spike_score.md](references/metrics/gradient_spike_score.md): Spike-to-baseline ratio for early warning of divergence and momentum contamination.
  - [references/metrics/layer_wise_weight_std.md](references/metrics/layer_wise_weight_std.md): Layer-level parameter spread evolution for normalization/scaling pathologies.
  - [references/metrics/loss_dispersion.md](references/metrics/loss_dispersion.md): Inter-worker loss variance for silent distributed inconsistency detection.
  - [references/metrics/singular_entropy.md](references/metrics/singular_entropy.md): Singular-value entropy for rank collapse and representational richness checks.
  - [references/metrics/spectral_radius.md](references/metrics/spectral_radius.md): Largest singular value monitoring to control instability in deep stacks.
  - [references/metrics/token_entropy.md](references/metrics/token_entropy.md): Output uncertainty indicator for hallucination risk, collapse, or stalled learning states.
  - [references/metrics/update_to_weight_ratio.md](references/metrics/update_to_weight_ratio.md): Relative update scale ($\|\Delta w\|/\|w\|$) for LR sanity and optimization pacing.
  - [references/metrics/zlib_compression_ratio.md](references/metrics/zlib_compression_ratio.md): Compression/perplexity relation for memorization and privacy-leak risk screening.

## Intent-to-Reference Routing

Use this routing logic to load only relevant context:

- **"Can this machine train/infer this model?"**
  - Load hardware + VRAM references.
  - If there are runtime errors, add troubleshooting.
- **"Which method should I choose for my objective?"**
  - Load tuning/alignment first, then one or more method guides.
- **"Why is training unstable or diverging?"**
  - Load troubleshooting first for fast triage.
  - Then load metrics guide and gradient/loss-focused metric docs for root-cause confirmation.
- **"Why does training crash, hang, or OOM?"**
  - Load troubleshooting + hardware.
  - Add VRAM estimation when memory is part of the failure.
- **"How do I improve reasoning performance efficiently?"**
  - Load tuning/alignment + GRPO/RLOO/PPO references.
- **"How much data do I need at each stage?"**
  - Load tuning/alignment dataset-scale sections.
- **"How do I detect overfitting or memorization?"**
  - Load token entropy, zlib compression ratio, CoDeC score, and collapse residual references.

## Quick Load Bundles

Use these minimal bundles to reduce over-loading:

- **Crash/OOM/Hang Bundle**
  - `references/troubleshooting.md` + `references/hardware_environment.md` (+ `references/vram_estimation.md` if OOM-related).
- **Method Selection Bundle**
  - `references/tuning_and_alignment.md` + one target method doc under `references/methods/`.
- **Instability Diagnosis Bundle**
  - `references/troubleshooting.md` + `references/metrics/guide.md` + two focused metric docs.
- **Memorization/Contamination Bundle**
  - `references/metrics/codec_score.md` + `references/metrics/zlib_compression_ratio.md` + `references/metrics/token_entropy.md`.

## Usage Rules

1. Prefer references over assumptions; cite the loaded file(s) that support each recommendation.
2. When giving numeric guidance, include assumptions (model size, precision, context length, optimizer, batch size).
3. For algorithm comparisons, present resource cost and failure modes, not just expected quality.
4. For anomaly diagnosis, correlate at least two metrics before concluding root cause.
5. If a method is out of resource budget, provide a lower-cost alternative from the method set in this skill.
