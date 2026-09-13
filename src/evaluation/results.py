"""Experiment results: representation, statistics, and export.

This module is responsible for representing and exporting experiment results.
It does NOT perform optimization — that is handled by optimizer.py.

Research pipeline position:
    generator.py -> scoring.py -> optimizer.py -> results.py
"""
import csv
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from src.models.schedule import Schedule


@dataclass
class ScoredSchedule:
    """A schedule paired with its evaluation results.

    Attributes:
        schedule: The examination schedule (candidate).
        csb_values: Individual CSB values for each consecutive pair.
        score: Total schedule score (sum of CSB values).
        rank: Position when all schedules are sorted by score (1 = best).
        is_optimal: Whether this schedule achieves the minimum score.
    """
    schedule: Schedule
    csb_values: Tuple[int, ...]
    score: int
    rank: int = 0
    is_optimal: bool = False


@dataclass
class OptimizationResult:
    """Complete results from the exhaustive optimization.

    Attributes:
        all_scored: All 120 scored schedules.
        optimal_schedules: Schedules achieving the minimum score.
        optimal_score: The minimum score found.
    """
    all_scored: List[ScoredSchedule]
    optimal_schedules: List[ScoredSchedule]
    optimal_score: int

    @property
    def total_evaluated(self) -> int:
        """Number of schedules evaluated."""
        return len(self.all_scored)

    @property
    def num_optimal(self) -> int:
        """Number of schedules tied for the minimum score."""
        return len(self.optimal_schedules)

    @property
    def max_score(self) -> int:
        """Maximum score across all schedules."""
        return max(s.score for s in self.all_scored)

    @property
    def mean_score(self) -> float:
        """Mean score across all schedules."""
        return statistics.mean(s.score for s in self.all_scored)

    @property
    def median_score(self) -> float:
        """Median score across all schedules."""
        return statistics.median(s.score for s in self.all_scored)

    @property
    def second_lowest_score(self) -> Optional[int]:
        """Second-lowest score, or None if all scores are identical."""
        unique_scores = sorted(set(s.score for s in self.all_scored))
        return unique_scores[1] if len(unique_scores) > 1 else None

    def summary(self) -> str:
        """Generate a human-readable summary of results."""
        lines = [
            "=" * 60,
            "EXAMINATION SCHEDULE OPTIMIZATION — RESULTS SUMMARY",
            "=" * 60,
            f"Total schedules evaluated : {self.total_evaluated}",
            f"Minimum score (optimal)  : {self.optimal_score}",
            f"Maximum score            : {self.max_score}",
            f"Mean score               : {self.mean_score:.2f}",
            f"Median score             : {self.median_score:.1f}",
            f"Second-lowest score      : {self.second_lowest_score}",
            f"Number of optimal ties   : {self.num_optimal}",
            "",
            "OPTIMAL SCHEDULE(S):",
        ]
        for s in self.optimal_schedules:
            lines.append(
                f"  {s.schedule.subject_codes}  "
                f"(difficulties: {'-'.join(str(d) for d in s.schedule.difficulty_sequence)})  "
                f"score = {s.score}"
            )
        lines.append("=" * 60)
        return "\n".join(lines)

    def to_csv(self, filepath: Path) -> None:
        """Export all 120 scored schedules to CSV.

        Columns: schedule_id, day_1 .. day_5, difficulty_sequence,
                 csb_1 .. csb_4, total_score, rank, is_optimal
        """
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "schedule_id",
                "day_1", "day_2", "day_3", "day_4", "day_5",
                "difficulty_sequence",
                "csb_1", "csb_2", "csb_3", "csb_4",
                "total_score", "rank", "is_optimal",
            ])

            for i, scored in enumerate(self.all_scored, start=1):
                subjects = scored.schedule.subjects
                writer.writerow([
                    i,
                    subjects[0].code, subjects[1].code,
                    subjects[2].code, subjects[3].code, subjects[4].code,
                    "-".join(str(d) for d in scored.schedule.difficulty_sequence),
                    *scored.csb_values,
                    scored.score,
                    scored.rank,
                    scored.is_optimal,
                ])
