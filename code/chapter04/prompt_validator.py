"""Listing 4.3 -- Prompt validation harness with run-to-run variability.

Run a prompt template against a held-out test set ``runs`` times at the
configured temperature, then report mean accuracy, per-run accuracy,
disagreement rate, and per-example consistency.

The validator uses a thin ``ModelClient`` interface so it can be driven
by any backend (transformers, an API, or a stub for tests).  By default
it uses the same ``mock`` backend as ``few_shot_demo.py`` so the
validator can be exercised end to end on a CPU.

Run from code/:

    # Mock backend (CPU smoke test):
    python -m chapter04.prompt_validator \
        --bank chapter04/data/example_bank.jsonl \
        --test chapter04/data/held_out_test.jsonl \
        --shots 8 --runs 3 --backend mock

    # HF backend (GPU):
    python -m chapter04.prompt_validator \
        --bank chapter04/data/example_bank.jsonl \
        --test chapter04/data/held_out_test.jsonl \
        --shots 8 --runs 5 --backend hf
"""
from __future__ import annotations

import argparse
import json
import random
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Sequence

from common.jsonl import read_jsonl_list
from common.seed import seed_everything

from chapter04 import DEFAULT_MODEL_NAME
from chapter04.few_shot_demo import (
    BACKENDS,
    build_prompt,
    parse_category,
    stratified_sample,
)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class ValidationReport:
    """Summary of multiple validator runs."""

    accuracy_mean: float
    accuracy_runs: List[float] = field(default_factory=list)
    disagreement_rate: float = 0.0
    per_example_consistency: List[float] = field(default_factory=list)
    per_example_predictions: List[List[str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "accuracy_mean": round(self.accuracy_mean, 4),
            "accuracy_runs": [round(a, 4) for a in self.accuracy_runs],
            "disagreement_rate": round(self.disagreement_rate, 4),
            "per_example_consistency": [round(c, 4) for c in self.per_example_consistency],
            "per_example_predictions": self.per_example_predictions,
        }


# ---------------------------------------------------------------------------
# Validation core (Listing 4.3)
# ---------------------------------------------------------------------------


def validate_prompt(
    examples: Sequence[Dict[str, str]],
    test_set: Sequence[Dict[str, str]],
    *,
    backend: Callable[[List[Dict[str, str]]], str],
    runs: int = 5,
) -> ValidationReport:
    """Run each test case ``runs`` times and report accuracy + variability.

    Args:
        examples: The few-shot example bank (rendered into the prompt).
        test_set: Held-out test cases with ``ticket`` and ``category`` keys.
        backend: A callable that takes chat-format messages and returns the
            model's response as a string.  Sampling temperature, decoding
            params, and model loading are the backend's responsibility.
        runs: How many times to repeat each test case.

    Returns:
        A ``ValidationReport`` with mean accuracy, per-run accuracy,
        disagreement rate, and per-example consistency.
    """
    if runs < 1:
        raise ValueError("runs must be >= 1")

    all_outputs: List[List[str]] = [[] for _ in test_set]
    accuracies: List[float] = []
    for _ in range(runs):
        run_correct = 0
        for i, case in enumerate(test_set):
            messages = build_prompt(examples, case["ticket"])
            raw = backend(messages)
            prediction = parse_category(raw)
            all_outputs[i].append(prediction)
            if prediction == case["category"]:
                run_correct += 1
        accuracies.append(run_correct / max(len(test_set), 1))

    consistencies: List[float] = []
    disagreement_count = 0
    for outputs in all_outputs:
        most_common = Counter(outputs).most_common(1)[0][1]
        consistencies.append(most_common / runs)
        if most_common < runs:
            disagreement_count += 1

    return ValidationReport(
        accuracy_mean=sum(accuracies) / len(accuracies),
        accuracy_runs=accuracies,
        disagreement_rate=disagreement_count / max(len(test_set), 1),
        per_example_consistency=consistencies,
        per_example_predictions=all_outputs,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt validator (chapter 4)")
    parser.add_argument(
        "--bank",
        default="chapter04/data/example_bank.jsonl",
        help="JSONL file with `ticket` and `category` fields",
    )
    parser.add_argument(
        "--test",
        default="chapter04/data/held_out_test.jsonl",
        help="JSONL held-out test set",
    )
    parser.add_argument("--shots", type=int, default=8, help="Few-shot example count")
    parser.add_argument("--runs", type=int, default=5, help="How many times to repeat each case")
    parser.add_argument(
        "--backend",
        choices=sorted(BACKENDS),
        default="mock",
        help="Model backend (hf = transformers, mock = offline keyword classifier)",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL_NAME, help="HF model id (hf backend)")
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature for the hf backend (0 = greedy, no variability)",
    )
    parser.add_argument(
        "--output",
        default="chapter04/runs/validator_report.json",
        help="Where to write the validator report JSON",
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    seed_everything(args.seed)
    rng = random.Random(args.seed)

    bank = read_jsonl_list(args.bank)
    test_set = read_jsonl_list(args.test)
    if args.shots > len(bank):
        raise ValueError(
            f"Requested {args.shots} shots but the example bank only has {len(bank)} entries."
        )

    examples = stratified_sample(bank, args.shots, rng=rng)
    backend = BACKENDS[args.backend](args)

    print(f"Validating prompt: shots={args.shots} runs={args.runs} backend={args.backend}")
    started = time.time()
    report = validate_prompt(examples, test_set, backend=backend, runs=args.runs)
    elapsed = time.time() - started

    print()
    print("=" * 60)
    print("VALIDATION REPORT")
    print("=" * 60)
    print(f"Mean accuracy:       {report.accuracy_mean:.2%}")
    print(f"Per-run accuracy:    {[f'{a:.2%}' for a in report.accuracy_runs]}")
    print(f"Disagreement rate:   {report.disagreement_rate:.2%}")
    avg_consistency = (
        sum(report.per_example_consistency) / max(len(report.per_example_consistency), 1)
    )
    print(f"Mean consistency:    {avg_consistency:.2%}")
    print(f"Wall time:           {elapsed:.1f}s")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "shots": args.shots,
        "runs": args.runs,
        "backend": args.backend,
        "model": args.model if args.backend == "hf" else None,
        "temperature": args.temperature if args.backend == "hf" else None,
        "test_size": len(test_set),
        "wall_seconds": round(elapsed, 2),
        **report.to_dict(),
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nReport: {out_path}")


if __name__ == "__main__":
    main()
