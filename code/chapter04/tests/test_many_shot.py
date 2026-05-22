"""Unit tests for chapter04.many_shot_demo (Listing 4.2)."""
from __future__ import annotations

import numpy as np

from chapter04.many_shot_demo import (
    assemble_prompt,
    estimate_prompt_tokens,
    hash_similarity,
    select_by_similarity,
)


def test_hash_similarity_orders_relevant_first():
    bank_texts = [
        "I cannot log in after the password reset email",
        "Refund the duplicate billing charge on my invoice",
        "The mobile app crashes on launch on iOS",
    ]
    scores = hash_similarity(bank_texts, "my password reset email did not work")
    assert scores.shape == (3,)
    # Login text is most relevant; billing and mobile should both score lower.
    assert int(np.argmax(scores)) == 0


def test_select_by_similarity_returns_most_relevant_last():
    bank = [
        {"ticket": "I cannot log in after the password reset email", "category": "login"},
        {"ticket": "Refund the duplicate billing charge on my invoice", "category": "billing"},
        {"ticket": "The mobile app crashes on launch on iOS", "category": "mobile"},
    ]
    selected = select_by_similarity(
        bank, "my password reset email did not work", k=3, similarity_fn=hash_similarity
    )
    # Must contain all three in some order, with the most relevant last.
    assert len(selected) == 3
    assert selected[-1]["category"] == "login"


def test_select_by_similarity_respects_k():
    bank = [
        {"ticket": "ticket one", "category": "a"},
        {"ticket": "ticket two", "category": "b"},
        {"ticket": "ticket three", "category": "c"},
    ]
    out = select_by_similarity(bank, "two", k=2, similarity_fn=hash_similarity)
    assert len(out) == 2


def test_select_by_similarity_rejects_oversized_k():
    bank = [{"ticket": "only one", "category": "a"}]
    try:
        select_by_similarity(bank, "anything", k=5, similarity_fn=hash_similarity)
    except ValueError:
        return
    raise AssertionError("Expected ValueError when k > len(bank)")


def test_assemble_prompt_includes_query_at_end():
    bank = [
        {"ticket": "I cannot log in after the password reset email", "category": "login"},
        {"ticket": "Refund the duplicate billing charge on my invoice", "category": "billing"},
    ]
    prompt = assemble_prompt(
        bank,
        "my password reset email did not work",
        k=2,
        similarity_fn=hash_similarity,
    )
    # The final query should be the last "Ticket:" block in the prompt.
    last_ticket = prompt.rsplit("Ticket:", 1)[-1]
    assert "my password reset email did not work" in last_ticket
    assert prompt.rstrip().endswith("Category:")


def test_estimate_prompt_tokens_is_positive():
    assert estimate_prompt_tokens("hello world") >= 1
    assert estimate_prompt_tokens("a" * 4000) > 500
