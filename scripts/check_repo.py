"""Check local Markdown links, public-file hygiene and output-free notebooks."""

import argparse
import ast
import json
import re
from pathlib import Path
from urllib.parse import unquote

from common import ROOT, registry


def check(root):
    errors = []
    models = [m["id"] for m in registry()["models"].values()]
    excluded = {".git", "outputs", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(p in excluded or p.startswith(".venv") for p in rel.parts) or not path.is_file():
            continue
        if path.stat().st_size > 5_000_000:
            errors.append(f"{rel}: file exceeds 5 MB")
        if path.suffix not in {".md", ".py", ".yaml", ".yml", ".json", ".ipynb", ".sh", ".txt", ".toml"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "\u2014" in text:
            errors.append(f"{rel}: contains an em dash")
        if str(rel) != "configs/models.yaml" and not str(rel).startswith("showcase/"):
            for model in models:
                if model in text:
                    errors.append(f"{rel}: duplicated registry model ID")
        if path.suffix == ".md":
            # Exclude code fences before interpreting Markdown links.
            prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
            for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", prose):
                target = match.group(1).split()[0].strip("<>")
                if re.match(r"^[a-zA-Z][\w+.-]*:", target) or target.startswith("#"):
                    continue
                local = unquote(target.split("#")[0])
                if local and not (path.parent / local).exists():
                    errors.append(f"{rel}: broken local link {target}")
            if rel.parts[0] == "guides" and len(text.split()) > 950:
                errors.append(f"{rel}: guide exceeds 950 words")
        if path.suffix == ".ipynb":
            import nbformat

            try:
                nb = nbformat.reads(text, as_version=4)
                nbformat.validate(nb)
                for cell in nb.cells:
                    if cell.cell_type == "code":
                        if cell.get("outputs") or cell.get("execution_count") is not None:
                            errors.append(f"{rel}: notebook has outputs or execution counts")
                        # Jupyter magics are not Python; compile the remaining cells.
                        source = cell.source
                        if not any(line.lstrip().startswith(("!", "%")) for line in source.splitlines()):
                            ast.parse(source)
            except (ValueError, SyntaxError, json.JSONDecodeError) as exc:
                errors.append(f"{rel}: invalid notebook: {exc}")
    return errors


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    a = p.parse_args()
    issues = check(a.root)
    if issues:
        p.exit(1, "\n".join(issues) + "\n")
    print("Local links, file sizes, model references, writing constraints and notebooks passed.")
