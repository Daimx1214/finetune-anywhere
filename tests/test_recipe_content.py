"""Check authored targets against their stated output contracts and SQLite schemas."""

import json
import sqlite3

import pytest

from common import ROOT, read_rows, registry
from configure_chat import configure_tokenizer, NON_THINKING_PREFIX


@pytest.mark.parametrize("split", ["train", "valid", "eval"])
def test_extraction_targets_obey_contract(split):
    rows = read_rows(ROOT / "recipes/json-extractor/data" / f"{split}.jsonl")
    for row in rows:
        target = json.loads(row["messages"][-1]["content"])
        assert set(target) == {"item", "quantity", "priority"}
        assert target["item"] is None or isinstance(target["item"], str)
        assert target["quantity"] is None or (type(target["quantity"]) is int and target["quantity"] >= 0)
        assert target["priority"] in {"normal", "urgent"}
    # Missing fields and explicit urgency are present in every split.
    targets = [json.loads(row["messages"][-1]["content"]) for row in rows]
    assert any(t["quantity"] is None for t in targets)
    assert any(t["priority"] == "urgent" for t in targets)


def sql_parts(row):
    question = row["messages"][-2]["content"]
    schema = question.removeprefix("Schema:\n").split("\nQuestion: ", 1)[0]
    return schema, row["messages"][-1]["content"]


@pytest.mark.parametrize("split", ["train", "valid", "eval"])
def test_sql_targets_execute_against_the_supplied_schema(split):
    for row in read_rows(ROOT / "recipes/sql-generator/data" / f"{split}.jsonl"):
        schema, query = sql_parts(row)
        with sqlite3.connect(":memory:") as db:
            db.executescript(schema)
            # SQLite enforces read-only queries after the schema is created.
            db.execute("PRAGMA query_only = ON")
            assert query.startswith("SELECT ")
            db.execute(query).fetchall()


def test_heldout_sql_handles_empty_groups_nulls_and_date_boundaries():
    rows = read_rows(ROOT / "recipes/sql-generator/data/eval.jsonl")
    cases = [
        (
            0,
            "INSERT INTO warehouses VALUES (1,'Full'),(2,'Empty'); INSERT INTO bins VALUES (10,1),(11,1);",
            [(1, "Full", 2), (2, "Empty", 0)],
        ),
        (
            1,
            "INSERT INTO parcels VALUES (1,'2026-01-01',NULL),(2,'2026-01-01','2026-01-01'),(3,'2026-01-01','2026-01-02');",
            [(1,)],
        ),
        (
            6,
            "INSERT INTO sensor_readings VALUES (1,'2026-09-01',2),(2,'2026-09-07',4),(3,'2026-09-08',90);",
            [(3.0,)],
        ),
        (8, "", [(0,)]),
    ]
    for index, inserts, expected in cases:
        schema, query = sql_parts(rows[index])
        with sqlite3.connect(":memory:") as db:
            db.executescript(schema + inserts)
            assert db.execute(query).fetchall() == expected


def test_registry_only_exposes_apache_text_models_as_aliases():
    data = registry()
    assert data["default"] == "starter"
    assert {model["params_b"] for model in data["models"].values()} == {0.6, 1.7, 4.0}
    for model in data["models"].values():
        assert model["license"] == "Apache-2.0"
        assert model["modality"] == "text"
        assert model["enable_thinking"] is False
    assert all(m["license"] == "Apache-2.0" for m in data["reviewed_multimodal"])


def test_template_configuration_is_idempotent_and_rejects_wrong_family():
    class Tokenizer:
        chat_template = "{% if enable_thinking %}reason{% endif %}{{ messages }}"

    tokenizer = Tokenizer()
    original = tokenizer.chat_template
    configure_tokenizer(tokenizer)
    configure_tokenizer(tokenizer)
    assert tokenizer.chat_template == NON_THINKING_PREFIX + original
    tokenizer.chat_template = "a different model family"
    with pytest.raises(ValueError, match="Qwen3"):
        configure_tokenizer(tokenizer)
