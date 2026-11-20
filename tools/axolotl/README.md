# Axolotl

Choose Axolotl when YAML configuration and distributed GPU training fit your workflow. Keep it in its own environment; optimized kernels and CUDA requirements can conflict with other trainers. Follow [the official installation instructions](https://docs.axolotl.ai/docs/installation.html) for release 0.21.1.

```bash
python -m pip install 'axolotl==0.21.1' 'PyYAML==6.0.3'
python scripts/prepare_tool.py axolotl
axolotl train outputs/axolotl/train.yaml
```

The generator resolves the registry ID and shared JSONL paths, downloads the tokenizer and places its non-thinking Qwen3 template in the generated config. The config uses tokenizer-default chat formatting, QLoRA, rank 16, batch 1 and no sample packing. It keeps validation separate from final evaluation. Install failures involving Flash Attention need the official matching wheel/toolchain instructions, not arbitrary package upgrades.

After training, merge the saved adapter:

```bash
python scripts/merge_adapter.py outputs/axolotl/adapter --output outputs/axolotl/merged
```

Follow [GGUF export](../../guides/05-quantize.md) with this merged directory, then [run locally](../../guides/06-run-locally.md) and [evaluate](../../guides/04-evaluate.md).
