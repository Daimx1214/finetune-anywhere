# Pick a model

Start with **starter**, the 1.7B Qwen3 text model. Use **tiny** for your first short run or an 8 GB laptop, and **larger** when you want more capacity. All three use the Apache 2.0 license.

Exact Hugging Face IDs, corresponding Unsloth catalog IDs, reviewed revisions and model-card parameter counts live in [configs/models.yaml](../configs/models.yaml). Resolve an alias from the repository root:

```bash
python scripts/model_id.py starter
```

| Alias | Model family | Parameters | FP16 GB | 8-bit GB | 4-bit GB | Good for |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| tiny | Qwen3 | 0.6B | 1.20 | 0.60 | 0.33 | First run and low-memory inference |
| starter | Qwen3 | 1.7B | 3.40 | 1.70 | 0.94 | Structured tasks and small adapters |
| larger | Qwen3 | 4.0B | 8.00 | 4.00 | 2.20 | More capacity for language and code |

These weight estimates use the rounded model-card counts × 2, 1 or 0.55 bytes per parameter, in decimal GB. Add KV cache and runtime memory using [the calculator](../scripts/memory_calc.py).

## Direct answers with Qwen3

Qwen3 supports thinking and non-thinking modes. These recipes train direct answers using `enable_thinking=False`. The training paths persist that setting in the tokenizer's chat template so the exported model uses the same response prefix. Keep the recipe's system message during inference.

## Why the text-only defaults?

The registry also records the catalog review of Qwen3.5's small 0.8B, 2B and 4B models. They are Apache 2.0 image-text models. Qwen3 gives these starter recipes a shared text-model architecture across Unsloth, MLX-LM and llama.cpp. The [model review notes](../MAINTAINER_NOTES.md#model-review) record the Qwen3.5 decision.

## Other models

Add an Apache-2.0 text model to the registry after checking its original model card and support in your trainer and exporter. Use that model's own tokenizer and chat template. The Qwen3 non-thinking helper is specific to the supported Qwen3 aliases; adapt it when adding another family.

Next: [Make a dataset](02-make-a-dataset.md).
