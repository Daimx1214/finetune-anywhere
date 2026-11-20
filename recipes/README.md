# Recipes

Start with one narrow task. Every recipe includes original MIT-licensed chat data, a configuration, and separate train, validation and evaluation files.

| Recipe | What to measure |
| --- | --- |
| [Commit message writer](commit-message-writer/) | Correct type and scope; no invented changes |
| [JSON extractor](json-extractor/) | Valid JSON, exact keys, correct values |
| [SQL generator](sql-generator/) | Result correctness on a disposable database |
| [Support bot from docs](support-bot-from-docs/) | Grounded answers and abstention |

Each dataset contains 60 separately authored scenarios: 40 training, 10 validation and 10 held-out evaluation examples. They include edge cases and distinct tasks within each recipe, rather than repeated templates with substituted identifiers. All sample data is original and MIT-licensed.

Strong community recipes can be promoted here with their builders' credit and permission. Include real measurements, data provenance and an honest failure analysis.
