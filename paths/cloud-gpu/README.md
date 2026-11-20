# Train on a rented GPU

Use a rented GPU when free notebooks are unavailable or you need a longer session. Prerequisites: a provider account, payment method, SSH/Jupyter access and a spending limit. Plan setup time plus the measured training duration. This guide does not quote prices.

## Shared workflow

1. Choose a GPU using the [memory estimate](../../scripts/memory_calc.py). Leave room for activations and export.
2. Choose a current Linux PyTorch/CUDA image compatible with the GPU and the training stack. Use persistent storage if you need checkpoints after an interruption.
3. Connect using the provider's displayed SSH command or Jupyter terminal. Keep its credentials private.
4. Clone and activate an isolated Python 3.11 environment:

```bash
git clone https://github.com/junaiddshaukat/finetune-anywhere.git
cd finetune-anywhere
nvidia-smi
python3.11 -m venv .venv-train
source .venv-train/bin/activate
python -m pip install -r paths/nvidia-gpu/requirements.txt
python paths/nvidia-gpu/train_unsloth.py --model tiny --max-steps 2 --output outputs/smoke
python paths/nvidia-gpu/train_unsloth.py --export-gguf
```

5. [Upload the adapter and exported model](../../guides/07-share-your-model.md). Confirm the files can be downloaded before destroying storage.
6. Download the GGUF and use [the local inference guide](../../guides/06-run-locally.md).
7. **Stop or terminate the billed GPU resource in the provider dashboard.** Check persistent volumes, snapshots and reserved resources separately because they may still incur charges.

## Provider notes

| Provider | Where to start | What to check |
| --- | --- | --- |
| [RunPod](https://docs.runpod.io/pods/overview) | GPU Pod with a PyTorch template | Pod storage lifecycle, SSH access, termination |
| [Vast.ai](https://docs.vast.ai/documentation/get-started/quickstart) | GPU instance with an appropriate container | Host reliability, disk, SSH mapping, instance removal |
| [Lambda](https://docs.lambda.ai/) | GPU cloud instance | SSH key, image CUDA stack, filesystem persistence |
| [Lightning AI](https://lightning.ai/docs/overview/studios) | Studio terminal and GPU machine | Workspace persistence, machine state and account billing |
| [Modal](https://modal.com/docs/guide/gpu) | GPU function in a Python app | Image dependencies, timeout, persistent Volume and app lifecycle |

Modal is function-based, not a normal SSH VM. Use its official GPU example to define an image with this repository's dependencies, mount your data and persist `outputs/` to a Volume. Run the same training command within the function. A ready-made Modal deployment is not included because it has not been validated here. Use a VM-style provider above for the shortest copy-paste route.

## Common errors

An image can have PyTorch without a compatible driver or GPU architecture. Verify `torch.cuda.is_available()` before downloading a large model. A disconnected browser does not necessarily stop billing. SSH loss does not prove the training job stopped. Export can need substantially more RAM and disk than adapter training. Never assume a temporary container filesystem is a backup.
