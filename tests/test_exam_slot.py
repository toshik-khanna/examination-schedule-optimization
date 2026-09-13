"""Unit tests for the ExamSlot model."""
import dataclasses
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.exam_slot import ExamSlot


def test_valid_exam_slot_creation() -> None:
    """Test creating a valid ExamSlot with day=1, session='Morning'."""
    slot = ExamSlot(day=1, session="Morning")
    assert slot.day == 1
    assert slot.session == "Morning"


def test_all_five_slots_create_successfully() -> None:
    """Test creating all 5 examination slots for days 1 through 5."""
    slots = [ExamSlot(day=d, session="Morning") for d in range(1, 6)]
    assert len(slots) == 5
    for i, slot in enumerate(slots, start=1):
        assert slot.day == i
        assert slot.session == "Morning"


@pytest.mark.parametrize("invalid_day", [0, 6, -1, 10, -5])
def test_invalid_day_raises_value_error(invalid_day: int) -> None:
    """Test that days outside 1-5 raise ValueError."""
    with pytest.raises(ValueError, match="Day must be between 1 and 5"):
        ExamSlot(day=invalid_day, session="Morning")


@pytest.mark.parametrize("invalid_session", ["Afternoon", "Evening", "", "morning", "Night"])
def test_invalid_session_raises_value_error(invalid_session: str) -> None:
    """Test that any session other than 'Morning' raises ValueError."""
    with pytest.raises(ValueError, match="Session must be one of"):
        ExamSlot(day=1, session=invalid_session)


def test_exam_slot_is_frozen() -> None:
    """Test that ExamSlot instances are immutable."""
    slot = ExamSlot(day=1, session="Morning")
    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        slot.day = 2  # type: ignore[misc]

    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        slot.session = "Afternoon"  # type: ignore[misc]


def test_exam_slot_repr() -> None:
    """Test string representation of ExamSlot."""
    slot = ExamSlot(day=3, session="Morning")
    assert repr(slot) == "ExamSlot(Day 3, Morning)"
