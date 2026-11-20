# Write read-only SQLite queries

Fine-tune the `starter` Qwen3 1.7B text model to learn this task's output format and response style. Exact IDs and Apache-2.0 license information are in [the registry](../../configs/models.yaml).

## Dataset

Questions cover filtering, nulls, joins, empty groups, aggregates, HAVING, distinct counts, sorting, tie-breaks and date boundaries. Each example supplies its own schema.

All 60 scenarios are original, individually authored synthetic examples released under the repository's MIT license. They contain no scraped customer records or copied repository code. The splits contain **40 training, 10 validation and 10 evaluation examples**, authored separately rather than expanded by replacing identifiers. [Data manifest](data/manifest.json).

## Train

For a visible walkthrough, open [Colab](../../paths/colab/) or [Kaggle](../../paths/kaggle/) and set `RECIPE = 'sql-generator'` in Settings. The notebook records measured training time, hardware and actual before/after outputs in `run-evidence.zip`.

On [NVIDIA](../../paths/nvidia-gpu/), run from the repository root:

```bash
python scripts/validate_dataset.py recipes/sql-generator/data/train.jsonl recipes/sql-generator/data/valid.jsonl recipes/sql-generator/data/eval.jsonl
python paths/nvidia-gpu/train_unsloth.py --config recipes/sql-generator/config.yaml --export-gguf
```

On [Apple Silicon](../../paths/apple-silicon/):

```bash
bash paths/apple-silicon/train_mlx.sh sql-generator starter 100
```

The configuration uses rank 16, alpha 32, learning rate 0.0002 and three epochs on the GPU. The paths preserve Qwen3 non-thinking mode. Keep the dataset's system instruction during inference.

## Evaluate

Execute SELECT queries on a disposable SQLite database. Compare result rows and ordering, including empty data, null values and ties.

Use [held-out evaluation](../../guides/04-evaluate.md), then [run locally](../../guides/06-run-locally.md). Report every evaluation example, including failures, and test the exported quantization too.
