# Frequently asked questions

## I have no GPU

Train in [Colab](../paths/colab/) or [Kaggle](../paths/kaggle/), then run a quantized model on CPU. CPU training is very slow and useful mainly for tiny experiments.

## Colab disconnected

Write checkpoints to Drive, then resume the same training run with `--resume` and its checkpoint path. A session's temporary files may disappear. Free resources are not guaranteed; see [Colab's FAQ](https://research.google.com/colaboratory/faq.html).

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

Next: [Glossary](glossary.md).
