"""Unit tests for the schedule generator."""
import sys
from pathlib import Path
from typing import List, Tuple

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.algorithms.generator import generate_all_schedules
from src.models.exam_slot import ExamSlot
from src.models.schedule import Schedule
from src.models.subject import Subject


@pytest.fixture
def default_subjects() -> List[Subject]:
    """Provide the 5 research subjects."""
    return [
        Subject(name="Mathematics", code="M", difficulty=5),
        Subject(name="Physics", code="P", difficulty=5),
        Subject(name="Chemistry", code="C", difficulty=4),
        Subject(name="Computer Science", code="CS", difficulty=3),
        Subject(name="English", code="E", difficulty=3),
    ]


@pytest.fixture
def default_slots() -> Tuple[ExamSlot, ...]:
    """Provide the 5 standard exam slots."""
    return tuple(ExamSlot(day=d, session="Morning") for d in range(1, 6))


def test_generator_returns_list_of_schedule(
    default_subjects: List[Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that generator returns a list containing Schedule instances."""
    schedules = generate_all_schedules(default_subjects, default_slots)
    assert isinstance(schedules, list)
    assert all(isinstance(s, Schedule) for s in schedules)


def test_exactly_120_schedules_generated(
    default_subjects: List[Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that generate_all_schedules generates exactly 5! = 120 schedules."""
    schedules = generate_all_schedules(default_subjects, default_slots)
    assert len(schedules) == 120


def test_all_schedules_are_unique(
    default_subjects: List[Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that all 120 generated schedules have distinct subject code orderings."""
    schedules = generate_all_schedules(default_subjects, default_slots)
    code_sequences = [s.subject_codes for s in schedules]
    assert len(set(code_sequences)) == 120


def test_every_schedule_contains_all_five_subjects(
    default_subjects: List[Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that every generated schedule contains all 5 required subjects."""
    schedules = generate_all_schedules(default_subjects, default_slots)
    expected_codes = {"M", "P", "C", "CS", "E"}
    for s in schedules:
        actual_codes = {subj.code for subj in s.subjects}
        assert actual_codes == expected_codes


def test_no_schedule_contains_duplicates(
    default_subjects: List[Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that no schedule has repeated subjects."""
    schedules = generate_all_schedules(default_subjects, default_slots)
    for s in schedules:
        codes = [subj.code for subj in s.subjects]
        assert len(codes) == len(set(codes))


def test_every_day_has_exactly_one_subject(
    default_subjects: List[Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that each schedule maps 5 subjects to 5 distinct exam slots."""
    schedules = generate_all_schedules(default_subjects, default_slots)
    for s in schedules:
        assert len(s.subjects) == 5
        assert len(s.slots) == 5
        days = [slot.day for slot in s.slots]
        assert days == [1, 2, 3, 4, 5]


def test_generator_is_deterministic(
    default_subjects: List[Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that calling generate_all_schedules twice produces identical results."""
    run1 = generate_all_schedules(default_subjects, default_slots)
    run2 = generate_all_schedules(default_subjects, default_slots)
    assert len(run1) == len(run2)
    assert [s.subject_codes for s in run1] == [s.subject_codes for s in run2]
