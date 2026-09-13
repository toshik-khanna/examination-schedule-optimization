# Research-to-Code Traceability

This document maps every research concept to its implementation.

## Methodology

This project implements a small deterministic combinatorial optimization.
Because the search space contains only 120 schedules, exhaustive enumeration
is used. This guarantees the global optimum — no heuristics are needed.

## Traceability Matrix

| Research Concept | Mathematical Notation | Implementation | File | Function/Class |
|---|---|---|---|---|
| 5 subjects | — | Configuration (YAML is the storage mechanism, not methodology) | `config/schedule_config.yaml` | — |
| Difficulty $D_i$ | $D_i \in \{1,...,5\}$ | `Subject.difficulty` | `src/models/subject.py` | `Subject` |
| Five exam days | Day 1–5, Morning | `ExamSlot` | `src/models/exam_slot.py` | `ExamSlot` |
| Each subject once | $\sum_d x_{s,d} = 1\ \forall s$ | Constraint validation | `src/constraints/validator.py` | `validate_schedule()` |
| Each day one subject | $\sum_s x_{s,d} = 1\ \forall d$ | Constraint validation | `src/constraints/validator.py` | `validate_schedule()` |
| Candidate schedule | Permutation of subjects | `Schedule` | `src/models/schedule.py` | `Schedule` |
| 120 permutations | $5! = 120$ | `itertools.permutations` | `src/algorithms/generator.py` | `generate_all_schedules()` |
| $CSB = D_i \times D_{i+1}$ | Consecutive pair product | CSB calculation | `src/evaluation/scoring.py` | `calculate_csb()` |
| $S = \sum_{i=1}^{4} D_i D_{i+1}$ | Sum of 4 CSB values | Total score | `src/evaluation/scoring.py` | `calculate_schedule_score()` |
| $S^* = \min(S_1,\ldots,S_{120})$ | Global minimum | Exhaustive search | `src/algorithms/optimizer.py` | `optimize()` |
| Optimal schedule | $DS^* = \arg\min S_j$ | Result with tied handling | `src/evaluation/results.py` | `OptimizationResult` |
| Experimental output | Complete CSV | All 120 records | `results/schedules.csv` | `OptimizationResult.to_csv()` |

## Research vs Implementation Decisions

### Explicitly Specified by Research
- Subject identities and difficulty values (M=5, P=5, C=4, CS=3, E=3)
- Five examination days, Morning session
- Each subject appears exactly once
- CSB = product of consecutive difficulties
- Total score = sum of 4 CSB values
- Exhaustive enumeration of all 120 permutations
- Optimal = minimum total score

### Implementation Decisions (Not Part of Methodology)
- Python as the implementation language
- YAML as the configuration storage format
- `itertools.permutations` for deterministic generation
- CSV as the output format
- `matplotlib` for supplementary visualizations (optional)
- `pytest` as the testing framework
- Dataclasses for model representation

### Key Design Decision: Score Separation
The `Schedule` model is a pure candidate — it does not contain a score.
Evaluation results are stored separately in `ScoredSchedule`.
This maintains clean research traceability:
```
Candidate (Schedule) → Evaluation (ScoredSchedule) → Optimization (OptimizationResult)
```
