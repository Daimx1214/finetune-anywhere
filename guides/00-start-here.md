# Start here

Fine-tuning updates a model using examples of the behavior you want. It is useful for a repeated style, output format or narrow task. Try a good prompt first. If the problem is changing facts, use retrieval to put current documents in the prompt. Fine-tuning is not a reliable database.

**LoRA** freezes the original weights and trains small extra matrices, called adapters. This makes experiments cheaper and keeps the result small. An adapter still needs its exact base model.

**QLoRA** keeps that base in a low-bit representation while training the adapter. This reduces base-weight memory. It does not remove the memory needed for training activations.

**Quantization** stores weights with fewer bits. It reduces disk and memory use and can affect quality. A training-time 4-bit model is not automatically a portable GGUF file. Evaluate the final format you plan to run.

## What you need

| Path | Requirements |
| --- | --- |
| Colab or Kaggle | Account, available GPU runtime, internet, backup storage |
| NVIDIA | Supported CUDA GPU/driver, Python 3.11, Linux or WSL2 |
| Mac | Apple Silicon, supported macOS for MLX, Python 3.11, free memory |
| CPU | RAM and disk for a quantized model; cloud account for training |
| Cloud GPU | Provider account, budget, SSH/Jupyter access, persistent output storage |

Choose your [hardware path](../README.md#pick-your-path). Every command in the guides assumes you are in the repository root and have activated that path's environment. Windows training commands run in Ubuntu under WSL2, not PowerShell.

```bash
git clone https://github.com/junaiddshaukat/finetune-anywhere.git
cd finetune-anywhere
```

Start with the JSON extractor recipe. Get one small complete run working before increasing the model, dataset or context. Keep the base model for comparison. Write down hardware, software versions, model revision, training time and failures.

Next: [Pick a model](01-pick-a-model.md).
