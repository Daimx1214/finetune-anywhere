"""Exercise the actual export/download cells against both Unsloth directory layouts."""

import json
import sys
import time
from types import ModuleType, SimpleNamespace

import nbformat
import pytest

from common import ROOT


def source(platform, marker):
    notebook = nbformat.read(ROOT / f"paths/{platform}/finetune_unsloth_{platform}.ipynb", as_version=4)
    return next(cell.source for cell in notebook.cells if cell.cell_type == "code" and marker in cell.source)


@pytest.mark.parametrize("platform", ["colab", "kaggle"])
@pytest.mark.parametrize("directory", ["gguf", "gguf_gguf"])
def test_export_records_actual_quantized_path(tmp_path, platform, directory):
    artifact = tmp_path / directory / "model.Q4_K_M.gguf"

    def export(*args, **kwargs):
        artifact.parent.mkdir()
        artifact.write_bytes(b"GGUF-test-fixture")
        (artifact.parent / "model.F16.gguf").write_bytes(b"intermediate-fixture")

    state = {
        "OUTPUT": tmp_path,
        "model": SimpleNamespace(save_pretrained_gguf=export),
        "tokenizer": object(),
        "report": {"export_completed": False},
        "time": time,
        "json": json,
    }
    exec(source(platform, "model.save_pretrained_gguf("), state)
    report = json.loads((tmp_path / "run.json").read_text())
    assert report["export_completed"] is True
    assert report["gguf_files"] == [
        {"name": artifact.name, "path": f"{directory}/{artifact.name}", "bytes": artifact.stat().st_size}
    ]


@pytest.mark.parametrize(
    "filename,contents", [("model.F16.gguf", b"intermediate"), ("model.Q4_K_M.gguf", b"")]
)
def test_intermediate_or_empty_export_is_not_success(tmp_path, filename, contents):
    def export(*args, **kwargs):
        (tmp_path / filename).write_bytes(contents)

    state = {
        "OUTPUT": tmp_path,
        "model": SimpleNamespace(save_pretrained_gguf=export),
        "tokenizer": object(),
        "report": {"export_completed": False},
        "time": time,
        "json": json,
    }
    with pytest.raises(AssertionError, match="No nonempty Q4_K_M"):
        exec(source("colab", "model.save_pretrained_gguf("), state)
    assert state["report"]["export_completed"] is False


def test_download_cell_finds_sibling_directory(tmp_path, monkeypatch):
    artifact = tmp_path / "gguf_gguf" / "model.Q4_K_M.gguf"
    artifact.parent.mkdir()
    artifact.write_bytes(b"GGUF-test-fixture")
    for name in ["run.json", "comparison.json", "comparison.md", "training-log.json"]:
        (tmp_path / name).write_text("test fixture")
    downloads = []
    google = ModuleType("google")
    colab = ModuleType("google.colab")
    colab.files = SimpleNamespace(download=lambda path: downloads.append(path))
    google.colab = colab
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.colab", colab)
    code = source("colab", "DOWNLOAD_GGUF = False").replace("DOWNLOAD_GGUF = False", "DOWNLOAD_GGUF = True")
    exec(code, {"OUTPUT": tmp_path})
    assert downloads == [str(tmp_path / "run-evidence.zip"), str(artifact)]
