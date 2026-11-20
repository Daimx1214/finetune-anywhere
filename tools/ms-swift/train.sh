#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
model_id=$(python scripts/model_id.py starter)
swift sft --model "$model_id" --use_hf true --tuner_type lora --enable_thinking false --add_non_thinking_prefix true \
  --dataset recipes/json-extractor/data/train.jsonl \
  --val_dataset recipes/json-extractor/data/valid.jsonl \
  --lora_rank 16 --lora_alpha 32 --target_modules all-linear \
  --learning_rate 0.0002 --num_train_epochs 3 --max_length 1024 \
  --per_device_train_batch_size 1 --gradient_accumulation_steps 4 \
  --torch_dtype float16 --output_dir outputs/ms-swift --report_to none
