"""Constraint validation for examination schedules.

Mathematical constraints:
    - sum_d x[s,d] = 1 for every subject s (each subject appears exactly once)
    - sum_s x[s,d] = 1 for every day d (each day has exactly one subject)
"""
from typing import List, Set

from src.models.subject import Subject
from src.models.schedule import Schedule

# The five required subject codes per the research specification
REQUIRED_SUBJECT_CODES: Set[str] = {"M", "P", "C", "CS", "E"}


def validate_schedule(schedule: Schedule, required_codes: Set[str] = REQUIRED_SUBJECT_CODES) -> bool:
    """Validate that a schedule satisfies all research constraints.

    Checks:
        1. Exactly 5 subjects.
        2. Every required subject code is present.
        3. No subject appears more than once.
        4. Every exam slot is occupied exactly once.
        5. Exactly 5 positions.

    Args:
        schedule: The schedule to validate.
        required_codes: Set of required subject codes.

    Returns:
        True if valid.

    Raises:
        ValueError: If any constraint is violated, with a descriptive message.
    """
    # Constraint 1 & 5: Exactly 5 subjects and 5 positions
    if len(schedule.subjects) != 5:
        raise ValueError(f"Schedule must contain exactly 5 subjects, got {len(schedule.subjects)}")
    if len(schedule.slots) != 5:
        raise ValueError(f"Schedule must contain exactly 5 slots, got {len(schedule.slots)}")

    # Constraint 3: No duplicate subjects
    codes = [s.code for s in schedule.subjects]
    if len(set(codes)) != len(codes):
        duplicates = [c for c in codes if codes.count(c) > 1]
        raise ValueError(f"Duplicate subjects found: {duplicates}")

    # Constraint 2: Every required subject present
    present_codes = set(codes)
    missing = required_codes - present_codes
    if missing:
        raise ValueError(f"Missing required subjects: {missing}")

    # Constraint 4: Every exam slot occupied exactly once
    days = [slot.day for slot in schedule.slots]
    if len(set(days)) != len(days):
        raise ValueError(f"Duplicate exam days found: {days}")

    return True
