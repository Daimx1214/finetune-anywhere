# Run locally

Use the evaluated GGUF from [quantization](05-quantize.md). Keep the runtime on localhost unless you deliberately add authentication and network controls.

## Ollama

Install [Ollama](https://ollama.com/download) for your OS. Start the app, or run `ollama serve` in a terminal. Save this full `Modelfile` next to the exported GGUF:

```dockerfile
FROM ./finetuned-q4_k_m.gguf
PARAMETER temperature 0
PARAMETER num_ctx 2048
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|im_start|>"
```

The GGUF carries the tokenizer's Qwen3 chat template with non-thinking mode saved by the training paths. Ollama imports recognized model templates; deliberately avoid replacing it with a hand-written template that may corrupt multi-turn messages. Verify the imported template with `ollama show recipe-local --modelfile` and compare behavior with llama.cpp. If recognition fails, update Ollama and check the export rather than guessing delimiters.

```bash
ollama create recipe-local -f outputs/Modelfile
ollama run recipe-local
```

For evaluation, copy the Modelfile to `outputs/Modelfile.base`, change its `FROM` line to `./base-q4_k_m.gguf`, and run `ollama create recipe-base -f outputs/Modelfile.base`.

## llama.cpp

Build it using the quantization guide. The CLI and server read the GGUF chat template:

```bash
outputs/llama.cpp/build/bin/llama-cli -m outputs/finetuned-q4_k_m.gguf -cnv --ctx-size 2048
outputs/llama.cpp/build/bin/llama-server -m outputs/finetuned-q4_k_m.gguf --host 127.0.0.1 --port 8080 --ctx-size 2048
```

Run one command at a time, or use separate terminals. Add `--n-gpu-layers 0` to force CPU inference.

## LM Studio

Install [LM Studio](https://lmstudio.ai/). Import your GGUF with its [documented import workflow](https://lmstudio.ai/docs/app/advanced/import-model), load it, and use Chat. The CLI route is `lms import outputs/finetuned-q4_k_m.gguf` once `lms` is available. Set a modest context and verify the template. The Developer tab can start a local API server.

## MLX-LM on Mac

```bash
mlx_lm.generate --model outputs/json-extractor/mlx/finetuned-4bit --prompt 'Please order 3 lamps.' --max-tokens 128
mlx_lm.server --model outputs/json-extractor/mlx/finetuned-4bit --host 127.0.0.1 --port 8080
```

## vLLM on a GPU server

Install vLLM in a separate environment using [its hardware-specific instructions](https://docs.vllm.ai/en/latest/getting_started/installation/). Serve merged Hugging Face weights:

```bash
vllm serve outputs/json-extractor/merged --served-model-name recipe-local --host 127.0.0.1 --port 8000
```

## Transformers in Python

In a Transformers/PyTorch environment:

```python
from transformers import pipeline
chat = pipeline("text-generation", model="outputs/json-extractor/merged", device_map="auto")
print(chat([{"role": "user", "content": "Please order 3 lamps."}], max_new_tokens=128, do_sample=False))
```

## Call a local OpenAI-compatible API

This example needs only Python's standard library. Use port 11434 and model `recipe-local` for Ollama, or port 8000 for the vLLM command above.

```python
import json
from urllib.request import Request, urlopen
body = {"model": "recipe-local", "messages": [{"role": "user", "content": "Please order 3 lamps."}], "max_tokens": 128, "temperature": 0}
request = Request("http://localhost:8080/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
with urlopen(request, timeout=120) as response:
    print(json.load(response)["choices"][0]["message"]["content"])
```

Include your task's system prompt in real calls, matching the dataset.

Next: [Share your model](07-share-your-model.md).
