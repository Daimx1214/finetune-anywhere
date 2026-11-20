"""Resolve registry aliases into a runnable LLaMA-Factory or Axolotl config."""

import argparse

import yaml
from common import ROOT, model_id


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("tool", choices=["llama-factory", "axolotl"])
    p.add_argument("--model", default="starter")
    p.add_argument(
        "--recipe",
        default="json-extractor",
        choices=["json-extractor", "commit-message-writer", "sql-generator", "support-bot-from-docs"],
    )
    a = p.parse_args()
    filename = "qwen_lora_sft.yaml" if a.tool == "llama-factory" else "qwen_lora.yaml"
    cfg = yaml.safe_load((ROOT / "tools" / a.tool / filename).read_text())
    output = ROOT / "outputs" / a.tool
    output.mkdir(parents=True, exist_ok=True)
    data = ROOT / "recipes" / a.recipe / "data"
    cfg["output_dir"] = str(output / "adapter")
    if a.tool == "llama-factory":
        cfg["model_name_or_path"] = model_id(a.model)
        cfg["dataset_dir"] = str(output)
        info = {}
        for split in ["train", "valid"]:
            info[split] = {
                "file_name": str(data / f"{split}.jsonl"),
                "formatting": "sharegpt",
                "columns": {"messages": "messages"},
                "tags": {
                    "role_tag": "role",
                    "content_tag": "content",
                    "user_tag": "user",
                    "assistant_tag": "assistant",
                    "system_tag": "system",
                },
            }
        import json

        (output / "dataset_info.json").write_text(json.dumps(info, indent=2) + "\n")
    else:
        from transformers import AutoTokenizer
        from configure_chat import configure_tokenizer

        cfg["base_model"] = model_id(a.model)
        tokenizer = configure_tokenizer(AutoTokenizer.from_pretrained(model_id(a.model)))
        cfg["chat_template_jinja"] = tokenizer.chat_template
        cfg.pop("chat_template", None)
        cfg["datasets"] = [
            {"path": str(data / "train.jsonl"), "type": "chat_template", "field_messages": "messages"}
        ]
        cfg["test_datasets"] = [
            {"path": str(data / "valid.jsonl"), "type": "chat_template", "field_messages": "messages"}
        ]
    target = output / "train.yaml"
    target.write_text(yaml.safe_dump(cfg, sort_keys=False))
    print(target)


if __name__ == "__main__":
    main()
