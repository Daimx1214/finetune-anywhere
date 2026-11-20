# TRL + PEFT

Use this notebook to understand the Python pieces: model, tokenizer, dataset, adapter and supervised trainer. A CUDA GPU is recommended. PyTorch device support does not mean every quantization backend supports the same device. CPU training is possible but slow, so CPU beginners should use the cloud paths.

Create a fresh Python 3.11 environment, install the pinned requirements and start Jupyter from the repository root:

```bash
python -m pip install -r tools/trl-peft/requirements.txt
jupyter lab tools/trl-peft/finetune_trl_peft.ipynb
```

Run the notebook in order. It loads the `starter` alias, uses the shared chat data, trains LoRA and saves both adapter and merged model. Full-precision base weights make the mechanics clear but use more memory than the Unsloth QLoRA route.

The notebook's merged directory is `outputs/trl/merged`. Use it in [GGUF export](../../guides/05-quantize.md), then [evaluate](../../guides/04-evaluate.md) and [run locally](../../guides/06-run-locally.md).

Sources: [TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer) and [PEFT LoRA](https://huggingface.co/docs/peft/conceptual_guides/lora).
