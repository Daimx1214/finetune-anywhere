# Train on your NVIDIA GPU

Prerequisites: a CUDA-capable NVIDIA GPU supported by the installed PyTorch build, a compatible driver, disk for base/merged/exported weights, Git and Python 3.11. Plan an afternoon for your first setup and experiment.

## Linux setup

Verify the driver and available VRAM before installing a training environment:

```bash
nvidia-smi
python3.11 -m venv .venv-nvidia
source .venv-nvidia/bin/activate
python -m pip install --upgrade pip
python -m pip install -r paths/nvidia-gpu/requirements.txt
python -c 'import torch; print(torch.__version__, torch.cuda.is_available()); assert torch.cuda.is_available()'
```

Run commands from the cloned repository root. Install build tools for GGUF export:

```bash
sudo apt-get update
sudo apt-get install -y git cmake build-essential
```

The environment targets Linux x86_64 and Python 3.11. Consult [Unsloth installation](https://github.com/unslothai/unsloth) for driver-specific requirements. Do not mix multiple training tools into one environment.

## Windows through WSL2

Install a current NVIDIA Windows driver with WSL support. In an Administrator PowerShell terminal:

```powershell
wsl --install -d Ubuntu
```

Reboot if requested, open Ubuntu, install Python 3.11 through a supported Python installer, clone this repo inside the Linux home directory, and follow the Linux commands above. Verify `nvidia-smi` inside WSL. See [NVIDIA's WSL guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html). Do not install a Linux display driver inside WSL.

## Train and export

Run a short smoke test first. It checks the pipeline, not model quality:

```bash
python paths/nvidia-gpu/train_unsloth.py --model tiny --max-steps 2 --output outputs/smoke
```

Then train the default recipe in a new output directory:

```bash
python paths/nvidia-gpu/train_unsloth.py --config recipes/json-extractor/config.yaml --export-gguf
```

This saves checkpoints, an adapter, merged weights, a run manifest and a Q4_K_M GGUF under `outputs/json-extractor/`. Copy the exported GGUF to `outputs/finetuned-q4_k_m.gguf`. Keep the adapter and original base revision too.

## Run

Install [Ollama](https://ollama.com/download), start its app or `ollama serve`, then create `outputs/Modelfile`:

```dockerfile
FROM ./finetuned-q4_k_m.gguf
PARAMETER temperature 0
PARAMETER num_ctx 2048
```

```bash
ollama create recipe-local -f outputs/Modelfile
ollama run recipe-local
```

Follow [evaluation](../../guides/04-evaluate.md) before claiming improvement and [sharing](../../guides/07-share-your-model.md) to publish it.

[Troubleshooting](../../guides/faq.md).
