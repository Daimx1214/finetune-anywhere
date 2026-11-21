# Extract a purchase request as JSON

Fine-tune the `starter` Qwen3 1.7B text model to learn this task's output format and response style. Exact IDs and Apache-2.0 license information are in [the registry](../../configs/models.yaml).

## Dataset

Requests include quantities in words, corrected orders, packaging units, cancellations, missing fields, delivery urgency and quoted instructions. Missing item or quantity is null; quantity zero represents an explicit cancellation.

All 60 scenarios are original, individually authored synthetic examples released under the repository's MIT license. They contain no scraped customer records or copied repository code. The splits contain **40 training, 10 validation and 10 evaluation examples**, authored separately rather than expanded by replacing identifiers. [Data manifest](data/manifest.json).

## Train

For a visible walkthrough, open [Colab](../../paths/colab/) or [Kaggle](../../paths/kaggle/) and set `RECIPE = 'json-extractor'` in Settings. The notebook records measured training time, hardware and actual before/after outputs in `run-evidence.zip`.

On [NVIDIA](../../paths/nvidia-gpu/), run from the repository root:

```bash
python scripts/validate_dataset.py recipes/json-extractor/data/train.jsonl recipes/json-extractor/data/valid.jsonl recipes/json-extractor/data/eval.jsonl
python paths/nvidia-gpu/train_unsloth.py --config recipes/json-extractor/config.yaml --export-gguf
```

On [Apple Silicon](../../paths/apple-silicon/):

```bash
bash paths/apple-silicon/train_mlx.sh json-extractor starter 100
```

The configuration uses rank 16, alpha 32, learning rate 0.0002 and three epochs on the GPU. The paths preserve Qwen3 non-thinking mode. Keep the dataset's system instruction during inference.

## Evaluate

Parse the output and compare the exact keys, types and values. An absent quantity must stay null, and a delivery date alone does not imply urgency.

Use [held-out evaluation](../../guides/04-evaluate.md), then [run locally](../../guides/06-run-locally.md). Report every evaluation example, including failures, and test the exported quantization too.

## Recorded Colab result

On the maintainer's Tesla T4 run, exact matches on the ten held-out examples rose from **2/10 to 7/10**, and directly parseable JSON rose from **8/10 to 10/10**. Training took **80.14 seconds** with **4.51 GB peak allocated GPU memory**. [Read the measured run, actual before/after answers and all three remaining errors](results/2026-11-21-t4/).
