"""Unit tests for chapter04.rag_minimal (Listing 4.4)."""
from __future__ import annotations

from chapter04.rag_minimal import MinimalRAG, hash_embed, stub_llm


def _build_rag() -> MinimalRAG:
    return MinimalRAG(
        embed=lambda texts: hash_embed(texts, dim=256),
        chunk_size=20,
        chunk_overlap=5,
    )


def test_chunker_returns_single_chunk_for_short_text():
    rag = _build_rag()
    chunks = rag._chunk("a b c d e")
    assert chunks == ["a b c d e"]


def test_chunker_splits_long_text_with_overlap():
    rag = _build_rag()
    text = " ".join(f"w{i}" for i in range(50))
    chunks = rag._chunk(text)
    assert len(chunks) >= 2
    # Check that consecutive chunks overlap (last words of one appear in the next).
    first_tail = chunks[0].split()[-rag.chunk_overlap :]
    second_head = chunks[1].split()[: rag.chunk_overlap]
    assert any(tok in second_head for tok in first_tail)


def test_ingest_then_retrieve_returns_relevant_chunk():
    rag = _build_rag()
    rag.ingest(
        [
            {
                "id": "billing_001",
                "title": "Refund policy",
                "text": "Customers may request a refund within 30 days of the charge date.",
            },
            {
                "id": "login_001",
                "title": "Password reset flow",
                "text": "Password reset emails expire after 24 hours from the time they are sent.",
            },
        ]
    )
    results = rag.retrieve("how do refunds work", k=2)
    assert len(results) >= 1
    assert results[0]["metadata"]["id"] == "billing_001"


def test_retrieve_on_empty_index_returns_empty():
    rag = _build_rag()
    assert rag.retrieve("anything", k=3) == []


def test_retrieve_zero_k_returns_empty():
    rag = _build_rag()
    rag.ingest([{"id": "a", "title": "t", "text": "some text here"}])
    assert rag.retrieve("query", k=0) == []


def test_answer_uses_stub_llm_and_returns_payload():
    rag = _build_rag()
    rag.ingest(
        [
            {
                "id": "api_001",
                "title": "API rate limits",
                "text": "The Standard tier allows 1,000 requests per minute. Above this the API returns 429.",
            }
        ]
    )
    result = rag.answer("what is the standard rate limit", stub_llm, k=1)
    assert "query" in result
    assert "prompt" in result
    assert result["retrieved"], "retrieval must return at least one chunk"
    assert "stub answer" in result["answer"]


def test_metadata_carried_through_chunks():
    rag = _build_rag()
    rag.ingest(
        [
            {
                "id": "doc_x",
                "title": "Some title",
                "text": " ".join(f"word{i}" for i in range(60)),
            }
        ]
    )
    assert all(meta["id"] == "doc_x" for meta in rag.metadata)
    assert all(meta["title"] == "Some title" for meta in rag.metadata)
