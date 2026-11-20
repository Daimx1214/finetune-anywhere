# Contributing

There are four ways to help:

1. [Add your model to the showcase](showcase/README.md#submit-your-model).
2. Add a recipe with licensed data, held-out evaluation and real run evidence.
3. Add or fix a hardware path, stating exactly what you tested.
4. Improve the docs, examples or error messages.

Use a separate PR for each showcase entry. For code and docs, explain the problem, what changed and how you checked it. Keep model IDs in `configs/models.yaml`; showcase manifests are the necessary exception because they report contributors' actual base models. Do not commit weights, credentials, notebook outputs or private data.

## Local checks

Use Python 3.11 and run from the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
ruff check scripts tests paths/nvidia-gpu
python -m pytest
python scripts/check_repo.py
python scripts/build_showcase.py
```

`check_repo.py` checks local Markdown links, notebook cleanliness, model-registry duplication, file sizes and writing constraints. CI also checks public links, with transient failures reported separately. GPU tests need their own hardware environments. Do not describe dependency resolution as a completed training run.

Keep guides below about 900 words. Use direct English, short sentences and no em dash characters. Explain why before non-obvious commands. Technical claims need an official source or an actual reproducible run.

## Credit

The maintainer adds contributors after merging. With the all-contributors app installed, a maintainer can comment `@all-contributors please add @username for code, doc` using the actual contributor's username and contribution types. Contributors do not need to request a star, follow or bot interaction to submit.

Please follow [the Code of Conduct](CODE_OF_CONDUCT.md). For questions, use [Discussions](https://github.com/junaiddshaukat/finetune-anywhere/discussions).
