"""Merge a standard PEFT adapter into a fresh full-precision base model."""

import argparse
from pathlib import Path

from common import model_id

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("adapter", type=Path)
    p.add_argument("--model", default="starter")
    p.add_argument("--output", type=Path, default=Path("outputs/merged"))
    a = p.parse_args()
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    base = AutoModelForCausalLM.from_pretrained(
        model_id(a.model), torch_dtype=torch.float32, device_map="cpu"
    )
    model = PeftModel.from_pretrained(base, str(a.adapter)).merge_and_unload()
    model.save_pretrained(a.output, safe_serialization=True)
    AutoTokenizer.from_pretrained(model_id(a.model)).save_pretrained(a.output)
    print(f"Merged to {a.output}. CPU float32 merge needs substantial system RAM.")
