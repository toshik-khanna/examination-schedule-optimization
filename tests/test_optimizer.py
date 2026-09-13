"""Unit tests for the schedule optimizer."""
import itertools
import sys
from pathlib import Path
from typing import List, Tuple

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.algorithms.optimizer import optimize
from src.evaluation.results import OptimizationResult, ScoredSchedule
from src.models.exam_slot import ExamSlot
from src.models.subject import Subject


@pytest.fixture
def research_subjects() -> List[Subject]:
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


@pytest.fixture
def optimization_result(
    research_subjects: List[Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> OptimizationResult:
    """Run optimization once and provide the OptimizationResult fixture."""
    return optimize(research_subjects, default_slots)


def test_exactly_120_schedules_evaluated(
    optimization_result: OptimizationResult,
) -> None:
    """Test that result.total_evaluated == 120 and len(result.all_scored) == 120."""
    assert optimization_result.total_evaluated == 120
    assert len(optimization_result.all_scored) == 120


def test_every_schedule_has_a_score(
    optimization_result: OptimizationResult,
) -> None:
    """Test that every evaluated candidate is assigned an integer score and 4 CSB values."""
    for scored in optimization_result.all_scored:
        assert isinstance(scored, ScoredSchedule)
        assert isinstance(scored.score, int)
        assert isinstance(scored.csb_values, tuple)
        assert len(scored.csb_values) == 4
        assert scored.score == sum(scored.csb_values)


def test_optimal_score_is_minimum_of_all_scores(
    optimization_result: OptimizationResult,
) -> None:
    """Test that optimal_score equals min(score for s in all_scored)."""
    min_score = min(s.score for s in optimization_result.all_scored)
    assert optimization_result.optimal_score == min_score


def test_no_candidate_has_lower_score_than_optimal(
    optimization_result: OptimizationResult,
) -> None:
    """Test that no candidate schedule achieves a score strictly lower than optimal_score."""
    for scored in optimization_result.all_scored:
        assert scored.score >= optimization_result.optimal_score


def test_all_optimal_schedules_have_optimal_score(
    optimization_result: OptimizationResult,
) -> None:
    """Test that every schedule marked optimal has score == optimal_score and is_optimal is True."""
    assert len(optimization_result.optimal_schedules) > 0
    for opt in optimization_result.optimal_schedules:
        assert opt.score == optimization_result.optimal_score
        assert opt.is_optimal is True
        assert opt.rank == 1


def test_tied_optimal_schedules_handled(
    optimization_result: OptimizationResult,
) -> None:
    """Test that ties for the minimum score are properly handled (num_optimal >= 1)."""
    assert optimization_result.num_optimal >= 1
    assert optimization_result.num_optimal == len(optimization_result.optimal_schedules)


def test_optimizer_is_deterministic(
    research_subjects: List[Subject],
    default_slots: Tuple[ExamSlot, ...],
) -> None:
    """Test that running optimize twice yields identical optimal score and schedules."""
    run1 = optimize(research_subjects, default_slots)
    run2 = optimize(research_subjects, default_slots)

    assert run1.optimal_score == run2.optimal_score
    assert run1.num_optimal == run2.num_optimal
    run1_codes = [s.schedule.subject_codes for s in run1.optimal_schedules]
    run2_codes = [s.schedule.subject_codes for s in run2.optimal_schedules]
    assert run1_codes == run2_codes


def test_ranks_assigned_correctly(
    optimization_result: OptimizationResult,
) -> None:
    """Test that ranks are assigned correctly with rank 1 = best and ascending order."""
    all_scored = optimization_result.all_scored
    # All scored should be sorted ascending by score
    scores = [s.score for s in all_scored]
    assert scores == sorted(scores)

    # First schedule must have rank 1
    assert all_scored[0].rank == 1

    # Check rank computation logic: tied scores get same rank, next score gets index+1
    for i, s in enumerate(all_scored):
        if i == 0:
            assert s.rank == 1
        else:
            if s.score == all_scored[i - 1].score:
                assert s.rank == all_scored[i - 1].rank
            else:
                assert s.rank == i + 1


def test_second_lowest_score_greater_than_optimal(
    optimization_result: OptimizationResult,
) -> None:
    """Test that second_lowest_score is strictly greater than optimal_score."""
    second_lowest = optimization_result.second_lowest_score
    assert second_lowest is not None
    assert second_lowest > optimization_result.optimal_score


def test_optimal_score_independently_verified() -> None:
    """Independently verify the optimal score against the mathematical model.

    The optimal score is discovered by the optimizer through enumeration.
    This test independently verifies it by computing all scores manually.
    """
    difficulties = {"M": 5, "P": 5, "C": 4, "CS": 3, "E": 3}
    codes = list(difficulties.keys())

    # Independently compute all 120 scores
    all_scores = []
    for perm in itertools.permutations(codes):
        diffs = [difficulties[c] for c in perm]
        score = sum(diffs[i] * diffs[i + 1] for i in range(4))
        all_scores.append(score)

    assert len(all_scores) == 120
    independent_minimum = min(all_scores)

    # Now run the optimizer
    subjects = [
        Subject(name="Mathematics", code="M", difficulty=5),
        Subject(name="Physics", code="P", difficulty=5),
        Subject(name="Chemistry", code="C", difficulty=4),
        Subject(name="Computer Science", code="CS", difficulty=3),
        Subject(name="English", code="E", difficulty=3),
    ]
    slots = tuple(ExamSlot(day=d, session="Morning") for d in range(1, 6))
    result = optimize(subjects, slots)

    # The optimizer's result must match the independent calculation
    assert result.optimal_score == independent_minimum
