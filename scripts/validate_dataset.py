"""Check chat JSONL and leakage. Token counts are estimates unless --tokenizer is set."""

import argparse
import json
import math
import statistics
from pathlib import Path

from common import model_id, read_rows


def validate(path, tokenizer=None, max_tokens=2048):
    errors, lengths, seen, prompts = [], [], set(), set()
    try:
        rows = read_rows(path)
    except (ValueError, OSError) as exc:
        return [str(exc)], [], set()
    for line, row in enumerate(rows, 1):
        prefix = f"{path}:{line}:"
        messages = row.get("messages")
        if not isinstance(messages, list) or len(messages) < 2:
            errors.append(f"{prefix} messages must contain a user and assistant turn")
            continue
        valid = True
        offset = int(isinstance(messages[0], dict) and messages[0].get("role") == "system")
        for i, message in enumerate(messages):
            expected = "system" if offset and i == 0 else ("user" if (i - offset) % 2 == 0 else "assistant")
            if not isinstance(message, dict) or message.get("role") != expected:
                errors.append(f"{prefix} turn {i + 1}: expected role {expected}")
                valid = False
            if (
                not isinstance(message, dict)
                or not isinstance(message.get("content"), str)
                or not message["content"].strip()
            ):
                errors.append(f"{prefix} turn {i + 1}: content must be nonempty text")
                valid = False
        if isinstance(messages[-1], dict) and messages[-1].get("role") != "assistant":
            errors.append(f"{prefix} last turn must be assistant")
            valid = False
        if not valid:
            continue
        signature = json.dumps(messages, sort_keys=True, ensure_ascii=False)
        if signature in seen:
            errors.append(f"{prefix} duplicate example")
        seen.add(signature)
        prompt = json.dumps(messages[:-1], sort_keys=True, ensure_ascii=False)
        if prompt in prompts:
            errors.append(f"{prefix} repeated prompt (possible conflicting target)")
        prompts.add(prompt)
        n = (
            len(
                tokenizer.apply_chat_template(
                    messages, tokenize=True, return_dict=False, enable_thinking=False
                )
            )
            if tokenizer
            else math.ceil(len(signature) / 4)
        )
        lengths.append(n)
        if n > max_tokens:
            errors.append(
                f"{prefix} {n} tokens exceeds {max_tokens}"
                + (" (estimate; confirm with --tokenizer)" if tokenizer is None else "")
            )
    return errors, lengths, prompts


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("files", nargs="+", type=Path)
    p.add_argument("--tokenizer", metavar="MODEL_ALIAS", help="exact counts using registry alias")
    p.add_argument("--max-tokens", type=int, default=2048)
    a = p.parse_args()
    tokenizer = None
    if a.max_tokens <= 0:
        p.error("--max-tokens must be positive")
    if a.tokenizer:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_id(a.tokenizer))
    errors, all_prompts = [], set()
    for path in a.files:
        issues, lengths, prompts = validate(path, tokenizer, a.max_tokens)
        errors.extend(issues)
        if all_prompts & prompts:
            errors.append(f"{path}: prompt leakage across input files")
        all_prompts |= prompts
        if lengths:
            print(
                f"{path}: {len(lengths)} examples; tokens "
                f"{'exact' if tokenizer else 'estimated (characters/4 including structure)'}: "
                f"min={min(lengths)}, median={statistics.median(lengths):g}, max={max(lengths)}"
            )
    if errors:
        p.exit(1, "\n".join(errors) + "\n")
    print("Valid. No duplicate prompts or cross-file prompt leakage found.")


if __name__ == "__main__":
    main()
