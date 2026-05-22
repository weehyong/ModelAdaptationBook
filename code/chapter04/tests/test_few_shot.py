"""Unit tests for chapter04.few_shot_demo (Listing 4.1)."""
from __future__ import annotations

import random

from chapter04 import CATEGORIES, DEFAULT_SYSTEM_INSTRUCTION
from chapter04.few_shot_demo import (
    build_prompt,
    evaluate,
    format_example,
    make_mock_backend,
    parse_category,
    stratified_sample,
)


def test_format_example_round_trip():
    rendered = format_example("My card was charged twice.", "billing")
    assert rendered == "Ticket: My card was charged twice.\nCategory: billing"


def test_build_prompt_structure():
    examples = [
        {"ticket": "Refund the duplicate charge", "category": "billing"},
        {"ticket": "Cannot log in after reset", "category": "login"},
    ]
    messages = build_prompt(examples, "My password reset link expired.")
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == DEFAULT_SYSTEM_INSTRUCTION
    assert messages[1]["role"] == "user"
    user = messages[1]["content"]
    assert "Refund the duplicate charge" in user
    assert "Cannot log in after reset" in user
    assert user.rstrip().endswith("Category:")
    # Most-relevant-last: the second example must appear after the first.
    assert user.find("Refund the duplicate charge") < user.find("Cannot log in after reset")


def test_stratified_sample_covers_categories():
    bank = [
        {"ticket": f"ticket {i}", "category": cat}
        for cat in ("billing", "login", "integrations")
        for i in range(3)
    ]
    rng = random.Random(0)
    selected = stratified_sample(bank, shots=3, rng=rng)
    cats = {ex["category"] for ex in selected}
    assert cats == {"billing", "login", "integrations"}


def test_stratified_sample_deterministic_with_seed():
    bank = [
        {"ticket": f"ticket {i}", "category": cat}
        for cat in ("billing", "login")
        for i in range(4)
    ]
    a = stratified_sample(bank, shots=4, rng=random.Random(7))
    b = stratified_sample(bank, shots=4, rng=random.Random(7))
    assert a == b


def test_parse_category_known_label():
    for cat in CATEGORIES:
        assert parse_category(cat) == cat
        assert parse_category(f"{cat}.") == cat
        assert parse_category(f"  {cat}\nextra text") == cat


def test_parse_category_unknown_returns_lowercased():
    assert parse_category("WeirdLabel") == "weirdlabel"


def test_mock_backend_classifies_obvious_tickets():
    backend = make_mock_backend()
    result = backend(
        [
            {"role": "system", "content": "ignored"},
            {"role": "user", "content": "Ticket: please refund my duplicate charge\nCategory:"},
        ]
    )
    assert result == "billing"

    result_login = backend(
        [
            {"role": "system", "content": "ignored"},
            {"role": "user", "content": "Ticket: cannot log in after password reset\nCategory:"},
        ]
    )
    assert result_login == "login"


def test_evaluate_runs_full_pipeline_with_mock():
    bank = [
        {"ticket": "Refund my duplicate charge", "category": "billing"},
        {"ticket": "Cannot log in", "category": "login"},
    ]
    test_set = [
        {"ticket": "Please refund the duplicate charge", "category": "billing"},
        {"ticket": "Password reset link expired", "category": "login"},
    ]
    backend = make_mock_backend()
    report = evaluate(bank, test_set, backend)
    assert report["test_size"] == 2
    assert report["correct"] == 2
    assert report["top1_accuracy"] == 1.0
    assert len(report["rows"]) == 2
    assert all(row["correct"] for row in report["rows"])
