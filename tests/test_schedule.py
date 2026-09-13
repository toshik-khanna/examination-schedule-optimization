"""Unit tests for the Schedule model."""
import dataclasses
import sys
from pathlib import Path
from typing import Tuple

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.exam_slot import ExamSlot
from src.models.schedule import Schedule
from src.models.subject import Subject


@pytest.fixture
def default_subjects() -> Tuple[Subject, ...]:
    """Provide the 5 research subjects in standard order."""
    return (
        Subject(name="Mathematics", code="M", difficulty=5),
        Subject(name="Physics", code="P", difficulty=5),
        Subject(name="Chemistry", code="C", difficulty=4),
        Subject(name="Computer Science", code="CS", difficulty=3),
        Subject(name="English", code="E", difficulty=3),
    )


@pytest.fixture
def default_slots() -> Tuple[ExamSlot, ...]:
    """Provide the 5 standard morning examination slots."""
    return tuple(ExamSlot(day=d, session="Morning") for d in range(1, 6))


def test_valid_schedule_creation(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test valid schedule creation with 5 subjects and 5 slots."""
    schedule = Schedule(subjects=default_subjects, slots=default_slots)
    assert len(schedule.subjects) == 5
    assert len(schedule.slots) == 5
    assert schedule.subjects == default_subjects
    assert schedule.slots == default_slots


def test_subject_codes_property(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test subject_codes property returns the dash-separated string."""
    schedule = Schedule(subjects=default_subjects, slots=default_slots)
    assert schedule.subject_codes == "M-P-C-CS-E"


def test_difficulty_sequence_property(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test difficulty_sequence property returns the tuple of difficulty integers."""
    schedule = Schedule(subjects=default_subjects, slots=default_slots)
    assert schedule.difficulty_sequence == (5, 5, 4, 3, 3)


def test_duplicate_subject_raises_value_error(
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that a schedule with duplicate subjects raises ValueError."""
    duplicate_subjects = (
        Subject(name="Mathematics", code="M", difficulty=5),
        Subject(name="Physics", code="P", difficulty=5),
        Subject(name="Chemistry", code="C", difficulty=4),
        Subject(name="Computer Science", code="CS", difficulty=3),
        Subject(name="Mathematics", code="M", difficulty=5),  # duplicate M
    )
    with pytest.raises(ValueError, match="Schedule contains duplicate subjects"):
        Schedule(subjects=duplicate_subjects, slots=default_slots)


def test_duplicate_subject_code_with_different_name_raises_value_error(
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that subjects with duplicate codes raise ValueError even if names differ."""
    duplicate_code_subjects = (
        Subject(name="Mathematics", code="M", difficulty=5),
        Subject(name="Physics", code="P", difficulty=5),
        Subject(name="Chemistry", code="C", difficulty=4),
        Subject(name="Computer Science", code="CS", difficulty=3),
        Subject(name="Modern Mathematics", code="M", difficulty=4),  # same code 'M'
    )
    with pytest.raises(ValueError, match="Schedule contains duplicate subjects"):
        Schedule(subjects=duplicate_code_subjects, slots=default_slots)


def test_wrong_number_of_subjects_raises_value_error(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that fewer than 5 or more than 5 subjects raises ValueError."""
    # 4 subjects
    with pytest.raises(ValueError, match="Schedule must contain exactly 5 subjects"):
        Schedule(subjects=default_subjects[:4], slots=default_slots)

    # 6 subjects
    extra_subject = Subject(name="Biology", code="B", difficulty=4)
    with pytest.raises(ValueError, match="Schedule must contain exactly 5 subjects"):
        Schedule(subjects=default_subjects + (extra_subject,), slots=default_slots)


def test_wrong_number_of_slots_raises_value_error(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that fewer than 5 or more than 5 slots raises ValueError."""
    # 4 slots
    with pytest.raises(ValueError, match="Schedule must contain exactly 5 exam slots"):
        Schedule(subjects=default_subjects, slots=default_slots[:4])

    # 6 slots (using a valid ExamSlot requires day 1-5 so we construct with custom/duplicate slot)
    extra_slots = default_slots + (default_slots[0],)
    with pytest.raises(ValueError, match="Schedule must contain exactly 5 exam slots"):
        Schedule(subjects=default_subjects, slots=extra_slots)


def test_schedule_is_frozen(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that Schedule instances are immutable."""
    schedule = Schedule(subjects=default_subjects, slots=default_slots)
    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        schedule.subjects = default_subjects[::-1]  # type: ignore[misc]

    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        schedule.slots = default_slots  # type: ignore[misc]


def test_schedule_repr(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test string representation of Schedule."""
    schedule = Schedule(subjects=default_subjects, slots=default_slots)
    assert repr(schedule) == "Schedule(M-P-C-CS-E)"
