"""Test that the YAML configuration matches the research paper's authoritative values.

This test guards against accidental edits to the research input. If the
configuration drifts from the paper's specification, this test will fail
immediately rather than allowing downstream tests to produce confusing
wrong-number failures.

Research paper specifies:
    Mathematics (M):        difficulty 5
    Physics (P):            difficulty 5
    Chemistry (C):          difficulty 4
    Computer Science (CS):  difficulty 3
    English (E):            difficulty 2
    Exam slots:             5
"""
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_configuration_matches_research_paper() -> None:
    """Verify that schedule_config.yaml matches the research paper exactly."""
    config_path = PROJECT_ROOT / "config" / "schedule_config.yaml"
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    actual = {
        subject["code"]: subject["difficulty"]
        for subject in config["subjects"]
    }
    assert actual == {
        "M": 5,
        "P": 5,
        "C": 4,
        "CS": 3,
        "E": 2,
    }
    assert len(config["exam_slots"]) == 5


def test_configuration_has_all_required_subject_fields() -> None:
    """Verify that each subject entry has name, code, and difficulty fields."""
    config_path = PROJECT_ROOT / "config" / "schedule_config.yaml"
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    for subject in config["subjects"]:
        assert "name" in subject, f"Missing 'name' in subject: {subject}"
        assert "code" in subject, f"Missing 'code' in subject: {subject}"
        assert "difficulty" in subject, f"Missing 'difficulty' in subject: {subject}"
        assert isinstance(subject["difficulty"], int)
        assert 1 <= subject["difficulty"] <= 5


def test_configuration_has_five_subjects() -> None:
    """Verify that the configuration contains exactly 5 subjects."""
    config_path = PROJECT_ROOT / "config" / "schedule_config.yaml"
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    assert len(config["subjects"]) == 5
