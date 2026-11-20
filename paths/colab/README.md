# Fine-tune on Colab

Prerequisites: a Colab account, available NVIDIA GPU runtime, internet and a place to save exports. Plan an afternoon; resource availability and training duration vary. [Open the notebook](https://colab.research.google.com/github/junaiddshaukat/finetune-anywhere/blob/main/paths/colab/finetune_unsloth_colab.ipynb).

## Setup and training

Select Runtime > Change runtime type > GPU. A free T4 can be a useful starting GPU when available. Confirm with the notebook’s `nvidia-smi` cell. Mount Drive when prompted so checkpoints survive disconnects.

Run the notebook cells in order: GPU check, repository clone, pinned dependencies, storage setup, dataset validation, training and GGUF export. Every non-obvious step has an explanation. Restart the session after installation if a previously imported package changed, then rerun the checkout cell.

The default is the `starter` alias from [the registry](../../configs/models.yaml), QLoRA and the JSON extractor recipe. Start with `--max-steps 2` in the training cell for a smoke test. Remove it for the full run. For another recipe change the `--config` path. No token is needed to download the public base model.

## Save and download

Checkpoints and model artifacts are written to your mounted Drive. The final cell downloads the GGUF. Large browser downloads can fail; download from Drive instead or upload to a model hub.

Do not end the session until you have verified your download or Hub upload. The adapter alone is not the merged portable model.

## Run on your laptop

Save the download as `outputs/finetuned-q4_k_m.gguf` in your local checkout. Install [Ollama](https://ollama.com/download), start it and create `outputs/Modelfile`:

```dockerfile
FROM ./finetuned-q4_k_m.gguf
PARAMETER temperature 0
PARAMETER num_ctx 2048
```

```bash
ollama create recipe-local -f outputs/Modelfile
ollama run recipe-local
```

[Compare with the base](../../guides/04-evaluate.md), then [share the actual results](../../guides/07-share-your-model.md). [Other local runtimes](../../guides/06-run-locally.md) work too.

## Common errors

No GPU: change runtime settings or wait for capacity; CPU fallback is not a practical training substitute. OOM: choose `tiny` and shorten sequence length. Disconnect: resume from a saved checkpoint with the same settings. GGUF build failure: retain merged weights and use [the manual converter](../../guides/05-quantize.md). Dependency installation failure: check the pinned Python/platform assumptions and [validation status](../../MAINTAINER_NOTES.md).

[Colab resource limits](https://research.google.com/colaboratory/faq.html) describe availability. No fixed free GPU quota is promised here.
