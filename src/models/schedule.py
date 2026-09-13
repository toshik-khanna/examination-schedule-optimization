"""Schedule model for examination scheduling.

Note: Schedule is a pure candidate — it does not contain a score.
Scoring is handled separately via ScoredSchedule in evaluation/results.py.
This separation maintains clean research traceability:
    Candidate -> Evaluation -> Optimization Result
"""
from dataclasses import dataclass
from typing import Tuple

from src.models.subject import Subject
from src.models.exam_slot import ExamSlot


@dataclass(frozen=True)
class Schedule:
    """An examination schedule: an ordered assignment of subjects to exam slots.

    Attributes:
        subjects: Ordered tuple of exactly 5 subjects.
        slots: Ordered tuple of exactly 5 exam slots.
    """
    subjects: Tuple[Subject, ...]
    slots: Tuple[ExamSlot, ...]

    def __post_init__(self) -> None:
        if len(self.subjects) != 5:
            raise ValueError(
                f"Schedule must contain exactly 5 subjects, got {len(self.subjects)}"
            )
        if len(self.slots) != 5:
            raise ValueError(
                f"Schedule must contain exactly 5 exam slots, got {len(self.slots)}"
            )
        codes = [s.code for s in self.subjects]
        if len(set(codes)) != len(codes):
            raise ValueError(f"Schedule contains duplicate subjects: {codes}")

    @property
    def subject_codes(self) -> str:
        """Dash-separated subject code string, e.g. 'M-P-C-E-CS'."""
        return "-".join(s.code for s in self.subjects)

    @property
    def difficulty_sequence(self) -> Tuple[int, ...]:
        """Tuple of difficulty values in schedule order."""
        return tuple(s.difficulty for s in self.subjects)

    def __repr__(self) -> str:
        return f"Schedule({self.subject_codes})"
