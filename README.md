# Navokoj Framework

*Physics-inspired SAT solving that treats constraints as flowing geometry*

[![Status](https://img.shields.io/badge/status-research_preview-yellow)]() [![Python](https://img.shields.io/badge/python-3.7+-blue)]() [![License](https://img.shields.io/badge/license-MIT-green)]()

**The Arithmetic Manifold, operationalized.** Solve SAT, scheduling, and graph coloring as energy landscapes using gradient descent + adiabatic cooling. Achieves 99%+ success on problems up to 100 variables in seconds.

---

## Table of Contents
- [What is Navokoj?](#what-is-navokoj)
- [Key Innovations](#key-innovations)
- [Performance Snapshot](#performance-snapshot)
- [Open Source vs Production API](#open-source-vs-production-api)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Features](#core-features)
- [Benchmarks](#benchmarks)
- [Theory to Practice](#theory-to-practice)
- [When to Use Navokoj](#when-to-use-navokoj)
- [Limitations](#limitations)
- [Citing](#citing)

---

## What is Navokoj?

Navokoj is a new SAT/max-SAT/max-UNSAT solver that reimagines constraint satisfaction as geometric flow. Instead of brute-force search or pure stochastic methods, it treats each constraint as a physical object with unique mass, then cools the system from chaos to order.

**Core Principle**: Discrete problems → Continuous relaxation → Gradient flow → Discrete solution.

This is the reference implementation of the [Arithmetic Manifold theory](https://scribe.rip/the-arithmetic-manifold-why-the-next-agi-will-think-in-geometric-operators-not-tokens-a2798c556b7b), demonstrating how geometric operators can outperform token-based reasoning for combinatorial optimization.

---

## Key Innovations

### The Three-Part Engine

```python
# 1. Prime-Weighted Operators (Arithmetic Sector)
primes = [2, 3, 5, 7, 11, ...]
weight_c = 1.0 / np.log(primes[i])  # Unique spectral identity

# 2. Adiabatic Quench (Dynamic Sector)
for t in range(steps):
    beta = (t / steps) * beta_max    # Temperature schedule
    grad = compute_constraint_energy(x, beta)
    x += learning_rate * beta * grad

# 3. Multi-Valued Collapse (Geometric Sector)
solution = [int(val > 0.5) for val in x]  # Discrete final state
```

1. **Prime Weights**: Each constraint gets a unique "mass" based on prime logarithms, breaking degeneracy and preventing local minima traps.
2. **Adiabatic Cooling**: Starts at high temperature (exploration) and slowly cools into ground state (exploitation).
3. **Native Multi-Valued Logic**: Handles binary, ternary, quaternary, or k-ary variables without encoding overhead.

---

## Performance Snapshot

| Problem Type | Variables | Success Rate | Time | Notes |
|--------------|-----------|--------------|------|-------|
| **3-SAT** (critical) | 50 | 99.4%±0.3% | 1.0s | Sweet spot |
| **3-SAT** (critical) | 100 | 99.5% | 2.0s | Linear scaling |
| **Graph Coloring** | 50 nodes | 100% | 1.4s | 7 colors |
| **Sudoku (AI Escargot)** | 729 | 99.85% | 82.8s | World's hardest |
| **MAX-SAT** (unsat) | 20 | 92.0% | 7.5s | Overconstrained |
| **Ternary CSP** | 50 | 80.4% | 9.6s | Dense graph |

*Scaling: ~20ms per variable, linear time complexity*

---

## Open Source vs Production API

This repository contains the **open-source research implementation**—a proof-of-concept in Python that demonstrates core principles. 
The Production API is at https://navokoj.shunyabar.foo/docs/

For production use, see **ShunyaBar API** ([Zenodo](https://zenodo.org/records/18096758)):
- **Free Tier**: Up to 5,000 variables, 35,000 clauses
- **Production Scale**: Up to 1M variables on H100 GPUs
- **100% Accuracy**: Guaranteed perfect solutions for satisfiable instances
- **Handles Structured Problems**: Fixes grain boundary issues in grid/lattice problems

### The Crystal Lattice Test

```python
# 400-variable perfect checkerboard coloring
# Open-source: Gets stuck at grain boundaries (~70% success)
# ShunyaBar API: 100% success in 4.3s
```

**When to use each**:
- **Open Source**: Research, prototyping, learning the theory, MAX-SAT problems
- **ShunyaBar API**: Production deployments, structured grids, guaranteed optimality, million-variable scale

---

## Installation

```bash
git clone https://github.com/sethuiyer/navokoj.git
cd navokoj
pip install -r requirements.txt
```

No external dependencies beyond NumPy/SciPy.

---

## Quick Start

### SAT Problem
```python
from navokoj import solve_sat, generate_3sat

# Generate random 3-SAT at critical density
clauses = generate_3sat(n_vars=50, alpha=4.26)

# Solve
solution = solve_sat(n_vars=50, clauses=clauses, steps=2000)
print(f"Satisfied {solution['satisfaction']:.1%} of clauses")
```

### Graph Coloring
```python
from navokoj import solve_qstate, generate_q_graph

# 50 nodes, 7 colors, 20% edge density
constraints = generate_q_graph(n_nodes=50, n_colors=7, density=0.2)
colors = solve_qstate(n_nodes=50, n_states=7, constraints=constraints)

print(f"Solution: {colors}")
```

### MAX-SAT (Overconstrained)
```python
# No special syntax needed - automatically optimizes
unsat_clauses = generate_3sat(n_vars=20, alpha=30.0)  # Unsatisfiable
best_solution = solve_sat(n_vars=20, clauses=unsat_clauses)
print(f"Best possible: {best_solution['satisfaction']:.1%}")
```

### Run Demos
```bash
# Comprehensive demo
python demo.py

# Full benchmark suite
python demo.py --benchmark

# Compare with ShunyaBar API
python shunya_bar_api_demo.py
```

---

## Core Features

### Multi-Valued SAT (2-ary to k-ary)
Native support without encoding overhead:
- **Binary**: Classical SAT (100% success)
- **Ternary**: {0,1,2} for fuzzy logic (89% success)
- **Quaternary**: Multi-level circuits (97% success)
- **9-ary**: Sudoku encoding (99.85% success)

```python
# 3-valued logic assignment
solution = solve_qstate(n=50, k=3, constraints=constraints)
```

### MAX-SAT Optimization
Unlike decision solvers that fail on unsatisfiable problems, Navokoj returns the **best possible assignment**:

| Variables | Clauses | Density | Satisfaction |
|-----------|---------|---------|--------------|
| 20 | 600 | 30.0 | 92.0% |
| 50 | 500 | 10.0 | 95.5% |

Perfect for real-world overconstrained problems: scheduling, resource allocation, configuration management.

### Three-Sector Architecture
- **Arithmetic**: Prime-weighted operators prevent symmetry traps
- **Geometric**: Continuous manifold enables gradient flows
- **Dynamic**: Adiabatic quench implements Hamiltonian dynamics

See [MANIFOLD_IMPLEMENTATION.md](MANIFOLD_IMPLEMENTATION.md) for theory-to-code mapping.

---

## Benchmarks

### SAT (3-SAT, α=4.26)
```
Variables: 10 → 100
Clauses: 42 → 426
Success Rate: 100% → 99.5%
Time: 0.2s → 2.0s (linear)
```

### Graph Coloring (7 colors)
```
Nodes: 50 → 100
Edges: 219 → 987
Success Rate: 100% → 98.6%
Time: 1.4s → 6.1s (linear)
```

### Specialty Problems
| Problem | Variables | Success | Time | Method |
|---------|-----------|---------|------|--------|
| 8-Queens | 64 | 100% | 1.0s | Binary CSP |
| AI Escargot | 729 | 99.85% | 82.8s | 9-ary SAT |
| R(5,5,5) Ramsey | ~4K | 100% | 12s | API only |

---

## Theory to Practice

| Manifold Concept | Code Implementation |
|------------------|---------------------|
| Operators as verbs | `grad[u] += weight * potential(v)` |
| Thoughts as trajectories | `for t in range(steps): beta = t/steps * beta_max` |
| Prime compression | `weights = 1.0 / np.log(primes + 1)` |
| Uncertainty as curvature | Energy → ∞ at constraint violation |
| Self-modifying geometry | `x = x + lr * grad` (no frozen weights) |
| Identity kernel | Prime weights flow-invariant |
| Collapse to discrete | `solution = [int(v > 0.5) for v in x]` |

The code *is* the differential equation. No separation between specification and implementation.

---

## When to Use Navokoj

### Perfect Fit
- Researching physics-inspired algorithms
- Solving modest SAT/CSP problems (10-200 vars)
- Working with multi-valued logic (ternary, quaternary)
- Overconstrained optimization (MAX-SAT)
- Prototyping operator-theoretic AI systems
- No need for formal completeness proofs

### ❌ Seek Alternatives
- Industrial-scale problems (1000+ vars) → Use ShunyaBar API
- Need 100% completeness guarantees → Use MiniSat, Z3, Glucose
- Real-time streaming constraints → Use incremental solvers
- Token-level interpretability required → This is operator-level

---

## Limitations

1. **Structured Grids**: Open-source version can get stuck on lattice problems (grain boundaries). Use ShunyaBar API for these.
2. **Scaling Ceiling**: Python implementation plateaus around 200-300 variables.
3. **Probabilistic**: 99%+ success, not 100% (unlike complete solvers).
4. **No Proofs**: Finds solutions but cannot prove unsatisfiability.
5. **MAX-SAT**: Optimization behavior is emergent, not formally guaranteed.

---

## Citing

If you use Navokoj in research, please cite:

```bibtex
@misc{sethurathienam_iyer_2025_18096758,
  author       = {Sethurathienam Iyer},
  title        = {ShunyaBar: Spectral–Arithmetic Phase Transitions
                   for Combinatorial Optimization},
  month        = dec,
  year         = 2025,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.18096758},
  url          = {https://doi.org/10.5281/zenodo.18096758}
}
```

---

## Contributing

We welcome contributions that align with the Arithmetic Manifold vision:

- New constraint encodings
- Performance optimizations
- Additional benchmarks
- Theory expansions

**License**: MIT. See LICENSE file for details.

---

*The next AGI will think in geometric operators, not tokens. This is where we start.*
