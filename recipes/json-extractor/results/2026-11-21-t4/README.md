# Colab T4 run: 21 November 2026

The maintainer trained the `starter` Qwen3 1.7B model with the JSON extractor recipe on a Tesla T4. All three dataset SHA-256 hashes match the repository data, and all ten recorded prompts and references match the held-out evaluation split.

## Measured results

| Measure | Before training | After training |
| --- | --- | --- |
| Parses directly as JSON | 8/10 | 10/10 |
| Correct keys and allowed field types/values | 7/10 | 9/10 |
| Exact reference match | 2/10 | 7/10 |
| Correct item | 6/10 | 7/10 |
| Correct quantity | 5/10 | 10/10 |
| Correct priority | 5/10 | 9/10 |

Scores use the raw response with `json.loads`, without removing Markdown fences. Field scores count an unparseable response as incorrect. Exact match compares parsed objects, including field types; whitespace and key order do not matter. Schema validity requires exactly item, quantity and priority, a string or null item, a nonnegative integer or null quantity, and normal or urgent priority.

Training took **80.14 seconds** around the trainer call (trainer-reported runtime: 78.53 seconds), with **4.51 GB / 4.20 GiB** peak PyTorch allocated GPU memory. The run used 40 training examples, 10 validation examples, three epochs and 30 optimizer steps. Final validation loss was 0.4560. Rank was 16, alpha 32, learning rate 0.0002, sequence limit 1024 and effective batch size 4. Generation was greedy, limited to 256 new tokens, with thinking disabled.

## Actual before and after

Prompt: “I was going to ask for 12 display easels, but the final approved number is 9.”

Before:

```json
{"item": "display easels", "quantity": null, "priority": "normal"}
```

After, matching the reference:

```json
{"item": "display easels", "quantity": 9, "priority": "normal"}
```

Three responses still differ from their references:

- Foot pedals: the tuned item includes “for the transcription desks”.
- Cable ties: the tuned item omits “bundles of”.
- Same-day replacement request: the tuned item is “replacement part” instead of null, and priority is “same-day” instead of urgent.

[All ten before/after responses](comparison.md) include every success and failure. [Interpretation and export status](../../../../MAINTAINER_NOTES.md#recorded-t4-run) explain the scope of this result.

## Evidence

- [Original run metadata](run.json): settings, actual loaded revision, software versions, hardware, timings and dataset hashes.
- [Raw comparisons](comparison.json): prompts, references and unchanged model responses.
- [Training log](training-log.json): losses and steps.
- [Provenance](provenance.json): source archive checksum and checksums for the four unchanged evidence files.

The source notebook came from repository commit `c1074b66c661a61a9a69435870fb9e664aa0f38c`. The run metadata records both the loaded base revision and the reviewed catalog revision.
