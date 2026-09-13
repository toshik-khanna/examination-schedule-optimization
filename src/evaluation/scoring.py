"""Consecutive Subject Burden (CSB) scoring.

Research formulation:
    CSB(i) = D_i * D_{i+1}     (for consecutive subjects i, i+1)
    S = sum(CSB(i)) for i=1..4  (total schedule score)

The score is based ONLY on consecutive subject difficulty products.
No additional weights, penalties, or factors are applied.
"""
from typing import List, Tuple

from src.models.subject import Subject
from src.models.schedule import Schedule


def calculate_csb(subject_a: Subject, subject_b: Subject) -> int:
    """Calculate the Consecutive Subject Burden for two adjacent subjects.

    CSB = D_a * D_b

    Args:
        subject_a: First subject in the consecutive pair.
        subject_b: Second subject in the consecutive pair.

    Returns:
        Product of the two subjects' difficulty values.
    """
    return subject_a.difficulty * subject_b.difficulty


def calculate_csb_values(schedule: Schedule) -> Tuple[int, ...]:
    """Calculate all individual CSB values for a schedule.

    For a 5-subject schedule, produces exactly 4 CSB values.

    Args:
        schedule: The schedule to evaluate.

    Returns:
        Tuple of CSB values for each consecutive pair.
    """
    subjects = schedule.subjects
    return tuple(
        calculate_csb(subjects[i], subjects[i + 1])
        for i in range(len(subjects) - 1)
    )


def calculate_schedule_score(schedule: Schedule) -> int:
    """Calculate the total schedule score.

    S = sum(D_i * D_{i+1}) for i = 1 to 4

    Args:
        schedule: The schedule to score.

    Returns:
        Total CSB score (sum of all consecutive-pair products).
    """
    return sum(calculate_csb_values(schedule))
