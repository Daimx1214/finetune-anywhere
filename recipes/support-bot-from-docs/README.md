# Answer from a support policy

Fine-tune the `starter` Qwen3 1.7B text model to learn this task's output format and response style. Exact IDs and Apache-2.0 license information are in [the registry](../../configs/models.yaml).

## Dataset

Each scenario has its own policy and question. Topics include subscriptions, returns, permissions, storage, bookings and delivery. Cases cover exceptions, timing conditions, unsupported questions and quoted instructions.

All 60 scenarios are original, individually authored synthetic examples released under the repository's MIT license. They contain no scraped customer records or copied repository code. The splits contain **40 training, 10 validation and 10 evaluation examples**, authored separately rather than expanded by replacing identifiers. [Data manifest](data/manifest.json).

## Train

For a visible walkthrough, open [Colab](../../paths/colab/) or [Kaggle](../../paths/kaggle/) and set `RECIPE = 'support-bot-from-docs'` in Settings. The notebook records measured training time, hardware and actual before/after outputs in `run-evidence.zip`.

On [NVIDIA](../../paths/nvidia-gpu/), run from the repository root:

```bash
python scripts/validate_dataset.py recipes/support-bot-from-docs/data/train.jsonl recipes/support-bot-from-docs/data/valid.jsonl recipes/support-bot-from-docs/data/eval.jsonl
python paths/nvidia-gpu/train_unsloth.py --config recipes/support-bot-from-docs/config.yaml --export-gguf
```

On [Apple Silicon](../../paths/apple-silicon/):

```bash
bash paths/apple-silicon/train_mlx.sh support-bot-from-docs starter 100
```

The configuration uses rank 16, alpha 32, learning rate 0.0002 and three epochs on the GPU. The paths preserve Qwen3 non-thinking mode. Keep the dataset's system instruction during inference.

## Evaluate

Check every claim against the provided policy, preserve its exceptions and abstain when the answer is absent.

Use [held-out evaluation](../../guides/04-evaluate.md), then [run locally](../../guides/06-run-locally.md). Report every evaluation example, including failures, and test the exported quantization too.
