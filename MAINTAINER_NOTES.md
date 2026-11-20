# Maintainer notes

## Validation status

Checked on 20 November 2026. Distinguish runnable source, dependency resolution, CLI checks and completed training.

| Area | Evidence | Remaining check |
| --- | --- | --- |
| Utility scripts | 25 local automated tests cover data, conversion, memory, HTTP comparison, schema, deadline and generated tables | Expand tests with real community submissions |
| Recipe data | 100 train, 12 validation and 12 evaluation examples per recipe; structural and leakage checks; actual tokenizer counts checked for the default recipe (71 to 79 tokens) | Independent human review and more diverse real task data |
| Notebooks | Valid notebook structure, Python cells parse, no outputs or execution counts | Execute Colab and Kaggle notebooks in fresh GPU sessions |
| NVIDIA stack | Exact dependency pins resolved for Linux x86_64, Python 3.11; CUDA 12.8 Torch selected | Run on a T4 and a local NVIDIA GPU; record driver and peak VRAM |
| MLX stack | Installed on Apple M4; lora, fuse and convert CLI options checked | Training stopped before loading weights because disk had less than 1 GB free; complete train, fuse, quantize and inference with adequate disk |
| Alternative trainers | Official configuration/API references checked; tool releases verified | Install and run each config on supported hardware |
| Model hubs | HF and ModelScope CLI help checked; ModelScope Python method signatures inspected | Upload a real trained artifact to both hubs |
| Showcase | Temporary test fixtures exercise success, readable failures, late status and all table locations | Exercise a real submission PR after model training; do not publish fictional results |
| GitHub Actions | Workflow source and trust boundaries reviewed; tests run in CI after publication | Verify an actual fork PR, artifact comment update and labels |

No completed fine-tuning run, quality gain, GPU memory benchmark or latency result is claimed. A successful environment resolver is not evidence that training kernels work. Pins are a reproducible candidate stack, not a hardware-tested promise. Promote each path's status only after its full training-to-inference run succeeds.

## Decisions where the spec was silent

- Use Python 3.11 across training and contributor tooling. Utilities use the standard library except YAML/schema handling and optional tokenizer-based counting.
- Use established Qwen2.5 instruction models rather than a moving latest-model default. Exact IDs, parameter counts and licenses live in the registry. The smallest model is for smoke tests; the middle model is the default. The larger model has a different license, explicitly called out.
- All guide commands start from the repository root. Windows GPU training uses WSL2. Keep each trainer in its own environment.
- The four recipe datasets are original rule-generated teaching data. Their structures and target rules were checked during authoring. They are MIT-licensed, intentionally repetitive and not real-world benchmarks. Evaluation entities are disjoint but templates overlap.
- Add a validation split separate from the final evaluation set. The trainer never loads evaluation data for fitting or hyperparameter selection.
- Training uses full-conversation loss. Assistant-only loss is not enabled without verifying model-specific template masks.
- MLX defaults to eight adapter layers and 100 iterations. Scale 2 with rank 16 corresponds to the alpha/rank ratio used by the GPU recipe, but iterations, layers and optimizer behavior do not make the runs equivalent.
- MLX fusion reloads the full-precision base instead of fusing and dequantizing a lossy base. Conversion to GGUF goes through llama.cpp because the built-in MLX exporter has architecture restrictions.
- CPU float32 merging is portable but may need substantial RAM. It is a separate operation from low-memory training.
- Memory numbers are decimal GB. The calculator exposes KV architecture assumptions. Its training budget is a labelled heuristic, not a measured architecture-specific activation calculation.
- compare.py uses local OpenAI-compatible servers so it works across hardware without installing two model stacks. It saves actual text and raw JSON. Unit tests use a clearly isolated mock HTTP server, not a published model example.
- No claimed quality outputs or hero GIF are included without a real run.
- Model IDs are centralized for first-party workflows. User showcase entries and externally uploaded model cards must identify their actual base model and are the necessary exception to the registry-only rule.
- The required submission template is intentionally a blank form. It is skipped by gallery discovery and fails validation until completed. There are no fictional gallery entries.
- Future event names are accepted only with an existing event README and a matching folder. Enum restrictions apply to the training tool, platform, method and runtime fields.
- The deadline's closing minute is inclusive. Late means PR creation at or after 2026-11-28T19:00:00Z. Edits do not change the creation timestamp.
- Newest gallery entries are ordered by their most recent manifest commit timestamp, then path for deterministic ties. Uncommitted test entries use timestamp zero. No participant tracking is added.
- Internal Markdown links are blocking checks. External links are checked in CI but transient network/auth failures are warnings. Notebook badges include a manual import fallback where needed.
- The trusted showcase validator comes from the PR base commit. Submission files are data only. The write-enabled comment workflow never checks out code, constrains archive extraction and text lengths, validates PR/run association and derives labels from GitHub metadata rather than artifact claims.
- Automatic table updates use the GitHub Actions bot identity in CI only. Local commits use the maintainer's default Git account. Main-branch rules must permit the intended bot update strategy or the workflow needs to open update PRs instead.
- CODE_OF_CONDUCT.md uses Contributor Covenant 2.1 with the maintainer's supplied account email for private reports and punctuation normalized to this repository's writing rule.

## Verified sources

Model cards were fetched directly from the official Hugging Face repositories named in configs/models.yaml. Recorded total parameters: 0.49B, 1.54B and 3.09B. The first two cards specify Apache-2.0; the third specifies its Qwen Research License. Open the registry ID on Hugging Face to inspect the current license and model revision.

- [Unsloth source and installation](https://github.com/unslothai/unsloth), with package metadata checked for the pinned release.
- [MLX LoRA guide](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md), plus installed CLI help and adapter configuration source.
- [LLaMA-Factory training example](https://github.com/hiyouga/LLaMA-Factory/blob/main/examples/train_lora/qwen3_lora_sft.yaml) and [dataset mappings](https://github.com/hiyouga/LLaMA-Factory/blob/main/data/README.md).
- [ms-swift quick start](https://github.com/modelscope/ms-swift), including current tuner flags and custom data references.
- [Axolotl conversation data](https://github.com/axolotl-ai-cloud/axolotl/blob/main/docs/dataset-formats/conversation.qmd) and [QLoRA configuration](https://github.com/axolotl-ai-cloud/axolotl/blob/main/examples/qwen3/32b-qlora.yaml).
- [TRL SFTConfig source](https://github.com/huggingface/trl/blob/v1.15.0/trl/trainer/sft_config.py) and [SFTTrainer source](https://github.com/huggingface/trl/blob/v1.15.0/trl/trainer/sft_trainer.py).
- [llama.cpp converter](https://github.com/ggml-org/llama.cpp/blob/master/convert_hf_to_gguf.py) and [Ollama import documentation](https://docs.ollama.com/import).
- [ModelScope SDK](https://github.com/modelscope/modelscope); installed CLI and Python signatures checked for version 1.40.3.
- [Colab FAQ](https://research.google.com/colaboratory/faq.html) and [Kaggle notebook documentation](https://www.kaggle.com/docs/notebooks). No fixed quota is stated.
- Provider references are linked in the cloud guide. No prices or guaranteed availability are claimed.

## Unverified or deliberately omitted

- AMD training folder: omitted because no end-to-end ROCm training setup was validated on available hardware. This does not mean AMD cannot train models.
- Full Modal deployment: the architecture is described with the official GPU guide, but an untested provider-specific app is not presented as working code.
- Remote notebook opening, authentication and GPU allocation require the user's platform accounts. Badge URLs target the published repository; they do not prove a notebook executed successfully.
- AWQ/GPTQ commands are omitted because hardware, model and serving-version compatibility must be checked for a specific deployment.
- Guaranteed times, measured speeds, free GPU quotas, costs and claims of universal compatibility are omitted.

## Real-run backlog

Run each recipe on at least one complete training-to-local-inference path and add only actual outputs:

- Run commit-message-writer and add real before/after outputs, elapsed time and failures.
- Run json-extractor and add real outputs, field-level accuracy and parseability counts.
- Run sql-generator and add real outputs with SQLite result-equivalence checks.
- Run support-bot-from-docs and add grounded-answer and abstention results.
- Repeat evaluation after GGUF or MLX quantization. Include hardware, software versions, revision and context length.
- Record a terminal GIF of a fine-tuned model running in Ollama.

## Repository administration

- Enable Discussions and create Q&A, Show and tell, and Ideas categories.
- Set the repository description to the one-line pitch.
- Add topics: fine-tuning, llm, qwen, lora, qlora, unsloth, mlx, llama-factory, gguf, ollama, llama-cpp, local-llm, colab, kaggle, hackathon.
- Upload a social preview image. No fabricated demo screenshot is supplied.
- Install the all-contributors app and add people manually after merging.
- Protect main and require repository checks. Require showcase validation for showcase submissions. A path-filtered validate workflow cannot be a universal required check without leaving unrelated PRs pending; use conditional rules or change the workflow to always run a no-op job outside showcase changes.
- Create labels: showcase, hackathon-2026, community and late.
- Decide whether table-update bot pushes bypass protection or should become PRs.
- Run a real valid and a deliberately broken submission through a fork PR, verify comments update in place, and check late labels with a controlled test of the timestamp logic.
- Record the hero GIF and replace the README's event block with actual winners after results are supplied.
