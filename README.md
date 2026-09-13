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
| English | E | 3 |

The **Consecutive Subject Burden (CSB)** for two adjacent subjects is:

```
CSB = D_i × D_{i+1}
```

The **total schedule score** is:

```
S = Σ(D_i × D_{i+1}) for i = 1 to 4
```

The **optimal schedule** minimizes S over all 5! = 120 possible orderings.

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
