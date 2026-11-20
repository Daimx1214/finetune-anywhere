"""Run identical held-out prompts through two local OpenAI-compatible chat endpoints."""

import argparse
import json
import os
import urllib.request
from pathlib import Path

from common import cell, read_rows


def generate(url, model, messages, max_tokens):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": False,
    }
    headers = {"Content-Type": "application/json"}
    if os.environ.get("LOCAL_API_KEY"):
        headers["Authorization"] = "Bearer " + os.environ["LOCAL_API_KEY"]
    request = urllib.request.Request(
        url.rstrip("/") + "/chat/completions", json.dumps(payload).encode(), headers
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        data = json.load(response)
    content = data["choices"][0]["message"]["content"]
    if not isinstance(content, str):
        raise ValueError("endpoint returned no text content")
    return content


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--eval", type=Path, required=True)
    p.add_argument("--base-url", default="http://localhost:8080/v1")
    p.add_argument("--tuned-url", default="http://localhost:8081/v1")
    p.add_argument("--base-model", default="base")
    p.add_argument("--tuned-model", default="finetuned")
    p.add_argument("--max-tokens", type=int, default=256)
    p.add_argument("--output", type=Path, default=Path("outputs/comparison.md"))
    a = p.parse_args()
    from validate_dataset import validate

    errors, _, _ = validate(a.eval, max_tokens=1000000)
    if errors:
        p.error("\n".join(errors))
    records = []
    try:
        for row in read_rows(a.eval):
            messages = row["messages"]
            prompt = messages[:-1]  # Never send the reference assistant answer.
            records.append(
                {
                    "messages": prompt,
                    "reference": messages[-1]["content"],
                    "base": generate(a.base_url, a.base_model, prompt, a.max_tokens),
                    "finetuned": generate(a.tuned_url, a.tuned_model, prompt, a.max_tokens),
                }
            )
    except (OSError, ValueError, KeyError, IndexError) as exc:
        p.exit(1, f"Comparison failed; check both servers and model names: {exc}\n")
    lines = [
        "# Held-out comparison",
        "",
        "Temperature: 0. Same prompts and token budget; reference answers were withheld.",
        "",
        "| Prompt | Reference | Base | Fine-tuned |",
        "| --- | --- | --- | --- |",
    ]
    for r in records:
        prompt_text = "\n".join(m["role"] + ": " + m["content"] for m in r["messages"])
        lines.append(
            "| "
            + " | ".join(cell(x) for x in [prompt_text, r["reference"], r["base"], r["finetuned"]])
            + " |"
        )
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    a.output.with_suffix(".json").write_text(
        json.dumps(
            {
                "base_model": a.base_model,
                "tuned_model": a.tuned_model,
                "max_tokens": a.max_tokens,
                "temperature": 0,
                "records": records,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {a.output} and raw JSON. Review correctness, failures and regressions.")


if __name__ == "__main__":
    main()
