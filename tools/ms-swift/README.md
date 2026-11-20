# ModelScope SWIFT

Choose ms-swift for its Qwen tooling and ModelScope ecosystem. Use an isolated Python 3.11 NVIDIA environment and the [official installation guidance](https://github.com/modelscope/ms-swift).

```bash
python -m pip install 'ms-swift==4.6.1' 'PyYAML==6.0.3'
bash tools/ms-swift/train.sh
```

The script enables the empty non-thinking prefix during training and disables reasoning at inference. It resolves the registry model, reads the same messages JSONL as other paths and trains LoRA. It explicitly selects Hugging Face downloads so the registry ID is interpreted consistently. SWIFT also supports ModelScope downloads and publishing; see [sharing](../../guides/07-share-your-model.md).

SWIFT creates versioned run and checkpoint folders under `outputs/ms-swift`. Read the final checkpoint path in its log, then supply that actual directory to the merger:

```bash
read -r -p 'Adapter checkpoint directory: ' ADAPTER_DIR
python scripts/merge_adapter.py "$ADAPTER_DIR" --output outputs/ms-swift/merged
```

Follow [GGUF export](../../guides/05-quantize.md), setting `MERGED=outputs/ms-swift/merged`, then [local inference](../../guides/06-run-locally.md) and [evaluation](../../guides/04-evaluate.md).
