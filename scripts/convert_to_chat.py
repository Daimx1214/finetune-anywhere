"""Convert CSV question/answer columns, JSON Q&A pairs, or paired text blocks to chat JSONL."""

import argparse
import csv
import json
from pathlib import Path


def convert(source, kind, question="question", answer="answer", system=None):
    with source.open(encoding="utf-8", newline="") as stream:
        if kind == "csv":
            rows = list(csv.DictReader(stream))
        elif kind == "json":
            rows = json.load(stream)
            if not isinstance(rows, list):
                raise ValueError("JSON input must be an array of question/answer objects")
        else:
            rows = []
            for block in stream.read().strip().split("\n\n"):
                if not block.startswith("Q: ") or "\nA: " not in block:
                    raise ValueError(
                        "Text blocks must be Q: question followed by A: answer, separated by blank lines"
                    )
                q, ans = block[3:].split("\nA: ", 1)
                rows.append({question: q, answer: ans})
    output = []
    for i, row in enumerate(rows, 1):
        if not isinstance(row, dict) or any(
            not isinstance(row.get(k), str) or not row[k].strip() for k in [question, answer]
        ):
            raise ValueError(f"row {i}: nonempty {question!r} and {answer!r} required")
        messages = [{"role": "system", "content": system}] if system else []
        messages += [
            {"role": "user", "content": row[question].strip()},
            {"role": "assistant", "content": row[answer].strip()},
        ]
        output.append({"messages": messages})
    if not output:
        raise ValueError("input has no examples")
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--format", choices=["csv", "json", "text"], required=True)
    p.add_argument("--question-column", default="question")
    p.add_argument("--answer-column", default="answer")
    p.add_argument("--system")
    a = p.parse_args()
    if a.output.exists():
        p.error("output already exists; choose a new path to avoid overwriting data")
    try:
        rows = convert(a.input, a.format, a.question_column, a.answer_column, a.system)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    except (OSError, ValueError) as exc:
        p.error(str(exc))
    print(f"Wrote {len(rows)} examples to {a.output}")


if __name__ == "__main__":
    main()
