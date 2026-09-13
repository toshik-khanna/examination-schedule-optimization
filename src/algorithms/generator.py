"""Exhaustive schedule generation.

Generates all 5! = 120 possible examination schedules
using deterministic enumeration via itertools.permutations.
"""
import itertools
from typing import List, Tuple

from src.models.subject import Subject
from src.models.exam_slot import ExamSlot
from src.models.schedule import Schedule


def generate_all_schedules(
    subjects: List[Subject],
    slots: Tuple[ExamSlot, ...],
) -> List[Schedule]:
    """Generate all possible examination schedules by exhaustive enumeration.

    Uses itertools.permutations to produce every permutation of the
    subject list. For n subjects, this produces n! schedules.
    For n=5: 5! = 120 unique schedules.

    Args:
        subjects: List of Subject instances to schedule.
        slots: Tuple of ExamSlot instances (fixed order).

    Returns:
        List of all possible Schedule instances.
    """
    schedules: List[Schedule] = []

    for perm in itertools.permutations(subjects):
        schedule = Schedule(subjects=perm, slots=slots)
        schedules.append(schedule)

    return schedules
