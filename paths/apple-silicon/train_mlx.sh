#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
recipe="${1:-json-extractor}"
model_alias="${2:-starter}"
iters="${3:-100}"
case "$recipe" in
  commit-message-writer|json-extractor|sql-generator|support-bot-from-docs) ;;
  *) echo 'Choose a recipe directory shipped in recipes/.' >&2; exit 2 ;;
esac
model_id=$(python scripts/model_id.py "$model_alias")
output="outputs/$recipe/mlx"
python scripts/validate_dataset.py "recipes/$recipe/data/train.jsonl" "recipes/$recipe/data/valid.jsonl" "recipes/$recipe/data/eval.jsonl"
mkdir -p "$output"
# Quantize before training to reduce unified-memory use.
mlx_lm.convert --hf-path "$model_id" --mlx-path "$output/base-4bit" -q --q-bits 4
python scripts/configure_chat.py "$output/base-4bit"
mlx_lm.lora --model "$output/base-4bit" --train --data "recipes/$recipe/data" \
  --iters "$iters" --batch-size 1 --num-layers 8 --learning-rate 0.0002 \
  --max-seq-length 1024 --grad-checkpoint --adapter-path "$output/adapters" \
  --config paths/apple-silicon/lora.yaml
# Fuse in full precision for portable HF-to-GGUF conversion.
mlx_lm.fuse --model "$model_id" --adapter-path "$output/adapters" --save-path "$output/merged"
python scripts/configure_chat.py "$output/merged"
mlx_lm.convert --hf-path "$output/merged" --mlx-path "$output/finetuned-4bit" -q --q-bits 4
mlx_lm.generate --model "$output/finetuned-4bit" --prompt 'Please order 3 lamps. This is urgent.' --max-tokens 128
