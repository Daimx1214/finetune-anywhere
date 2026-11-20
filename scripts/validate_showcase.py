"""Validate a single submission against trusted schema and changed-file metadata."""

import argparse
import datetime as dt
import ipaddress
import json
import socket
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import jsonschema
import yaml
from common import ROOT

DEADLINE = dt.datetime(2026, 11, 28, 18, 59, tzinfo=dt.UTC)


def is_late(created_at):
    # The published closing minute is inclusive.
    return dt.datetime.fromisoformat(created_at.replace("Z", "+00:00")) >= DEADLINE + dt.timedelta(minutes=1)


def urls(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from urls(child)
    elif isinstance(value, list):
        for child in value:
            yield from urls(child)
    elif isinstance(value, str) and value.startswith("https://"):
        yield value


def public_url(url):
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.port not in [None, 443]
    ):
        return False
    return all(
        ipaddress.ip_address(addr[4][0]).is_global for addr in socket.getaddrinfo(parsed.hostname, 443)
    )


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check_urls(data):
    warnings = []
    opener = urllib.request.build_opener(NoRedirect)
    for url in sorted(set(urls(data)))[:30]:
        try:
            if not public_url(url):
                raise ValueError("only public HTTPS hosts on port 443 are checked")
            opener.open(
                urllib.request.Request(
                    url, method="HEAD", headers={"User-Agent": "finetune-anywhere-link-check"}
                ),
                timeout=5,
            ).close()
        except (OSError, ValueError, urllib.error.URLError) as exc:
            warnings.append(f"Could not confirm URL {url}: {exc}")
    return warnings


def validate(root, changed, created_at, network=False):
    errors, warnings, entries = [], [], set()
    for name in changed:
        parts = Path(name).parts
        if len(parts) < 4 or parts[0] != "showcase" or parts[1] == "_template" or ".." in parts:
            errors.append(f"{name}: change only files in one showcase/<event>/<slug>/ folder")
        else:
            entries.add(Path(*parts[:3]))
    if len(entries) != 1:
        errors.append(f"Expected exactly one entry folder; found {len(entries)}")
    data, late = {}, False
    if len(entries) == 1:
        relative = next(iter(entries))
        folder = root / relative
        if not (root / relative.parent / "README.md").is_file():
            errors.append("Event folder must already have a README; use community for general submissions")
        for path in folder.rglob("*"):
            if path.is_symlink():
                errors.append(f"{path.relative_to(root)}: symlinks are not allowed")
            elif path.is_file():
                if path.stat().st_size > 5_000_000:
                    errors.append(f"{path.relative_to(root)}: exceeds 5 MB")
                if path.suffix.lower() in {".gguf", ".safetensors", ".bin", ".pt", ".pth", ".ckpt"}:
                    errors.append(f"{path.relative_to(root)}: model weights are not allowed")
        manifest = folder / "model.yaml"
        try:
            if (
                manifest.is_symlink()
                or folder.is_symlink()
                or not manifest.resolve().is_relative_to(root.resolve())
            ):
                raise ValueError("manifest must be a regular file inside the submission")
            if manifest.stat().st_size > 100_000:
                raise ValueError("model.yaml exceeds 100 KB")
            data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
            schema = json.loads((ROOT / "schema/model.schema.json").read_text())
            for error in jsonschema.Draft202012Validator(schema).iter_errors(data):
                errors.append(
                    f"model.yaml:{'.'.join(map(str, error.absolute_path)) or 'root'}: {error.message}"
                )
            if not isinstance(data, dict):
                data = {}
            if data.get("slug") != relative.name:
                errors.append("slug must match the entry folder name")
            if data.get("event") != relative.parent.name:
                errors.append("event must match the parent folder name")
            late = relative.parent.name == "qwen-local-hackathon-2026" and is_late(created_at)
            if late:
                warnings.append(
                    "This entry is late and will not be judged. Consider moving it to community/."
                )
            readme = folder / "README.md"
            template = (ROOT / "showcase/_template/README.md").read_text()
            if (
                readme.is_symlink()
                or not readme.is_file()
                or readme.read_text().strip() == template.strip()
                or len(readme.read_text().strip()) < 100
            ):
                errors.append("Add a completed README.md with your actual training, commands and results")
            if network and not errors:
                warnings.extend(check_urls(data))
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{relative}: {exc}")
    return {"passed": not errors, "errors": errors, "warnings": warnings, "late": late}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument(
        "--changed-json", type=Path, required=True, help="JSON array of repo-relative changed filenames"
    )
    p.add_argument("--created-at", required=True, help="PR creation time, ISO 8601 UTC")
    p.add_argument("--check-urls", action="store_true")
    p.add_argument("--output", type=Path, default=Path("results.json"))
    a = p.parse_args()
    result = validate(a.root, json.loads(a.changed_json.read_text()), a.created_at, a.check_urls)
    a.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
