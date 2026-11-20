# Share your model

Publish weights on a model hub, not in this Git repository. Keep credentials in your account's token store or environment, never in notebooks or model cards. Review license terms and remove private data first.

## Write the model card

Put a `README.md` in your export directory. State the task, exact base ID and revision, license, dataset source and rights, split method, training settings, hardware, measured duration, runtime, quantization, actual before/after examples and limitations. Explain whether the upload is an adapter or a merged model. Include commands to reproduce inference.

Repository model IDs belong in the registry. A model card uploaded to a separate model hub must still identify its base accurately.

## Hugging Face CLI

Install the Hub client in your active environment. Read the model card before making the repository public.

```bash
python -m pip install 'huggingface-hub==2.4.0'
hf auth login
read -r -p 'Your Hub username: ' HF_USER
hf upload "$HF_USER/finetuned-json-extractor" outputs/json-extractor/merged .
```

The CLI can create the target model repository. Upload a GGUF export folder instead if that is the artifact you want to share. Do not upload checkpoints or tokens by accident.

## Hugging Face Python

This uses the login token saved by `hf auth login`:

```python
from huggingface_hub import HfApi
api = HfApi()
repo_id = input("Your model repository (owner/name): ").strip()
api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)
api.upload_folder(repo_id=repo_id, folder_path="outputs/json-extractor/merged", repo_type="model")
```

## ModelScope CLI

Create a model repository in your ModelScope account first and choose its visibility and license. The installed CLI's help confirms these commands:

```bash
python -m pip install 'modelscope==1.40.3'
modelscope login
read -r -p 'Your ModelScope repository (owner/name): ' MS_REPO
modelscope upload "$MS_REPO" outputs/json-extractor/merged
```

## ModelScope Python

Use a token from your own account. `getpass` keeps it out of terminal history:

```python
from getpass import getpass
from modelscope.hub.api import HubApi
api = HubApi()
api.login(getpass("ModelScope token: "))
repo_id = input("Existing model repository (owner/name): ").strip()
api.upload_folder(repo_id=repo_id, folder_path="outputs/json-extractor/merged", repo_type="model")
```

Source: [ModelScope SDK](https://github.com/modelscope/modelscope). Hub APIs evolve, so these examples name the checked client release. After upload, open the public link while signed out and verify files and model card are visible.

Next: [Add your model to the showcase](../showcase/README.md#submit-your-model).
