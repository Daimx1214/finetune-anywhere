# Frequently asked questions

## I have no GPU

Train in [Colab](../paths/colab/) or [Kaggle](../paths/kaggle/), then run a quantized model on CPU. CPU training is very slow and useful mainly for tiny experiments.

## Colab disconnected

Write checkpoints to Drive, then pass the saved checkpoint directory as `resume_from_checkpoint` to the notebook's `trainer.train` call. The NVIDIA script accepts `--resume`. A session's temporary files may disappear. Free resources are not guaranteed; see [Colab's FAQ](https://research.google.com/colaboratory/faq.html).

## How many GPU hours does Kaggle give me?

Check your account's current quota and [Kaggle documentation](https://www.kaggle.com/docs/notebooks). Limits and availability can change. Save a notebook version with outputs before ending the session. This repository does not promise a quota.

## Out of memory

Reduce sequence length, use microbatch 1, enable checkpointing, then choose a smaller model. Gradient accumulation changes effective batch, not the memory of a single example. Close other applications on a unified-memory Mac. A fitting weight file does not imply a fitting training run.

## The model repeats itself

Check the chat template, end-of-turn token, duplicated training targets and generation budget. Compare the same prompt on the base. Overtraining on repetitive examples can make this worse.

## The model ignores the fine-tune

Check that the adapter was loaded or correctly merged with the exact base. Use the same system prompt and chat template as training. Test in the training framework before blaming quantization.

## Loss is not dropping

Inspect actual tokenized examples, assistant targets, learning rate and trainable parameter count. A wrong template or masking configuration can remove useful supervision. A tiny loss on repeated examples may still mean poor generalization.

## Windows installation fails

Use [the WSL2 path](../paths/nvidia-gpu/). Run Linux commands in Ubuntu, store the repo in the Linux filesystem and verify `nvidia-smi` inside WSL. Do not combine Windows Python with Linux packages.

## Ollama cannot load the GGUF

Confirm it is a complete GGUF, not an adapter or bitsandbytes file. Update the runtime, verify architecture support and inspect `ollama show recipe-local --modelfile`. Retry the GGUF in llama.cpp. Export again from merged weights if necessary.

## Can I publish the model under MIT?

The code and authored sample data here are MIT. Base model and upstream dataset terms still apply. Read the registry's license field and the original model card.


## Which claims have been tested?

[Maintainer notes](../MAINTAINER_NOTES.md) distinguish local checks from completed GPU training. The cloud notebooks follow the verified Unsloth install procedure, but a complete T4 training/export run has not yet been supplied for this revision. Send the notebook's `run-evidence.zip` to record actual results. Do not infer a quality improvement from successful installation or a falling loss alone.

## Are the path times and memory sizes guaranteed?

An afternoon is a planning allowance, not a measured training duration. GPU availability, download speed, context and dataset size affect the run. The tables show approximate weights only, using rounded model-card parameter counts. Training activations, KV cache, the runtime and the OS also use memory. Mac size recommendations are starting points, and CPU training is slow.

## Why not select Qwen3.5 in these notebooks?

The reviewed small Qwen3.5 models are multimodal. This starter selects text-only Qwen3 models to keep one architecture across the Unsloth, MLX-LM and llama.cpp paths. Catalog availability does not establish text-only training, fusion and export compatibility across all three tools. The model review is recorded in maintainer notes.

## Why did a model return a thinking block?

Use the tokenizer saved by the training path. It fixes Qwen3's `enable_thinking` mode to false. Keep the same prefix for the base control model by running `python scripts/configure_chat.py outputs/base-hf` before exporting it. A runtime may supply its own template; inspect it and select non-thinking mode there too. Do not strip arbitrary parts of answers to make an evaluation look better.

## What if a notebook install or GGUF export fails?

Keep the complete failing cell output and its section title. The notebook uses Unsloth's recommended platform install sequence, not the Linux environment lockfile. If an imported library changes, restart the session before loading the model. GGUF export needs a compiler, extra disk and memory. The notebook saves adapters and comparison evidence before export; run Download evidence even after export failure.

## What does the small recipe evaluation establish?

Each recipe has 60 original, individually authored synthetic examples. The 10 held-out scenarios are separate from training and validation, but are not a broad real-world benchmark. Review the targets for your domain, expand training coverage and add an independently collected test set before deploying. Training on the supplied examples does not guarantee correct SQL, faithful support answers or valid JSON.

## Does restarting MLX restore the optimizer?

MLX's adapter resume loads adapter weights. Do not assume it restores optimizer state. Preserve previous outputs before rerunning the wrapper, which uses fixed paths. For a Metal allocation failure, close other applications, reduce sequence length and select `tiny`.

## Is a ready-made Modal deployment included?

No provider-specific Modal app has been validated here. The cloud guide links its official GPU workflow. Use one of the VM-style providers for the shared terminal commands. A disconnected SSH session or browser does not stop a billed instance; stop the resource and inspect persistent storage charges in the provider dashboard.

Next: [Glossary](glossary.md).
