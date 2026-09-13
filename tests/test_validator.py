"""Unit tests for the schedule constraint validator."""
import sys
from pathlib import Path
from typing import Tuple

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.constraints.validator import REQUIRED_SUBJECT_CODES, validate_schedule
from src.models.exam_slot import ExamSlot
from src.models.schedule import Schedule
from src.models.subject import Subject


@pytest.fixture
def default_subjects() -> Tuple[Subject, ...]:
    """Provide the 5 research subjects."""
    return (
        Subject(name="Mathematics", code="M", difficulty=5),
        Subject(name="Physics", code="P", difficulty=5),
        Subject(name="Chemistry", code="C", difficulty=4),
        Subject(name="Computer Science", code="CS", difficulty=3),
        Subject(name="English", code="E", difficulty=3),
    )


@pytest.fixture
def default_slots() -> Tuple[ExamSlot, ...]:
    """Provide the 5 standard exam slots."""
    return tuple(ExamSlot(day=d, session="Morning") for d in range(1, 6))


def test_valid_schedule_passes_validation(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that a standard valid schedule passes validation and returns True."""
    schedule = Schedule(subjects=default_subjects, slots=default_slots)
    assert validate_schedule(schedule) is True


def test_missing_or_wrong_subject_raises_value_error(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that replacing a required subject (e.g. English with Biology) raises ValueError."""
    # Replace English ('E') with Biology ('B')
    biology = Subject(name="Biology", code="B", difficulty=3)
    modified_subjects = (
        default_subjects[0],
        default_subjects[1],
        default_subjects[2],
        default_subjects[3],
        biology,
    )
    schedule = Schedule(subjects=modified_subjects, slots=default_slots)
    with pytest.raises(ValueError, match="Missing required subjects"):
        validate_schedule(schedule)


def test_custom_required_codes_missing_subject(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that specifying custom required codes detects missing subjects."""
    schedule = Schedule(subjects=default_subjects, slots=default_slots)
    custom_required = {"M", "P", "C", "CS", "E", "HIST"}
    with pytest.raises(ValueError, match="Missing required subjects.*HIST"):
        validate_schedule(schedule, required_codes=custom_required)


def test_duplicate_subject_handled(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that duplicate subjects raise ValueError in validate_schedule."""
    # Bypass Schedule.__post_init__ to test validate_schedule defense-in-depth
    mock_schedule = object.__new__(Schedule)
    duplicate_subjects = (
        default_subjects[0],
        default_subjects[1],
        default_subjects[2],
        default_subjects[3],
        default_subjects[0],  # Duplicate 'M'
    )
    object.__setattr__(mock_schedule, "subjects", duplicate_subjects)
    object.__setattr__(mock_schedule, "slots", default_slots)

    with pytest.raises(ValueError, match="Duplicate subjects found"):
        validate_schedule(mock_schedule)


def test_exactly_five_subjects_constraint(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that validate_schedule enforces exactly 5 subjects."""
    # Test 4 subjects
    mock_schedule = object.__new__(Schedule)
    object.__setattr__(mock_schedule, "subjects", default_subjects[:4])
    object.__setattr__(mock_schedule, "slots", default_slots)

    with pytest.raises(ValueError, match="Schedule must contain exactly 5 subjects, got 4"):
        validate_schedule(mock_schedule)

    # Test 6 subjects
    extra_subject = Subject(name="Biology", code="B", difficulty=3)
    mock_schedule_6 = object.__new__(Schedule)
    object.__setattr__(mock_schedule_6, "subjects", default_subjects + (extra_subject,))
    object.__setattr__(mock_schedule_6, "slots", default_slots)

    with pytest.raises(ValueError, match="Schedule must contain exactly 5 subjects, got 6"):
        validate_schedule(mock_schedule_6)


def test_exactly_five_slots_constraint(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that validate_schedule enforces exactly 5 slots."""
    mock_schedule = object.__new__(Schedule)
    object.__setattr__(mock_schedule, "subjects", default_subjects)
    object.__setattr__(mock_schedule, "slots", default_slots[:4])

    with pytest.raises(ValueError, match="Schedule must contain exactly 5 slots, got 4"):
        validate_schedule(mock_schedule)


def test_duplicate_exam_days_handled(
    default_subjects: Tuple[Subject, ...],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that validate_schedule detects duplicate exam days."""
    mock_schedule = object.__new__(Schedule)
    duplicate_day_slots = (
        default_slots[0],
        default_slots[0],  # Day 1 duplicated
        default_slots[2],
        default_slots[3],
        default_slots[4],
    )
    object.__setattr__(mock_schedule, "subjects", default_subjects)
    object.__setattr__(mock_schedule, "slots", duplicate_day_slots)

    with pytest.raises(ValueError, match="Duplicate exam days found"):
        validate_schedule(mock_schedule)
