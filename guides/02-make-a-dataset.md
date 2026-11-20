# Make a dataset

Start with 100 to 500 high-quality examples of one task. Hold out 10 to 20 examples for final evaluation. Use a separate validation split for changing training settings. Split by source document, customer, repository or time when related examples could leak across splits.

## Chat JSONL

Each line is one JSON object. Use an optional system message, then alternating user and assistant messages. Finish with an assistant answer.

```json
{"messages":[{"role":"system","content":"Return only the requested label."},{"role":"user","content":"The parcel arrived broken."},{"role":"assistant","content":"damaged"}]}
```

Use the same system instructions during evaluation and deployment. Keep the full conversations short enough for the configured sequence length.

## Convert existing material

CSV input needs `question` and `answer` columns. JSON input is an array of objects with those keys. Text input uses `Q: ` and `A: ` lines, with a blank line between pairs. Custom CSV column names are supported.

Create a small CSV, then convert it:

```bash
mkdir -p outputs
python -c 'import csv; f=open("outputs/pairs.csv","w",newline=""); w=csv.writer(f); w.writerow(["question","answer"]); w.writerow(["What is two plus two?","Four."]); f.close()'
python scripts/convert_to_chat.py outputs/pairs.csv outputs/chat.jsonl --format csv
python scripts/validate_dataset.py outputs/chat.jsonl
```

Raw docs and notes are not automatically good chat examples. Write grounded question/answer pairs from them first. Include the relevant passage in the user message, and add questions the passage cannot answer. The converter intentionally does not invent answers from raw text.

## Validate before training

```bash
python scripts/validate_dataset.py recipes/json-extractor/data/train.jsonl recipes/json-extractor/data/valid.jsonl recipes/json-extractor/data/eval.jsonl
python scripts/validate_dataset.py recipes/json-extractor/data/train.jsonl --tokenizer starter --max-tokens 1024
```

The first command checks JSON, roles, nonempty content, duplicate examples, repeated prompts and exact prompt leakage across files. It prints character-based token estimates. The second uses the actual tokenizer and chat template. Exact matching cannot detect paraphrased leakage; review the split yourself.

Only use data you have the right to use. Remove credentials, private messages and personal details. Synthetic examples from a larger model are allowed if its terms permit your use. Review every target for accuracy and diversity. A hundred copies of one pattern are not a hundred different skills.

Next: [Train](03-train.md).
