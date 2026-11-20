# LLaMA-Factory

Choose this for LlamaBoard's web UI or YAML-based training with several backends. Use a separate NVIDIA Python 3.11 environment. Follow the [official install requirements](https://github.com/hiyouga/LLaMA-Factory) for the selected release and CUDA stack.

```bash
python -m pip install 'llamafactory==0.9.5' 'PyYAML==6.0.3'
python scripts/prepare_tool.py llama-factory
llamafactory-cli train outputs/llama-factory/train.yaml
```

The preparation script resolves the default model alias and registers the shared chat JSONL files as ShareGPT-style messages with explicit role/content mappings. The checked-in YAML is a template for that script, not a standalone config with a duplicated model ID.

For the UI, run `llamafactory-cli webui`, choose the registry model and match the config's settings. Keep the UI private to your machine.

Export the resulting adapter using the shared merger:

```bash
python scripts/merge_adapter.py outputs/llama-factory/adapter --output outputs/llama-factory/merged
```

This CPU float32 merge needs RAM for the base and temporary tensors. Follow [GGUF export](../../guides/05-quantize.md) using that merged directory, [local inference](../../guides/06-run-locally.md), and [evaluation](../../guides/04-evaluate.md). The installed tool version is pinned; GPU execution is listed separately in maintainer validation notes.
