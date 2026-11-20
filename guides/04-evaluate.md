# Evaluate

A fine-tune is useful only if it improves the task without unacceptable regressions. Compare the same unseen prompts with the same system message, generation settings and token budget.

## Create two local endpoints

After the [GGUF export steps](05-quantize.md), start a base model server in one terminal and a tuned server in another. Use the same quantization and the saved non-thinking template for both.

```bash
outputs/llama.cpp/build/bin/llama-server -m outputs/base-q4_k_m.gguf --port 8080 --ctx-size 2048
```

```bash
outputs/llama.cpp/build/bin/llama-server -m outputs/finetuned-q4_k_m.gguf --port 8081 --ctx-size 2048
```

On smaller machines, use Ollama to load the two models sequentially. Import the base as `recipe-base` and the tuned model as `recipe-local`, following [local inference](06-run-locally.md).

```bash
python scripts/compare.py --eval recipes/json-extractor/data/eval.jsonl --base-url http://localhost:11434/v1 --tuned-url http://localhost:11434/v1 --base-model recipe-base --tuned-model recipe-local --output outputs/comparison.md
```

For the two llama.cpp servers, the defaults work:

```bash
python scripts/compare.py --eval recipes/json-extractor/data/eval.jsonl
```

The script sends all messages except the final reference answer. It writes a Markdown table and raw JSON with both actual outputs. Temperature is zero. `LOCAL_API_KEY` can authenticate to endpoints that require it.

The cloud notebooks run this comparison directly before export and save `run-evidence.zip`. It contains all 10 held-out results, settings, timings and data hashes.

## Score the task

Write the rubric before looking at outputs. JSON extraction: parseability and exact field accuracy. SQL: execute read-only queries in a disposable database and compare results. Commit messages: factual changes and convention. Support: grounded claims and correct abstention. Report a count such as correct / total only after doing the scoring.

Include hard cases, unrelated questions, long inputs and malicious instructions embedded in task data. Record every failure, not just your favorite answers. Use the separately authored evaluation scenarios, then add examples from your own task.

Record base revision, data split, seed, hardware, software versions, quantization, runtime, training duration and output length. Re-evaluate the quantized model, not just the merged weights.

Advanced: [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) helps measure general capabilities and regressions. Its benchmark scores complement your task tests; they do not replace them.

Next: [Quantize](05-quantize.md).
