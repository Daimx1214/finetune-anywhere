"""Train a recipe with QLoRA, save adapters, and optionally export GGUF."""

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from common import model_id  # noqa: E402
from validate_dataset import validate  # noqa: E402


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=ROOT / "recipes/json-extractor/config.yaml")
    p.add_argument("--model", help="override the model alias")
    p.add_argument("--output", type=Path)
    p.add_argument("--max-steps", type=int, default=-1, help="positive value for a smoke test")
    p.add_argument("--resume", help="checkpoint directory")
    p.add_argument("--export-gguf", action="store_true")
    a = p.parse_args()
    import yaml

    cfg = yaml.safe_load(a.config.read_text())
    data = a.config.parent / "data"
    for split in ["train", "valid", "eval"]:
        errors, _, _ = validate(data / f"{split}.jsonl", max_tokens=cfg["max_seq_length"])
        if errors:
            p.error("\n".join(errors))
    output = a.output or ROOT / "outputs" / cfg["recipe"]
    # Import Unsloth before TRL and Transformers so its optimizations are applied.
    from datasets import load_dataset
    from trl import SFTConfig, SFTTrainer
    from unsloth import FastLanguageModel, is_bfloat16_supported

    started = time.monotonic()
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_id(a.model or cfg["model"]),
        max_seq_length=cfg["max_seq_length"],
        dtype=None,
        load_in_4bit=True,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=cfg["rank"],
        lora_alpha=cfg["alpha"],
        lora_dropout=0,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=cfg["seed"],
    )
    dataset = load_dataset("json", data_files={s: str(data / f"{s}.jsonl") for s in ["train", "valid"]})

    def format_rows(batch):
        return {
            "text": [
                tokenizer.apply_chat_template(m, tokenize=False, add_generation_prompt=False)
                for m in batch["messages"]
            ]
        }

    dataset = dataset.map(format_rows, batched=True, remove_columns=["messages"])
    training = SFTConfig(
        output_dir=str(output / "checkpoints"),
        dataset_text_field="text",
        max_length=cfg["max_seq_length"],
        per_device_train_batch_size=cfg["batch_size"],
        gradient_accumulation_steps=cfg["gradient_accumulation_steps"],
        learning_rate=cfg["learning_rate"],
        num_train_epochs=cfg["epochs"],
        max_steps=a.max_steps,
        bf16=is_bfloat16_supported(),
        fp16=not is_bfloat16_supported(),
        logging_steps=1,
        save_strategy="epoch",
        eval_strategy="epoch",
        per_device_eval_batch_size=1,
        seed=cfg["seed"],
        report_to="none",
        packing=False,
    )
    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset["valid"],
        args=training,
    )
    trainer.train(resume_from_checkpoint=a.resume)
    model.save_pretrained(str(output / "adapter"))
    tokenizer.save_pretrained(str(output / "adapter"))
    model.save_pretrained_merged(str(output / "merged"), tokenizer, save_method="merged_16bit")
    if a.export_gguf:
        model.save_pretrained_gguf(str(output / "gguf"), tokenizer, quantization_method="q4_k_m")
    (output / "run.json").write_text(
        json.dumps(
            {
                "config": cfg,
                "model_alias": a.model or cfg["model"],
                "elapsed_seconds": time.monotonic() - started,
                "max_steps": a.max_steps,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"Saved run to {output}. Evaluate before choosing it over the base model.")


if __name__ == "__main__":
    main()
