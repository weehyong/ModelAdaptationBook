"""Tests for chat data normalization and format conversion."""
from chapter05.data import normalize_row_to_chat_example


def test_normalize_messages_adds_system_prompt_if_missing():
    row = {"messages": [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]}
    ex = normalize_row_to_chat_example(row, system_prompt="SYS", context="t")
    assert ex.messages[0]["role"] == "system"
    assert ex.messages[0]["content"] == "SYS"


def test_normalize_prompt_response_to_messages():
    row = {"prompt": "Question", "response": "Answer"}
    ex = normalize_row_to_chat_example(row, system_prompt="SYS", context="t")
    assert [m["role"] for m in ex.messages] == ["system", "user", "assistant"]
    assert ex.messages[1]["content"] == "Question"
    assert ex.messages[2]["content"] == "Answer"

