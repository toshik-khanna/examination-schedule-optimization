# Examination Schedule Optimization

Optimal examination scheduling for five A-Level subjects using exhaustive
combinatorial optimization.

## Mathematical Model

Given five subjects with difficulty ratings:

| Subject | Code | Difficulty |
|---|---|---|
| Mathematics | M | 5 |
| Physics | P | 5 |
| Chemistry | C | 4 |
| Computer Science | CS | 3 |
| English | E | 2 |

The **Consecutive Subject Burden (CSB)** for two adjacent subjects is:

```
CSB = D_i × D_{i+1}
```

The **total schedule score** is:

```
S = Σ(D_i × D_{i+1}) for i = 1 to 4
```

The **optimal schedule** minimizes S over all 5! = 120 possible orderings.

## Expected Results for the Research Model

The model uses the following difficulty scores:

- Mathematics (M): 5
- Physics (P): 5
- Chemistry (C): 4
- Computer Science (CS): 3
- English (E): 2

The objective function is:

```
S = Σ(D_i × D_{i+1}), for i = 1 to 4
```

The experiment evaluates all 120 possible orders.

Expected results:
- Baseline M-P-C-E-CS: **59**
- Minimum score: **45**
- Number of optimal schedules: **4**
- Absolute reduction from baseline: **14**
- Percentage reduction: **23.73%**

The four optimal orderings (all scoring 45):

| # | Order | CSB Values | Total |
|---|---|---|---|
| 1 | M-CS-C-E-P | 15, 12, 8, 10 | 45 |
| 2 | P-E-C-CS-M | 10, 8, 12, 15 | 45 |
| 3 | M-E-C-CS-P | 10, 8, 12, 15 | 45 |
| 4 | P-CS-C-E-M | 15, 12, 8, 10 | 45 |

## Installation

```bash
pip install -r requirements.txt
```

Core dependencies: `pyyaml`, `pytest`
Optional: `matplotlib` (for visualizations)

## Usage

Run the optimization experiment:

```bash
python -m experiments.run_experiment
```

With visualizations:

```bash
python -m experiments.run_experiment --plot
```

## Run Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
├── config/                  # Configuration (YAML storage of research input)
├── docs/                    # Research-to-code traceability
├── src/
│   ├── models/              # Data models (Subject, ExamSlot, Schedule)
│   ├── constraints/         # Constraint validation
│   ├── algorithms/          # Generator (120 permutations) & Optimizer
│   ├── evaluation/          # CSB scoring & results export
│   └── utils/               # Logging
├── experiments/             # Experiment entry point
├── tests/                   # Comprehensive test suite
└── results/                 # Output (CSV, visualizations)
```

## Research Pipeline

```
Subjects + difficulties
    ↓
Generate 5! = 120 schedules
    ↓
Score each: S = Σ(D_i × D_{i+1})
    ↓
S_optimal = min(S_1, ..., S_120)
    ↓
Optimal schedule(s)
```

## License

Research project — see documentation for methodology details.
