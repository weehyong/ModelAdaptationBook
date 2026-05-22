"""Listing 4.2 -- Many-shot prompt assembly with similarity-based selection.

Build a many-shot prompt by selecting the ``k`` examples whose ticket text
is most similar to the incoming query.  The default similarity backend is
``sentence-transformers`` (CPU-friendly, ~30 ms per query for ``k=50`` on
a small bank).  A ``hash`` backend is provided for environments without
sentence-transformers and for unit tests; it uses a token-overlap score
as a stand-in for embedding similarity.

Run from code/:

    # Sentence-transformers backend (CPU, default):
    python -m chapter04.many_shot_demo \
        --bank chapter04/data/example_bank.jsonl \
        --query "I cannot log in after the password reset email" \
        --shots 20

    # Token-overlap backend (no sentence-transformers needed):
    python -m chapter04.many_shot_demo \
        --bank chapter04/data/example_bank.jsonl \
        --query "Refund the duplicate charge" \
        --shots 10 --backend hash
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Callable, Dict, List, Sequence

import numpy as np

from common.jsonl import read_jsonl_list

from chapter04 import DEFAULT_SYSTEM_INSTRUCTION


# ---------------------------------------------------------------------------
# Similarity backends
# ---------------------------------------------------------------------------


def _tokenize(text: str) -> List[str]:
    return re.sub(r"[^a-z0-9\s]", " ", text.lower()).split()


def hash_similarity(bank_texts: Sequence[str], query: str) -> np.ndarray:
    """Token-overlap fallback similarity (no embedding model required).

    Returns a 1D numpy array of overlap scores in ``[0, 1]`` aligned to
    ``bank_texts``.  Useful when sentence-transformers is unavailable and
    inside unit tests where deterministic output matters.
    """
    q_tokens = set(_tokenize(query))
    if not q_tokens:
        return np.zeros(len(bank_texts), dtype=np.float32)
    scores = np.zeros(len(bank_texts), dtype=np.float32)
    for i, text in enumerate(bank_texts):
        b_tokens = set(_tokenize(text))
        if not b_tokens:
            continue
        overlap = len(q_tokens & b_tokens)
        scores[i] = overlap / max(len(q_tokens | b_tokens), 1)
    return scores


def make_st_backend(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """Sentence-transformers similarity backend (cosine on normalised vectors)."""
    from sentence_transformers import SentenceTransformer

    embedder = SentenceTransformer(model_name)

    def similarity(bank_texts: Sequence[str], query: str) -> np.ndarray:
        bank_vecs = embedder.encode(list(bank_texts), normalize_embeddings=True)
        q_vec = embedder.encode([query], normalize_embeddings=True)[0]
        return np.asarray(bank_vecs @ q_vec, dtype=np.float32)

    return similarity


# ---------------------------------------------------------------------------
# Selection + assembly (Listing 4.2)
# ---------------------------------------------------------------------------


def select_by_similarity(
    bank: List[Dict[str, str]],
    query: str,
    k: int,
    *,
    similarity_fn: Callable[[Sequence[str], str], np.ndarray],
) -> List[Dict[str, str]]:
    """Pick the ``k`` examples whose ``ticket`` is most similar to ``query``.

    Returns the examples sorted from least similar to most similar.  The
    ordering puts the most relevant example last so the recency rule from
    section 4.2 lands without an extra sort step at the call site.
    """
    if k <= 0:
        return []
    if k > len(bank):
        raise ValueError(f"Requested {k} examples but the bank only has {len(bank)}.")
    scores = similarity_fn([ex["ticket"] for ex in bank], query)
    order = np.argsort(scores)[-k:]  # ascending by score, top-k
    return [bank[i] for i in order]


def assemble_prompt(
    bank: List[Dict[str, str]],
    query: str,
    *,
    k: int = 50,
    similarity_fn: Callable[[Sequence[str], str], np.ndarray],
) -> str:
    """Build a many-shot prompt: instruction, ``k`` selected examples, then the query."""
    selected = select_by_similarity(bank, query, k=k, similarity_fn=similarity_fn)
    parts = [DEFAULT_SYSTEM_INSTRUCTION, ""]
    for ex in selected:
        parts.append(f"Ticket: {ex['ticket']}\nCategory: {ex['category']}\n")
    parts.append(f"Ticket: {query}\nCategory:")
    return "\n".join(parts)


def estimate_prompt_tokens(prompt: str) -> int:
    """Rough token estimate (1 token ~ 4 characters of English text)."""
    return max(1, len(prompt) // 4)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


SIMILARITY_BACKENDS = {
    "st": lambda: make_st_backend(),
    "hash": lambda: hash_similarity,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Many-shot prompt assembly (chapter 4)")
    parser.add_argument(
        "--bank",
        default="chapter04/data/example_bank.jsonl",
        help="JSONL file with `ticket` and `category` fields",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="The ticket text to classify (used to drive similarity selection)",
    )
    parser.add_argument("--shots", type=int, default=20, help="How many examples to include")
    parser.add_argument(
        "--backend",
        choices=sorted(SIMILARITY_BACKENDS),
        default="st",
        help="Similarity backend (st = sentence-transformers, hash = token overlap)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write the assembled prompt as text",
    )
    args = parser.parse_args()

    bank = read_jsonl_list(args.bank)
    similarity_fn = SIMILARITY_BACKENDS[args.backend]()

    prompt = assemble_prompt(
        bank, args.query, k=min(args.shots, len(bank)), similarity_fn=similarity_fn
    )
    tokens = estimate_prompt_tokens(prompt)

    print(f"Backend:           {args.backend}")
    print(f"Examples selected: {min(args.shots, len(bank))}")
    print(f"Prompt characters: {len(prompt)}")
    print(f"Prompt tokens:     ~{tokens}")
    print()
    print("Last 600 characters of the assembled prompt:")
    print("-" * 60)
    print(prompt[-600:])

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(prompt, encoding="utf-8")
        print(f"\nFull prompt written to {args.output}")


if __name__ == "__main__":
    main()
