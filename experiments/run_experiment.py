"""Main experiment entry point.

Runs the complete examination schedule optimization pipeline:
    1. Load configuration (research input, represented as YAML)
    2. Generate all 120 candidate schedules
    3. Score every schedule using CSB
    4. Find the optimal schedule(s) via exhaustive enumeration
    5. Export results to CSV
    6. Optionally generate visualizations (--plot flag)

Usage:
    python -m experiments.run_experiment
    python -m experiments.run_experiment --plot
"""
import argparse
import sys
from pathlib import Path

import yaml

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.models.subject import Subject
from src.models.exam_slot import ExamSlot
from src.algorithms.optimizer import optimize
from src.constraints.validator import validate_schedule
from src.utils.logging_config import setup_logging


def load_config(config_path: Path) -> dict:
    """Load experiment configuration from YAML.

    Note: YAML is an implementation representation of the research input.
    The research input (subjects, difficulties) is defined by the paper.
    YAML is merely the storage mechanism.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_subjects(config: dict) -> list:
    """Create Subject instances from configuration."""
    return [
        Subject(name=s["name"], code=s["code"], difficulty=s["difficulty"])
        for s in config["subjects"]
    ]


def build_slots(config: dict) -> tuple:
    """Create ExamSlot instances from configuration."""
    return tuple(
        ExamSlot(day=slot["day"], session=slot["session"])
        for slot in config["exam_slots"]
    )


def generate_visualizations(result, output_dir: Path) -> None:
    """Generate research visualizations (supplementary analysis output).

    These visualizations are implementation/analysis outputs,
    not part of the research methodology.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available — skipping visualizations.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    scores = [s.score for s in result.all_scored]

    # 1. Score distribution histogram
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(scores, bins=range(min(scores), max(scores) + 2), edgecolor="black", alpha=0.7)
    ax.axvline(result.optimal_score, color="red", linestyle="--", linewidth=2, label=f"Minimum = {result.optimal_score}")
    ax.set_xlabel("Schedule Score (Total CSB)")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Schedule Scores (n=120)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "score_distribution.png", dpi=150)
    plt.close(fig)

    # 2. All 120 schedule scores (sorted)
    sorted_scores = sorted(scores)
    fig, ax = plt.subplots(figsize=(14, 6))
    colors = ["red" if s == result.optimal_score else "steelblue" for s in sorted_scores]
    ax.bar(range(1, 121), sorted_scores, color=colors, width=1.0, edgecolor="none")
    ax.set_xlabel("Schedule Rank")
    ax.set_ylabel("Total CSB Score")
    ax.set_title("All 120 Schedule Scores (Ranked)")
    ax.axhline(result.optimal_score, color="red", linestyle="--", alpha=0.7, label=f"Optimal = {result.optimal_score}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "ranked_scores.png", dpi=150)
    plt.close(fig)

    # 3. Score vs schedule index
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.scatter(range(1, 121), scores, s=15, alpha=0.6, c="steelblue")
    ax.axhline(result.optimal_score, color="red", linestyle="--", linewidth=1.5, label=f"Minimum = {result.optimal_score}")
    ax.set_xlabel("Schedule Index")
    ax.set_ylabel("Total CSB Score")
    ax.set_title("Scores of All 120 Schedules")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "all_scores.png", dpi=150)
    plt.close(fig)

    print(f"Visualizations saved to: {output_dir}")


def main() -> None:
    """Run the complete optimization experiment."""
    parser = argparse.ArgumentParser(
        description="Examination Schedule Optimization Experiment"
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate visualizations (requires matplotlib)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "config" / "schedule_config.yaml",
        help="Path to configuration file",
    )
    args = parser.parse_args()

    logger = setup_logging()

    # Step 1: Load configuration
    logger.info("Loading configuration from %s", args.config)
    config = load_config(args.config)
    subjects = build_subjects(config)
    slots = build_slots(config)
    logger.info("Subjects: %s", [s.code for s in subjects])
    logger.info("Exam slots: %d days", len(slots))

    # Step 2-4: Run exhaustive optimization
    logger.info("Running exhaustive optimization over 5! = 120 schedules...")
    result = optimize(subjects, slots)

    # Validate all optimal schedules
    for optimal in result.optimal_schedules:
        validate_schedule(optimal.schedule)

    # Step 5: Print summary
    print("\n" + result.summary())

    # Step 6: Export CSV
    results_dir = PROJECT_ROOT / "results"
    csv_path = results_dir / "schedules.csv"
    result.to_csv(csv_path)
    logger.info("Results exported to %s", csv_path)

    # Step 7: Optional visualizations
    if args.plot:
        generate_visualizations(result, results_dir)

    logger.info("Experiment complete.")


if __name__ == "__main__":
    main()
