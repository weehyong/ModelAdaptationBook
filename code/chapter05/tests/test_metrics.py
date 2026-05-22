"""Tests for exact_match and token_f1 metrics."""
from chapter05.metrics import exact_match, token_f1


def test_exact_match_normalizes_whitespace_and_case():
    assert exact_match("Hello  world", "hello world") is True
    assert exact_match("Hello world", "hello") is False


def test_token_f1_basic_cases():
    assert token_f1("a b c", "a b c") == 1.0
    assert token_f1("a b", "c d") == 0.0
    assert 0.0 < token_f1("reset the thermostat", "reset thermostat") <= 1.0

