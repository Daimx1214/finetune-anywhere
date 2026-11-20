# Quantize

Keep the adapter and merged full-precision model. Quantize a copy, then evaluate it. Training-time bitsandbytes 4-bit weights are not the same file format as GGUF.

## Choose a GGUF quantization

| Format | Practical choice |
| --- | --- |
| Q4_K_M | First try when memory and disk matter |
| Q5_K_M | More storage for potentially better quality |
| Q8_0 | Larger, useful when quality loss is a concern |

These formats use mixed blocks and metadata; the bit label does not exactly equal file bytes. Measure task quality and memory on your hardware.

Unsloth's training script exports Q4_K_M with `--export-gguf`. Its underlying call is `model.save_pretrained_gguf(path, tokenizer, quantization_method="q4_k_m")`.

## Convert merged Hugging Face weights

Install Git, CMake and a C++ compiler. On Ubuntu/WSL use `sudo apt-get install -y git cmake build-essential`. On Mac use `xcode-select --install` and `brew install cmake` after installing Homebrew. Run from the repository root:

```bash
mkdir -p outputs
git clone https://github.com/ggml-org/llama.cpp.git outputs/llama.cpp
cmake -S outputs/llama.cpp -B outputs/llama.cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build outputs/llama.cpp/build --config Release -j 2
python -m pip install -r outputs/llama.cpp/requirements.txt
```

Set `MERGED` to the directory your trainer produced. This command uses the default NVIDIA recipe output; for Mac use `outputs/json-extractor/mlx/merged`.

```bash
MERGED=outputs/json-extractor/merged
python outputs/llama.cpp/convert_hf_to_gguf.py "$MERGED" --outfile outputs/finetuned-f16.gguf --outtype f16
outputs/llama.cpp/build/bin/llama-quantize outputs/finetuned-f16.gguf outputs/finetuned-q4_k_m.gguf Q4_K_M
```

To make a base control, download the same unmodified model, then convert and quantize it with the same commands:

```bash
hf download "$(python scripts/model_id.py starter)" --local-dir outputs/base-hf
python scripts/configure_chat.py outputs/base-hf
python outputs/llama.cpp/convert_hf_to_gguf.py outputs/base-hf --outfile outputs/base-f16.gguf --outtype f16
outputs/llama.cpp/build/bin/llama-quantize outputs/base-f16.gguf outputs/base-q4_k_m.gguf Q4_K_M
```

## MLX

```bash
mlx_lm.convert --hf-path outputs/json-extractor/mlx/merged --mlx-path outputs/json-extractor/mlx/finetuned-4bit -q --q-bits 4
mlx_lm.convert --hf-path outputs/json-extractor/mlx/merged --mlx-path outputs/json-extractor/mlx/finetuned-8bit -q --q-bits 8
```

MLX's built-in fused GGUF exporter does not support every architecture. For these Qwen models, use the merged model plus llama.cpp conversion above. Do not assume `--export-gguf` works for them.

Advanced: AWQ and GPTQ are other quantization approaches used for GPU serving. Check [vLLM's supported formats and hardware](https://docs.vllm.ai/en/latest/features/quantization/) before producing them. They are not GGUF substitutes for every runtime.

Next: [Run locally](06-run-locally.md).
