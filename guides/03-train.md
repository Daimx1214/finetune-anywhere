# Train

Choose [Colab](../paths/colab/), [Kaggle](../paths/kaggle/), [NVIDIA](../paths/nvidia-gpu/), [Apple Silicon](../paths/apple-silicon/), [CPU plus cloud](../paths/cpu-only/) or [rented GPU](../paths/cloud-gpu/). Prefer a UI? Try [LLaMA-Factory](../tools/llama-factory/). Prefer plain Python? Try [TRL + PEFT](../tools/trl-peft/).

## Starting settings

These are conservative starter settings, not optimal values for every task.

| Setting | Start with | Meaning |
| --- | --- | --- |
| Rank | 16 | Adapter capacity. Higher rank adds trainable weights |
| Alpha | 32 | Adapter scaling. In MLX use scale 2 with rank 16 |
| Learning rate | 0.0002 | Update size. Reduce it if learning becomes unstable |
| Epochs | 1 | Complete passes through the training set |
| Maximum sequence length | 1024 | Maximum tokens per training conversation |
| Microbatch | 1 | Examples processed together on the device |
| Gradient accumulation | 4 | Four microbatches per optimizer update |
| Seed | 42 | Helps repeat a run, but does not ensure identical GPU results |

The Mac wrapper trains 100 iterations over eight adapter-equipped layers to keep its first run small. This is not numerically equivalent to the GPU recipe. Change the iteration count using its third argument. MLX uses its own adapter scaling convention.

## Chat template

A model expects special tokens around each role and message. Always use the tokenizer's `apply_chat_template`. For training, use `add_generation_prompt=False` because the assistant answer is already present. For inference, end on the user turn and enable the generation prompt. Avoid adding special tokens twice to a rendered string.

The starter trains on full conversations. Assistant-only loss is an advanced option that needs a compatible template and carefully verified masking. Bad masking can train on zero useful tokens. A mismatched inference template can make a good adapter look broken.

## Save and inspect

Run a two-step smoke test before a long NVIDIA job. Save checkpoints, adapter, tokenizer, merged model and a run manifest. A loss decrease says the training data became easier; it does not establish better answers. Use validation to select settings and leave evaluation untouched.

Optional tracking: TensorBoard can display local training logs when configured as the trainer's reporting backend. Cloud tracking such as Weights & Biases is opt-in and may upload data. This starter defaults to no remote reporting.

Next: [Evaluate](04-evaluate.md).
