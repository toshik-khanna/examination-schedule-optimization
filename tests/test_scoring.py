"""Unit tests for Consecutive Subject Burden (CSB) scoring."""
import sys
from pathlib import Path
from typing import Tuple

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.evaluation.scoring import (
    calculate_csb,
    calculate_csb_values,
    calculate_schedule_score,
)
from src.models.exam_slot import ExamSlot
from src.models.schedule import Schedule
from src.models.subject import Subject


@pytest.fixture
def default_slots() -> Tuple[ExamSlot, ...]:
    """Provide standard 5 morning examination slots."""
    return tuple(ExamSlot(day=d, session="Morning") for d in range(1, 6))


@pytest.fixture
def research_subjects() -> dict[str, Subject]:
    """Provide a lookup dictionary of research subjects."""
    return {
        "M": Subject(name="Mathematics", code="M", difficulty=5),
        "P": Subject(name="Physics", code="P", difficulty=5),
        "C": Subject(name="Chemistry", code="C", difficulty=4),
        "CS": Subject(name="Computer Science", code="CS", difficulty=3),
        "E": Subject(name="English", code="E", difficulty=2),
    }


def test_calculate_csb_math_physics(research_subjects: dict[str, Subject]) -> None:
    """Test calculate_csb for M(5) and P(5) -> 25."""
    m = research_subjects["M"]
    p = research_subjects["P"]
    assert calculate_csb(m, p) == 25


def test_calculate_csb_cs_english(research_subjects: dict[str, Subject]) -> None:
    """Test calculate_csb for CS(3) and E(2) -> 6."""
    cs = research_subjects["CS"]
    e = research_subjects["E"]
    assert calculate_csb(cs, e) == 6


def test_calculate_csb_math_english(research_subjects: dict[str, Subject]) -> None:
    """Test calculate_csb for M(5) and E(2) -> 10."""
    m = research_subjects["M"]
    e = research_subjects["E"]
    assert calculate_csb(m, e) == 10


def test_example_1_m_p_c_e_cs(
    research_subjects: dict[str, Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test Example 1 (baseline): M-P-C-E-CS -> CSB values (25, 20, 8, 6), total 59."""
    schedule = Schedule(
        subjects=(
            research_subjects["M"],
            research_subjects["P"],
            research_subjects["C"],
            research_subjects["E"],
            research_subjects["CS"],
        ),
        slots=default_slots,
    )
    csb_values = calculate_csb_values(schedule)
    assert csb_values == (25, 20, 8, 6)
    total_score = calculate_schedule_score(schedule)
    assert total_score == 59


def test_example_2_m_cs_c_e_p(
    research_subjects: dict[str, Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test Example 2 (optimal): M-CS-C-E-P -> CSB values (15, 12, 8, 10), total 45."""
    schedule = Schedule(
        subjects=(
            research_subjects["M"],
            research_subjects["CS"],
            research_subjects["C"],
            research_subjects["E"],
            research_subjects["P"],
        ),
        slots=default_slots,
    )
    csb_values = calculate_csb_values(schedule)
    assert csb_values == (15, 12, 8, 10)
    total_score = calculate_schedule_score(schedule)
    assert total_score == 45


def test_calculate_csb_values_returns_exactly_four_values(
    research_subjects: dict[str, Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that calculate_csb_values always returns exactly 4 values for a 5-subject schedule."""
    schedule = Schedule(
        subjects=(
            research_subjects["M"],
            research_subjects["P"],
            research_subjects["C"],
            research_subjects["CS"],
            research_subjects["E"],
        ),
        slots=default_slots,
    )
    values = calculate_csb_values(schedule)
    assert isinstance(values, tuple)
    assert len(values) == 4
    assert all(isinstance(v, int) for v in values)


def test_score_is_sum_of_csb_values(
    research_subjects: dict[str, Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that calculate_schedule_score equals the sum of calculate_csb_values."""
    schedule = Schedule(
        subjects=(
            research_subjects["E"],
            research_subjects["CS"],
            research_subjects["C"],
            research_subjects["P"],
            research_subjects["M"],
        ),
        slots=default_slots,
    )
    values = calculate_csb_values(schedule)
    score = calculate_schedule_score(schedule)
    assert score == sum(values)
