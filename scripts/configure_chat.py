"""Persist Qwen3 non-thinking mode in a local tokenizer for training and GGUF export."""

import argparse
from pathlib import Path

NON_THINKING_PREFIX = "{% set enable_thinking = false %}\n"


def configure_tokenizer(tokenizer):
    template = tokenizer.chat_template
    if not isinstance(template, str) or "enable_thinking" not in template:
        raise ValueError("Expected the Qwen3 chat template with enable_thinking support")
    if not template.startswith(NON_THINKING_PREFIX):
        tokenizer.chat_template = NON_THINKING_PREFIX + template
    return tokenizer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="local model or tokenizer directory")
    args = parser.parse_args()
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.directory, local_files_only=True)
    configure_tokenizer(tokenizer).save_pretrained(args.directory)
    print(f"Saved non-thinking chat template in {args.directory}")
