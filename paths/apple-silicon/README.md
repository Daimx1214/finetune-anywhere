# Train on Apple Silicon

Prerequisites: an Apple Silicon Mac, a macOS version supported by [MLX](https://github.com/ml-explore/mlx), Python 3.11, Git and free disk. Intel Macs use the [CPU path](../cpu-only/). Plan an afternoon for setup, training and evaluation.

## Choose a size

On 8 GB unified memory start with `tiny`, four-bit base weights, batch 1 and short sequences. On 16 GB start with `starter`. With 32 GB or more, use `larger`. All three are Apache-2.0 text models. macOS, context, activations and other apps share the same memory.

## Install

From the repository root:

```bash
python3.11 -m venv .venv-mlx
source .venv-mlx/bin/activate
python -m pip install -r paths/apple-silicon/requirements.txt
mlx_lm.lora --help
```

## Train, fuse and quantize

The wrapper validates all splits, converts the base to four-bit MLX, trains an adapter, fuses it into the full-precision base and creates a four-bit inference model:

```bash
bash paths/apple-silicon/train_mlx.sh json-extractor starter 100
```

For a small setup check use `bash paths/apple-silicon/train_mlx.sh json-extractor tiny 2`. The shared MLX config sets rank 16, scale 2, seed 42 and regular validation. The wrapper uses eight layers to limit adapter training cost.

## Run natively

```bash
mlx_lm.generate --model outputs/json-extractor/mlx/finetuned-4bit --prompt 'Please order 3 lamps. This is urgent.' --max-tokens 128
mlx_lm.server --model outputs/json-extractor/mlx/finetuned-4bit --host 127.0.0.1 --port 8081
```

Start the unchanged `outputs/json-extractor/mlx/base-4bit` on port 8080 in a second terminal if memory allows. Then run [compare.py](../../guides/04-evaluate.md) with matching system prompts. Run one server at a time or use sequential Ollama loading on smaller machines.

## Ollama and LM Studio

Use [the llama.cpp conversion steps](../../guides/05-quantize.md) with `MERGED=outputs/json-extractor/mlx/merged`. The wrapper saves the non-thinking Qwen3 template. Convert the merged weights with llama.cpp. Once converted, follow the complete [Ollama or LM Studio instructions](../../guides/06-run-locally.md). Evaluate the GGUF again, then [share it](../../guides/07-share-your-model.md).

[Troubleshooting](../../guides/faq.md).
