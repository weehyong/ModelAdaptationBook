"""Unit tests for chapter04.prompt_validator (Listing 4.3)."""
from __future__ import annotations

from typing import Dict, List

from chapter04.few_shot_demo import make_mock_backend
from chapter04.prompt_validator import ValidationReport, validate_prompt


def test_validation_report_shape():
    bank = [
        {"ticket": "Refund my duplicate charge", "category": "billing"},
        {"ticket": "Cannot log in after reset", "category": "login"},
    ]
    test_set = [
        {"ticket": "Please refund the duplicate charge", "category": "billing"},
        {"ticket": "Password reset link expired", "category": "login"},
    ]
    backend = make_mock_backend()
    report = validate_prompt(bank, test_set, backend=backend, runs=3)
    assert isinstance(report, ValidationReport)
    assert len(report.accuracy_runs) == 3
    assert len(report.per_example_consistency) == 2
    assert len(report.per_example_predictions) == 2
    assert all(len(preds) == 3 for preds in report.per_example_predictions)


def test_validator_perfect_accuracy_on_deterministic_backend():
    bank = [
        {"ticket": "Refund my duplicate charge", "category": "billing"},
        {"ticket": "Cannot log in after reset", "category": "login"},
    ]
    test_set = [
        {"ticket": "Please refund the duplicate charge", "category": "billing"},
        {"ticket": "Password reset link expired", "category": "login"},
    ]
    backend = make_mock_backend()
    report = validate_prompt(bank, test_set, backend=backend, runs=4)
    # The mock backend is deterministic, so disagreement should be zero.
    assert report.accuracy_mean == 1.0
    assert report.disagreement_rate == 0.0
    assert all(c == 1.0 for c in report.per_example_consistency)


def test_validator_detects_disagreement_with_flaky_backend():
    """A backend that flips between two answers should drive disagreement up."""
    state: Dict[str, int] = {"call": 0}

    def flaky_backend(messages: List[Dict[str, str]]) -> str:
        state["call"] += 1
        return "billing" if state["call"] % 2 == 0 else "login"

    bank = [{"ticket": "anything", "category": "billing"}]
    test_set = [{"ticket": "first case", "category": "billing"}]
    report = validate_prompt(bank, test_set, backend=flaky_backend, runs=4)
    # Two distinct answers across runs means the test case is in the
    # disagreement bucket and consistency drops below 1.
    assert report.disagreement_rate == 1.0
    assert report.per_example_consistency[0] < 1.0


def test_validator_rejects_zero_runs():
    bank = [{"ticket": "x", "category": "billing"}]
    test_set = [{"ticket": "y", "category": "billing"}]
    backend = make_mock_backend()
    try:
        validate_prompt(bank, test_set, backend=backend, runs=0)
    except ValueError:
        return
    raise AssertionError("Expected ValueError on runs=0")
