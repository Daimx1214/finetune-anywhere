# Recipes

Start with one narrow task. Every recipe includes original MIT-licensed chat data, a configuration, and separate train, validation and evaluation files.

| Recipe | What to measure |
| --- | --- |
| [Commit message writer](commit-message-writer/) | Correct type and scope; no invented changes |
| [JSON extractor](json-extractor/) | Valid JSON, exact keys, correct values |
| [SQL generator](sql-generator/) | Result correctness on a disposable database |
| [Support bot from docs](support-bot-from-docs/) | Grounded answers and abstention |

These are teaching datasets, not benchmarks. They are intentionally small and repetitive. Expand coverage and test on independently written examples. Fine-tuning changes behavior; retrieval is usually the better way to supply changing facts.

Strong community recipes can be promoted here with their builders' credit and permission. Include real measurements, data provenance and an honest failure analysis.
