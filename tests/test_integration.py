"""Integration tests for the complete examination schedule optimization pipeline."""
import csv
import sys
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.algorithms.optimizer import optimize
from src.constraints.validator import validate_schedule
from src.models.exam_slot import ExamSlot
from src.models.subject import Subject


def test_end_to_end_pipeline_from_config(tmp_path: Path) -> None:
    """Test full pipeline: load YAML config, build objects, optimize, and export CSV."""
    config_path = PROJECT_ROOT / "config" / "schedule_config.yaml"
    assert config_path.exists(), f"Config file not found at {config_path}"

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    subjects = [
        Subject(name=s["name"], code=s["code"], difficulty=s["difficulty"])
        for s in config["subjects"]
    ]
    slots = tuple(
        ExamSlot(day=slot["day"], session=slot["session"])
        for slot in config["exam_slots"]
    )

    assert len(subjects) == 5
    assert len(slots) == 5

    result = optimize(subjects, slots)

    # 1. Verify 120 schedules evaluated
    assert result.total_evaluated == 120
    assert len(result.all_scored) == 120

    # 2. Validate all optimal schedules satisfy constraints
    assert result.num_optimal > 0
    for optimal in result.optimal_schedules:
        assert validate_schedule(optimal.schedule) is True

    # 3. CSV export verification using tmp_path
    csv_file = tmp_path / "test_schedules.csv"
    result.to_csv(csv_file)
    assert csv_file.exists()

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    # 1 header row + 120 data rows
    assert len(reader) == 121
    header = reader[0]
    assert header == [
        "schedule_id",
        "day_1", "day_2", "day_3", "day_4", "day_5",
        "difficulty_sequence",
        "csb_1", "csb_2", "csb_3", "csb_4",
        "total_score", "rank", "is_optimal",
    ]


def test_property_five_subjects_each_appearing_once() -> None:
    """Property test: every generated candidate contains 5 subjects, each appearing once."""
    config_path = PROJECT_ROOT / "config" / "schedule_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    subjects = [
        Subject(name=s["name"], code=s["code"], difficulty=s["difficulty"])
        for s in config["subjects"]
    ]
    slots = tuple(
        ExamSlot(day=slot["day"], session=slot["session"])
        for slot in config["exam_slots"]
    )

    result = optimize(subjects, slots)
    required_codes = {s.code for s in subjects}

    for scored in result.all_scored:
        codes = [s.code for s in scored.schedule.subjects]
        assert len(codes) == 5
        assert len(set(codes)) == 5
        assert set(codes) == required_codes


def test_property_four_csb_terms_and_score_sum() -> None:
    """Property test: every schedule produces 4 CSB terms and total score equals their sum."""
    config_path = PROJECT_ROOT / "config" / "schedule_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    subjects = [
        Subject(name=s["name"], code=s["code"], difficulty=s["difficulty"])
        for s in config["subjects"]
    ]
    slots = tuple(
        ExamSlot(day=slot["day"], session=slot["session"])
        for slot in config["exam_slots"]
    )

    result = optimize(subjects, slots)

    for scored in result.all_scored:
        assert len(scored.csb_values) == 4
        assert scored.score == sum(scored.csb_values)


def test_property_optimal_score_leq_every_candidate_score() -> None:
    """Property test: optimal_score is less than or equal to every candidate score."""
    config_path = PROJECT_ROOT / "config" / "schedule_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    subjects = [
        Subject(name=s["name"], code=s["code"], difficulty=s["difficulty"])
        for s in config["subjects"]
    ]
    slots = tuple(
        ExamSlot(day=slot["day"], session=slot["session"])
        for slot in config["exam_slots"]
    )

    result = optimize(subjects, slots)

    for scored in result.all_scored:
        assert result.optimal_score <= scored.score


def test_example_schedules_comparison() -> None:
    """Verify both research example schedules:

    Example 1: M-P-C-E-CS with score 66
    Example 2: M-CS-C-E-P with score 54
    Verify 54 < 66.
    """
    config_path = PROJECT_ROOT / "config" / "schedule_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    subjects = [
        Subject(name=s["name"], code=s["code"], difficulty=s["difficulty"])
        for s in config["subjects"]
    ]
    slots = tuple(
        ExamSlot(day=slot["day"], session=slot["session"])
        for slot in config["exam_slots"]
    )

    result = optimize(subjects, slots)

    scored_by_codes = {s.schedule.subject_codes: s for s in result.all_scored}

    # Verify Example 1
    assert "M-P-C-E-CS" in scored_by_codes
    ex1 = scored_by_codes["M-P-C-E-CS"]
    assert ex1.csb_values == (25, 20, 12, 9)
    assert ex1.score == 66

    # Verify Example 2
    assert "M-CS-C-E-P" in scored_by_codes
    ex2 = scored_by_codes["M-CS-C-E-P"]
    assert ex2.csb_values == (15, 12, 12, 15)
    assert ex2.score == 54
    assert ex2.is_optimal is True

    # Verify 54 < 66
    assert ex2.score < ex1.score
    assert 54 < 66
