"""Unit tests for the Subject model."""
import dataclasses
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.subject import Subject


def test_valid_subject_creation() -> None:
    """Test valid subject creation with Mathematics."""
    subject = Subject(name="Mathematics", code="M", difficulty=5)
    assert subject.name == "Mathematics"
    assert subject.code == "M"
    assert subject.difficulty == 5


def test_all_five_research_subjects_create_successfully() -> None:
    """Test that all 5 research subjects can be instantiated successfully."""
    research_subjects = [
        ("Mathematics", "M", 5),
        ("Physics", "P", 5),
        ("Chemistry", "C", 4),
        ("Computer Science", "CS", 3),
        ("English", "E", 3),
    ]
    created = [
        Subject(name=name, code=code, difficulty=diff)
        for name, code, diff in research_subjects
    ]
    assert len(created) == 5
    for sub, (name, code, diff) in zip(created, research_subjects):
        assert sub.name == name
        assert sub.code == code
        assert sub.difficulty == diff


@pytest.mark.parametrize("invalid_difficulty", [0, 6, -1, 3.5, 10, -5])
def test_invalid_difficulty_raises_value_error(invalid_difficulty: object) -> None:
    """Test that difficulty outside 1-5 or non-integer raises ValueError."""
    with pytest.raises(ValueError, match="Difficulty must be an integer between 1 and 5"):
        Subject(name="Mathematics", code="M", difficulty=invalid_difficulty)  # type: ignore[arg-type]


@pytest.mark.parametrize("empty_name", ["", "   ", "\t\n"])
def test_empty_or_whitespace_name_raises_value_error(empty_name: str) -> None:
    """Test that an empty or whitespace name raises ValueError."""
    with pytest.raises(ValueError, match="Subject name must be a non-empty string"):
        Subject(name=empty_name, code="M", difficulty=5)


@pytest.mark.parametrize("empty_code", ["", "   ", "\t\n"])
def test_empty_or_whitespace_code_raises_value_error(empty_code: str) -> None:
    """Test that an empty or whitespace code raises ValueError."""
    with pytest.raises(ValueError, match="Subject code must be a non-empty string"):
        Subject(name="Mathematics", code=empty_code, difficulty=5)


def test_subject_is_frozen() -> None:
    """Test that Subject instances are immutable."""
    subject = Subject(name="Mathematics", code="M", difficulty=5)
    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        subject.difficulty = 4  # type: ignore[misc]

    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        subject.name = "Applied Mathematics"  # type: ignore[misc]

    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        subject.code = "AM"  # type: ignore[misc]


def test_subject_repr_contains_code_and_difficulty() -> None:
    """Test that Subject repr representation contains the code and difficulty."""
    subject = Subject(name="Mathematics", code="M", difficulty=5)
    repr_str = repr(subject)
    assert "M" in repr_str
    assert "5" in repr_str
    assert repr_str == "Subject(M, difficulty=5)"
