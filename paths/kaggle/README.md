# Fine-tune on Kaggle

Prerequisites: a Kaggle account, available NVIDIA GPU runtime, internet and a place to save exports. Plan an afternoon; resource availability and training duration vary. [Open the notebook](https://www.kaggle.com/kernels/welcome?src=https://raw.githubusercontent.com/junaiddshaukat/finetune-anywhere/main/paths/kaggle/finetune_unsloth_kaggle.ipynb).

## Setup and training

Create or import a notebook, enable a GPU accelerator and turn Internet on in settings. Account verification or quota availability may affect access. If the import link does not work, download the notebook from this folder and use File > Import Notebook. Outputs go under `/kaggle/working`. Save a version with outputs before ending the session.

Run the notebook cells in order: GPU check, repository clone, pinned dependencies, storage setup, dataset validation, training and GGUF export. Every non-obvious step has an explanation. Restart the session after installation if a previously imported package changed, then rerun the checkout cell.

The default is the `starter` alias from [the registry](../../configs/models.yaml), QLoRA and the JSON extractor recipe. Start with `--max-steps 2` in the training cell for a smoke test. Remove it for the full run. For another recipe change the `--config` path. No token is needed to download the public base model.

## Save and download

Use the Files panel to download the GGUF. Save Version with outputs for persistent notebook artifacts. Optional Hub uploads read HF_TOKEN from Kaggle Secrets, never from a committed cell.

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

[Kaggle notebook documentation](https://www.kaggle.com/docs/notebooks) describe availability. No fixed free GPU quota is promised here.
