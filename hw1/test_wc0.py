import json
import wc0_fixed as wc

"""
Bonus Task 3
Unit tests for wc0_fixed.py

These tests verify that all model functions are:
- Pure
- Policy-free
- Deterministic

"""

def test_clean_word():
    assert wc.clean_word("hello,", ".,") == "hello"
    assert wc.clean_word("world!", "!") == "world"
    assert wc.clean_word("clean", ".,") == "clean"


def test_valid_word():
    stopwords = {"the", "and"}
    assert wc.valid_word("cat", stopwords)
    assert not wc.valid_word("the", stopwords)
    assert not wc.valid_word("", stopwords)


def test_normalize():
    assert wc.normalize("Hello WORLD") == "hello world"


def test_tokenize():
    assert wc.tokenize("one two three") == ["one", "two", "three"]


def test_get_counts_no_stopwords():
    words = ["cat", "dog", "cat"]
    stopwords = set()
    counts = wc.get_counts(words, stopwords, "")
    assert counts == {"cat": 2, "dog": 1}


def test_get_counts_with_stopwords():
    words = ["the", "cat", "and", "the", "dog"]
    stopwords = {"the"}
    counts = wc.get_counts(words, stopwords, "")
    assert counts == {"cat": 1, "and": 1, "dog": 1}


def test_get_counts_with_punctuation():
    words = ["hello,", "hello!", "world."]
    stopwords = set()
    counts = wc.get_counts(words, stopwords, ".,!")
    assert counts == {"hello": 2, "world": 1}


def test_sort_counts():
    counts = {"a": 1, "b": 3, "c": 2}
    sorted_counts = wc.sort_counts(counts)
    assert sorted_counts == [("b", 3), ("c", 2), ("a", 1)]


def test_total_words():
    counts = {"a": 2, "b": 3}
    assert wc.total_words(counts) == 5


def test_toJSON():
    result = {
        "total": 3,
        "unique": 2,
        "counts": {"a": 2, "b": 1},
        "top": [("a", 2), ("b", 1)]
    }
    data = json.loads(wc.toJSON(result))
    assert data["total"] == 3
    assert data["counts"]["a"] == 2


def test_toCSV():
    result = {
        "top": [("hello", 2), ("world", 1)]
    }
    csv_text = wc.toCSV(result)
    lines = csv_text.strip().splitlines()
    assert lines[0] == "word,count"
    assert "hello,2" in lines
    assert "world,1" in lines
