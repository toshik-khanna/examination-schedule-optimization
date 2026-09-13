"""Examination slot model."""
from dataclasses import dataclass

_VALID_DAYS = frozenset(range(1, 6))
_VALID_SESSIONS = frozenset({"Morning"})


@dataclass(frozen=True)
class ExamSlot:
    """Represents a single examination time slot.

    Attributes:
        day: Examination day number (1-5).
        session: Session name. Per research spec, always 'Morning'.
    """
    day: int
    session: str

    def __post_init__(self) -> None:
        if self.day not in _VALID_DAYS:
            raise ValueError(f"Day must be between 1 and 5, got: {self.day}")
        if self.session not in _VALID_SESSIONS:
            raise ValueError(f"Session must be one of {_VALID_SESSIONS}, got: {self.session!r}")

    def __repr__(self) -> str:
        return f"ExamSlot(Day {self.day}, {self.session})"
