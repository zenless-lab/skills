# Accelerate Example Zoo Reference

A categorized guide to official scripts and community integrations showcasing `accelerate` capabilities. Use this to find implementation patterns for specific tasks.

## 1. Official Core Examples

Basic boilerplates for starting new projects.

* **NLP:** [Barebones Script](https://github.com/huggingface/accelerate/blob/main/examples/nlp_example.py) | [Jupyter Notebook](https://github.com/huggingface/notebooks/blob/main/examples/accelerate_examples/simple_nlp_example.ipynb)
* **Computer Vision:** [Barebones Script](https://github.com/huggingface/accelerate/blob/main/examples/cv_example.py) | [Jupyter Notebook](https://github.com/huggingface/notebooks/blob/main/examples/accelerate_examples/simple_cv_example.ipynb)
* **Platform Specific:** [Multi-GPU on Kaggle](https://www.kaggle.com/code/muellerzr/multi-gpu-and-accelerate)

## 2. Feature-Specific Implementations

Targeted scripts for advanced distributed training techniques.

| Feature | Example Link |
| :--- | :--- |
| **FSDP** | [FSDP with Peak Memory Tracking](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/fsdp_with_peak_mem_tracking.py) |
| **DeepSpeed** | [DeepSpeed with Config Support](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/deepspeed_with_config_support.py) |
| **Megatron-LM** | [GPT Pretraining](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/megatron_lm_gpt_pretraining.py) |
| **Gradient Accumulation** | [Basic](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/gradient_accumulation.py) \| [Automatic (Memory-Aware)](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/automatic_gradient_accumulation.py) |
| **Memory Tools** | [Batch Size Finder](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/memory.py) |
| **Ops & Metrics** | [Checkpointing](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/checkpointing.py) \| [Tracking](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/tracking.py) \| [Distributed Metrics](https://github.com/huggingface/accelerate/blob/main/examples/by_feature/multi_process_metrics.py) |

## 3. Full Fine-Tuning Templates (No-Trainer)

Complete implementations for various `transformers` tasks using raw PyTorch + Accelerate.

* **Language Modeling:** [Causal LM (run_clm)](https://github.com/huggingface/transformers/blob/main/examples/pytorch/language-modeling/run_clm_no_trainer.py) \| [Masked LM (run_mlm)](https://github.com/huggingface/transformers/blob/main/examples/pytorch/language-modeling/run_mlm_no_trainer.py)
* **Question Answering:** [Standard QA](https://github.com/huggingface/transformers/blob/main/examples/pytorch/question-answering/run_qa_no_trainer.py) \| [Beam Search](https://github.com/huggingface/transformers/blob/main/examples/pytorch/question-answering/run_qa_beam_search_no_trainer.py)
* **Generative:** [Translation](https://github.com/huggingface/transformers/blob/main/examples/pytorch/translation/run_translation_no_trainer.py) \| [Summarization](https://github.com/huggingface/transformers/blob/main/examples/pytorch/summarization/run_summarization_no_trainer.py)
* **Classification:** [Text (GLUE)](https://github.com/huggingface/transformers/blob/main/examples/pytorch/text-classification/run_glue_no_trainer.py) \| [Image Classification](https://github.com/huggingface/transformers/blob/main/examples/pytorch/image-classification/run_image_classification_no_trainer.py)
* **Specialized:** [NER/Token Class](https://github.com/huggingface/transformers/blob/main/examples/pytorch/token-classification/run_ner_no_trainer.py) \| [Speech Pretraining](https://github.com/huggingface/transformers/blob/main/examples/pytorch/speech-pretraining/run_wav2vec2_pretraining_no_trainer.py) \| [Semantic Segmentation](https://github.com/huggingface/transformers/blob/main/examples/pytorch/semantic-segmentation/run_semantic_segmentation_no_trainer.py)

## 4. Ecosystem & Third-Party Integrations

How other libraries utilize Accelerate under the hood.

* **Generative AI:** [Diffusers (DreamBooth/Textual Inversion)](https://github.com/huggingface/diffusers/tree/main/examples) \| [DALLE2-pytorch](https://github.com/lucidrains/DALLE2-pytorch) \| [Imagen-pytorch](https://github.com/lucidrains/imagen-pytorch)
* **Audio/Speech:** [Amphion (TTS/SVC/Vocoder)](https://github.com/open-mmlab/Amphion)
* **3D & Vision:** [Stable-Dreamfusion (Text-to-3D)](https://colab.research.google.com/drive/1MXT3yfOFvO0ooKEfiUUvTKwUkrrlCHpF) \| [Kornia (Vision Trainer)](https://kornia.readthedocs.io/en/latest/get-started/training.html) \| [PyTorch3D](https://pytorch3d.org/tutorials/)
* **High-Level Wrappers:** [fastai](https://docs.fast.ai/tutorial.distributed.html) \| [Catalyst](https://catalyst-team.github.io/catalyst/tutorials/ddp.html) \| [PyTorch Accelerated](https://pytorch-accelerated.readthedocs.io/en/latest/quickstart.html)
* **UI/Deployment:** [ComfyUI (Low-VRAM optimization)](https://github.com/comfyanonymous/ComfyUI/blob/master/comfy/model_management.py)

## 5. Research Case Studies

Selected papers utilizing Accelerate for high-performance scaling.

* **Efficiency:** [High-throughput Gen-Inference with Single GPU (2303.06865)](http://huggingface.co/papers/2303.06865)
* **Reasoning:** [Plan-and-Solve Prompting (2305.04091)](http://huggingface.co/papers/2305.04091)
* **Multi-Modal:** [Instruct-NeRF2NeRF (2303.12789)](http://huggingface.co/papers/2303.12789) \| [HuggingGPT (2303.17580)](http://huggingface.co/papers/2303.17580)

## 6. Local Skill Assets (PEP 723 Scripts)

These scripts are local runnable templates placed in `assets/` for agents to load directly after this skill is activated.

* **Gradient Accumulation:** [gradient_accumulation_basic.py](assets/gradient_accumulation_basic.py) — Minimal training loop using `accelerator.accumulate(model)`.
* **Distributed Training Modes:** [distributed_training_patterns.py](assets/distributed_training_patterns.py) — Baseline/DDP hook/FSDP initialization scaffold.
* **Distributed Inference Split:** [distributed_inference_split.py](assets/distributed_inference_split.py) — `split_between_processes` prompt partitioning template.
* **Big Model Inference:** [big_model_inference_dispatch.py](assets/big_model_inference_dispatch.py) — `init_empty_weights` + `load_checkpoint_and_dispatch` template.
* **DeepSpeed Bootstrap:** [deepspeed_training_template.py](assets/deepspeed_training_template.py) — DeepSpeed config parsing and accelerator bootstrap.
* **Megatron-LM Launch Planning:** [megatron_lm_pretraining_template.py](assets/megatron_lm_pretraining_template.py) — TP/PP planning and launch command generation.
* **FP8 Mixed Precision:** [fp8_mixed_precision_template.py](assets/fp8_mixed_precision_template.py) — FP8 backend handler selection template.
* **Troubleshooting Helpers:** [troubleshooting_debug_tools.py](assets/troubleshooting_debug_tools.py) — synchronized logging and OOM auto batch-size fallback.
* **Complete NLP (MRPC):** [complete_nlp_mrpc_example.py](assets/complete_nlp_mrpc_example.py) — integrated NLP training loop inspired by `examples/nlp_example.py` + `examples/complete_nlp_example.py`.
* **Complete CV (Classification):** [complete_cv_classification_example.py](assets/complete_cv_classification_example.py) — integrated CV training loop inspired by `examples/cv_example.py` + `examples/complete_cv_example.py`.
* **Causal LM No-Trainer Style:** [nlp_causal_lm_no_trainer_template.py](assets/nlp_causal_lm_no_trainer_template.py) — no-trainer style LM template inspired by `run_clm_no_trainer.py` and Accelerate launch patterns.
