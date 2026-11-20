"""Shared registry, JSONL and Markdown helpers."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def registry():
    import yaml

    return yaml.safe_load((ROOT / "configs/models.yaml").read_text())


def model_id(alias=None):
    data = registry()
    key = alias or data["default"]
    if key not in data["models"]:
        raise ValueError(f"Unknown model alias {key!r}. Choose: {', '.join(data['models'])}")
    return data["models"][key]["id"]


def read_rows(path):
    rows = []
    for line, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line}: invalid JSON: {exc.msg}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line}: expected a JSON object")
        rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no examples")
    return rows


def cell(value):
    import html

    return html.escape(str(value)).replace("|", "&#124;").replace("\r", "").replace("\n", "<br>")
