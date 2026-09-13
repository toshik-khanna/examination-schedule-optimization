"""Subject model for examination scheduling."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Subject:
    """Represents an examination subject.

    Attributes:
        name: Full subject name (e.g. 'Mathematics').
        code: Short code (e.g. 'M').
        difficulty: Difficulty rating, integer from 1 to 5.
    """
    name: str
    code: str
    difficulty: int

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError(f"Subject name must be a non-empty string, got: {self.name!r}")
        if not isinstance(self.code, str) or not self.code.strip():
            raise ValueError(f"Subject code must be a non-empty string, got: {self.code!r}")
        if not isinstance(self.difficulty, int) or not (1 <= self.difficulty <= 5):
            raise ValueError(
                f"Difficulty must be an integer between 1 and 5, got: {self.difficulty!r}"
            )

    def __repr__(self) -> str:
        return f"Subject({self.code}, difficulty={self.difficulty})"
