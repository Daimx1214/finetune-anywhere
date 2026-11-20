# No GPU: train in the cloud, run on your laptop

Prerequisites: an 8 GB or larger laptop, disk for a quantized model and access to a cloud notebook. Use [Colab](../colab/) or [Kaggle](../kaggle/) for training instead. Plan an afternoon plus the cloud job's actual duration.

## Train and export

Complete either notebook path, export Q4_K_M and download it. Start with `tiny` or `starter` for an 8 GB laptop. Use `starter` or `larger` with 16 GB RAM. All aliases use Apache 2.0.

## Run with a desktop app

Install [Ollama](https://ollama.com/download). Save your downloaded GGUF as `finetuned-q4_k_m.gguf` in a folder and create `Modelfile` beside it:

```dockerfile
FROM ./finetuned-q4_k_m.gguf
PARAMETER temperature 0
PARAMETER num_ctx 2048
```

Open a terminal in that folder, start Ollama and run:

```bash
ollama create recipe-local -f Modelfile
ollama run recipe-local
```

For a GUI use [LM Studio](https://lmstudio.ai/) and its [local model import](https://lmstudio.ai/docs/app/advanced/import-model).

## Force CPU with llama.cpp

Build llama.cpp with [the shared guide](../../guides/05-quantize.md), then:

```bash
outputs/llama.cpp/build/bin/llama-cli -m outputs/finetuned-q4_k_m.gguf --n-gpu-layers 0 --ctx-size 2048 -cnv
```

If replies are slow, reduce output length and context, and choose a smaller model. Close memory-heavy apps if the system swaps. See the [FAQ](../../guides/faq.md) for inference troubleshooting.

Finish with [held-out evaluation](../../guides/04-evaluate.md) and [sharing](../../guides/07-share-your-model.md). State the exact CPU, RAM, runtime, context and quantization so others can judge portability.
