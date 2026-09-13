"""Exhaustive optimization over the complete search space.

Research model:
    S_optimal = min(S_1, S_2, ..., S_120)
    DS_optimal = argmin_{DS_j} S_j

Because |search space| = 5! = 120, exhaustive evaluation is
computationally trivial and guarantees the global optimum.
"""
from typing import List, Tuple

from src.models.subject import Subject
from src.models.exam_slot import ExamSlot
from src.algorithms.generator import generate_all_schedules
from src.evaluation.scoring import calculate_csb_values, calculate_schedule_score
from src.evaluation.results import ScoredSchedule, OptimizationResult


def optimize(subjects: List[Subject], slots: Tuple[ExamSlot, ...]) -> OptimizationResult:
    """Run exhaustive optimization over all possible schedules.

    Algorithm:
        1. Generate all 5! = 120 valid schedules.
        2. Calculate the CSB score for every schedule.
        3. Identify the minimum score.
        4. Return all schedules tied for the minimum.

    Args:
        subjects: List of Subject instances.
        slots: Tuple of ExamSlot instances.

    Returns:
        OptimizationResult containing all scored schedules and the optimum.
    """
    # Step 1: Generate complete search space
    all_schedules = generate_all_schedules(subjects, slots)

    # Step 2: Score every schedule
    scored: List[ScoredSchedule] = []
    for schedule in all_schedules:
        csb_values = calculate_csb_values(schedule)
        score = sum(csb_values)
        scored.append(ScoredSchedule(
            schedule=schedule,
            csb_values=csb_values,
            score=score,
        ))

    # Step 3: Sort and rank
    scored.sort(key=lambda s: s.score)
    current_rank = 1
    for i, s in enumerate(scored):
        if i > 0 and s.score != scored[i - 1].score:
            current_rank = i + 1
        s.rank = current_rank

    # Step 4: Identify optimum
    optimal_score = scored[0].score
    optimal_schedules: List[ScoredSchedule] = []
    for s in scored:
        if s.score == optimal_score:
            s.is_optimal = True
            optimal_schedules.append(s)
        else:
            break  # sorted, so no more ties after this

    return OptimizationResult(
        all_scored=scored,
        optimal_schedules=optimal_schedules,
        optimal_score=optimal_score,
    )
