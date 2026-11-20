# Pick a model

Use **starter** for your first task. Use **tiny** for an installation smoke test or a low-memory machine. The exact model IDs live only in [configs/models.yaml](../configs/models.yaml). Resolve them instead of copying names between scripts:

```bash
python scripts/model_id.py starter
```

| Alias | Total parameters | FP16 GB | 8-bit GB | 4-bit GB | Good for |
| --- | ---: | ---: | ---: | ---: | --- |
| tiny | 0.49B | 0.98 | 0.49 | 0.27 | Setup checks, small structured tasks |
| starter | 1.54B | 3.08 | 1.54 | 0.85 | A first useful adapter |
| larger | 3.09B | 6.18 | 3.09 | 1.70 | More capacity when memory and license fit |

These are weights only: billions of parameters × 2, 1 or 0.55 bytes. Context, runtime and training activations need extra space. See [the calculator](../scripts/memory_calc.py).

The registry uses established instruction-tuned Qwen2.5 models to keep the starter simple. Smaller aliases use Apache-2.0; **larger uses the Qwen Research License**. Read the linked model card by opening the ID under the Hugging Face model site before distributing a derivative. The repository's MIT license does not replace model terms.

## Beyond Qwen

The dataset and evaluation approach also work with other open models. Add a verified model to the registry, confirm its license and architecture support in your trainer and exporter, and use its own tokenizer and chat template. Do not reuse Qwen's template for a different family. A text-only workflow does not automatically support vision or audio models.

Next: [Make a dataset](02-make-a-dataset.md).
