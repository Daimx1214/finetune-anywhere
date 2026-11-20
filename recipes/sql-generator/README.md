# Generate read-only SQL for a fixed schema

Fine-tuning can teach a repeatable output format and task style. It does not guarantee correctness or add a reliable knowledge database.

## Data and license

The included data is original synthetic teaching data, released under this repository's MIT license. Its rules and targets were checked during authoring. There are 100 training, 12 validation and 12 held-out evaluation examples. Validation chooses settings; evaluation stays untouched until the final comparison.

These examples deliberately use simple patterns. New entities are held out, but templates overlap. A good score here does not establish real-world generalization. Add diverse, licensed examples and a separate human-written test set before using the model for real work.

## Train

Model: `starter` from [the registry](../../configs/models.yaml). Default path: [NVIDIA](../../paths/nvidia-gpu/), also usable on [Colab](../../paths/colab/) and [Mac](../../paths/apple-silicon/). Training time has not been measured; the script records elapsed seconds for your run.

From the repository root, after installing the hardware path:

```bash
python scripts/validate_dataset.py recipes/sql-generator/data/train.jsonl recipes/sql-generator/data/valid.jsonl recipes/sql-generator/data/eval.jsonl
python paths/nvidia-gpu/train_unsloth.py --config recipes/sql-generator/config.yaml --export-gguf
```

On Mac, pass this recipe to the shared wrapper:

```bash
bash paths/apple-silicon/train_mlx.sh sql-generator
```

## Evaluate and run

Execute queries against a disposable SQLite database and compare results. Never execute model SQL on production data.

Follow [held-out evaluation](../../guides/04-evaluate.md), then [local inference](../../guides/06-run-locally.md). No before/after outputs are published without a real run. Record the base revision, adapter, seed, hardware, elapsed time and failed examples in your model card.
