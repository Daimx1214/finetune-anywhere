# Fine-tune on Colab

Train a Qwen3 text model, compare real before/after answers and export a local model. You need a Colab account and a GPU runtime. Plan an afternoon for the first run.

[Open the notebook](https://colab.research.google.com/github/junaiddshaukat/finetune-anywhere/blob/main/paths/colab/finetune_unsloth_colab.ipynb).

## Run the notebook

1. Save a copy to Drive. Select Runtime > Change runtime type > T4 GPU and save.
2. Run **Check the GPU**. Confirm the output says Tesla T4.
3. Run **Install Unsloth**. The cell follows Unsloth's recommended Colab installation sequence and displays its logs. If prompted to restart, restart and continue at Settings.
4. In **Settings and recipe**, keep `RECIPE = 'json-extractor'` and `MODEL_ALIAS = 'starter'` for the first run. This selects the Apache-2.0 Qwen3 1.7B text model.
5. Set `SAVE_TO_DRIVE = True` in the optional backup cell to preserve checkpoints in Drive.
6. Run cells **Load the model** through **Download evidence and model**, in order.

The notebook shows model loading, every LoRA setting, the non-thinking chat template, data validation, base answers, training, a test prompt, held-out evaluation, saving and GGUF export. Training uses 40 original examples; 10 validation examples guide the run and 10 held-out examples supply the final comparison.

## Send back real results

Download **`run-evidence.zip`** from the final results cell. It contains:

- `comparison.md`: all held-out prompts and actual base and fine-tuned answers.
- `comparison.json`: the full system/user messages, references and raw answers.
- `run.json`: model, software versions, GPU, settings, data hashes, elapsed training time and export status.
- `training-log.json`: training and validation losses.

Send that ZIP to the maintainer to add real before/after examples. If a cell fails, send its full error output and the section title. Run the evidence cell after an export failure to collect the already-saved training results.

Set `DOWNLOAD_GGUF = True` in the download cell to download the model too, or retrieve it from your Drive output directory.

## Run the exported model locally

Install [Ollama](https://ollama.com/download), start it and save the downloaded GGUF as `outputs/finetuned-q4_k_m.gguf` in your local checkout. Create `outputs/Modelfile`:

```dockerfile
FROM ./finetuned-q4_k_m.gguf
PARAMETER temperature 0
PARAMETER num_ctx 2048
```

```bash
ollama create recipe-local -f outputs/Modelfile
ollama run recipe-local
```

Use the recipe's system instruction when testing the extraction task. See [local inference](../../guides/06-run-locally.md) and [evaluation](../../guides/04-evaluate.md) for API calls and a quantized base-versus-tuned comparison.

## Train on your own data

The last notebook section accepts `train.jsonl`, `valid.jsonl` and `eval.jsonl` in [chat format](../../guides/02-make-a-dataset.md). Turn on `USE_OWN_DATA`, upload all three files, and run validation. Restart the session, rerun Install and Settings, apply the printed data path and `RECIPE = 'my-task'`, then load a fresh base and train again.

[Troubleshooting](../../guides/faq.md) · [Share your model](../../guides/07-share-your-model.md)
