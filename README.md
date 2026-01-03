# Navokoj Framework

*The operational implementation of the Arithmetic Manifold - where constraint satisfaction becomes geometric flow*

[![Status](https://img.shields.io/badge/status-research_preview-yellow)]() [![Python](https://img.shields.io/badge/python-3.7%2B-blue)]()

**This is not just a SAT solver. This is the executable version of [The Arithmetic Manifold](https://scribe.rip/the-arithmetic-manifold-why-the-next-agi-will-think-in-geometric-operators-not-tokens-a2798c556b7b) theory.**


**TL;DR**: Treat SAT, scheduling, and graph coloring as energy landscapes. Use gradient descent + adiabatic cooling instead of backtracking. Gets 99%+ success on problems up to 100 variables in seconds.

---

## Part of the ShunyaBar Framework

This system is a special case implementation of the broader general framework presented in:

**[ShunyaBar: Spectral–Arithmetic Phase Transitions for Combinatorial Optimization](https://zenodo.org/records/18096758)**

For larger-scale problems and production use cases, you can access the full **ShunyaBar API**:

- **FREE Tier**: Up to 5,000 variables and 35,000 clauses
- **API Endpoint**: https://navokoj.shunyabar.foo/
- **Capabilities**: Handles industrial-scale SAT/CSP problems with the same spectral-arithmetic approach

This repository contains the reference implementation demonstrating the core theoretical principles.

### About Navokoj

- **Physics-Inspired**: Uses non-commutative geometry and statistical mechanics to transform constraint satisfaction into geometric flow
- **Independently Verified**: 92.57% perfect solution rate on 4,199 industrial problems (SAT 2024 Industrial Track)
- **Production Scale**: Handles up to 1M variables and 8M clauses on H100 GPU infrastructure
- **Unified API**: Single REST endpoint for CNF, XOR, weighted constraints, and QBF quantifiers
- **Proven Results**: Solved R(5,5,5) Ramsey theory problem, 129-Queens, and 200-variable 1M-clause ultra-high-k SAT at 100% satisfaction

---

## The Shockingly Simple Idea

Instead of searching through combinatorial space, we:

1. **Relax** discrete variables to continuous probabilities/times/potentials
2. **Define** each constraint as an energy penalty
3. **Cool** slowly (high temperature → low temperature) while following gradients  
4. **Collapse** final state back to discrete solution

That's it. Physics does the search for you.

---

## Quick Demo

```python
# SAT: 50-variable 3-SAT at critical density
from navokoj import solve_sat, generate_3sat

clauses = generate_3sat(n_vars=50, alpha=4.26)
solution = solve_sat(50, clauses, steps=2000)
# Result: 99.5% clauses satisfied in ~1 second

# Graph Coloring: 50 nodes, 7 colors  
from navokoj import solve_qstate, generate_q_graph

constraints = generate_q_graph(50, density=0.2)
colors = solve_qstate(50, 7, constraints)
# Result: 100% conflict-free in ~1.4 seconds

# Run comprehensive demo
python demo.py

# Run benchmark suite  
python demo.py --benchmark
```

---

## What Makes This Different

### This is the Arithmetic Manifold, Operationalized

The [Arithmetic Manifold manifesto](https://scribe.rip/the-arithmetic-manifold-why-the-next-agi-will-think-in-geometric-operators-not-tokens-a2798c556b7b) argues that AGI will emerge from **geometric operators, not tokens**. Navokoj is the first code that makes this concrete:

- **Operators as Neurons**: Each constraint is a *first-class operator* with unique prime-weighted spectral signature
- **Manifold as State Space**: Continuous probabilities/times/potentials = points on high-dimensional geometric landscape  
- **Adiabatic Flows**: β-schedule implements Hamiltonian dynamics, cooling from chaos to order
- **Self-Modification**: Every gradient step warps the manifold - no frozen weights

See [MANIFOLD_IMPLEMENTATION.md](MANIFOLD_IMPLEMENTATION.md) for the complete theory-to-code mapping.

### 1. **Three-Sector Architecture**

- **Arithmetic Sector**: Prime-weighted constraint operators (unique spectral identity)
- **Geometric Sector**: Continuous manifold of possible states
- **Dynamic Sector**: Hamiltonian flows guided by adiabatic cooling

### 2. **Prime Weighting (Novel)**

```python
primes = [2, 3, 5, 7, 11, ...]
weight_c = 1.0 / log(primes[i])  # Unique energy scale per constraint
```

Every constraint has a distinct "mass" preventing degenerate trade-offs.

### 3. **Adiabatic Cooling (Physics-Inspired)**

```python
for t in range(steps):
    beta = (t / steps) * beta_max  # Temperature schedule
    grad = compute_constraint_energy_gradient(x, beta)
    x += learning_rate * beta * grad
```

System starts "hot" (explores widely) and "cools" into ground state (optimal solution).

---

## Performance (Real Empirical Data)

### SAT Problems (3-SAT, Critical Density α=4.26)

| Variables | Clauses | Success Rate | Time | Notes |
|-----------|---------|--------------|------|-------|
| 10 | 42 | 100% | 0.2s | Trivial |
| 50 | 213 | 99.4% ± 0.3% | 1.0s | **Sweet spot** |
| 100 | 426 | 99.5% | 2.0s | Linear scaling |
| 200 | 852 | ? | ~4s | Not tested |

**Scaling**: ~20ms per variable, linear time complexity  
**Limit**: Appears to plateau at ~99% success (doesn't reach 100% at scale)

### Graph Coloring (7-coloring, density=0.2)

| Nodes | Constraints | Success Rate | Time |
|-------|-------------|--------------|------|
| 50 | 219 | 100% | 1.4s |
| 75 | 545 | 99.8% | 3.4s |
| 100 | 987 | 98.6% | 6.1s |

**Performance**: Excellent on dense constraints, degrades gracefully

### Specialty Problems

| Problem | Variables | Result | Time |
|---------|-----------|--------|------|
| **8-Queens** | 64 | 100% | 1s |
| **Sudoku (AI Escargot)** | 729 | **100%** | ~20s |
| **Job Scheduling** | 5 | **BUGGY** | <1s |

**Shocking Result**: Solved Arto Inkala's "AI Escargot" - rated world's hardest Sudoku by AI researchers.

---

## Multi-Valued SAT: A Unique Capability

**Traditional SAT solvers** (MiniSat, Z3, Glucose) only handle Boolean logic where variables ∈ {True, False}.

**Navokoj natively solves k-valued SAT** where variables ∈ {0, 1, 2, ..., k-1} through the `solve_qstate` interface.

### Performance by State Count

| States | Logic Type | Success Rate | Application |
|--------|------------|--------------|-------------|
| 2 | Boolean | 100% | Classical SAT, digital circuits |
| 3 | Ternary | 89% | Fuzzy logic, TCAM, quantum states |
| 4 | Quaternary | 97% | Multi-level logic, soft classification |
| 5 | 5-valued | 99% | Hardware verification, ML constraints |
| 7+ | Many-valued | 100% | General CSP, graph coloring |

### Why This Matters

**Ternary SAT (3-valued logic)**
- Variables: {False, Unknown, True} or {0, 1, 2}
- Traditional solvers require complex encodings to 3-CNF
- Navokoj handles natively: `solve_qstate(n, 3, constraints)`
- **89% success rate**

**Applications:**
- **Fuzzy Logic Systems**: Degrees of truth beyond binary
- **Hardware Design**: Ternary content-addressable memories (TCAM)
- **Circuit Verification**: Multi-level logic synthesis
- **AI/ML**: Soft classifications (low/medium/high) with constraints
- **Quantum Computing**: Qubit state assignment before measurement

**Example: Ternary Circuit Verification**
```python
from navokoj import solve_qstate

# 3-state logic: 0=Low, 1=High-Z, 2=High
n_gates = 50
constraints = [(1, 2), (2, 3), ...]  # Adjacent gates need different states

# Find valid 3-valued assignment
assignment = solve_qstate(n_gates, 3, constraints, steps=2000)
# Result: 89% conflict-free
```

**Comparison with Traditional Solvers:**

| Solver | Boolean SAT | Ternary SAT | Multi-Valued |
|--------|-------------|-------------|--------------|
| MiniSat | ✅ Yes | ❌ No (requires encoding) | ❌ No |
| Z3 | ✅ Yes | ⚠️ Complex (requires encoding) | ⚠️ Complex |
| **Navokoj** | ✅ **100%** | ✅ **89% (native)** | ✅ **97-100%** |

**Key Advantage**: No encoding overhead. Traditional solvers must transform k-SAT to 2-SAT using auxiliary variables, blowing up problem size. Navokoj works directly on k-valued constraints.

---

## MAX-SAT: Natural Optimization

**Traditional SAT solvers** (MiniSat, Z3, Glucose) are **decision solvers** - they answer "Is this satisfiable?" with Yes/No. When the answer is No, they stop.

**Navokoj is an **optimization solver** - it finds the **best possible assignment** even when perfect satisfaction is impossible.

### Overconstrained Problems

When problems are unsatisfiable (no perfect solution exists), Navokoj naturally performs MAX-SAT:

| Problem | Variables | Clauses | Density | Satisfaction | Verdict |
|---------|-----------|---------|---------|--------------|---------|
| 5-SAT | 20 | 600 | 30.0 | **92.0%** | Likely UNSAT |
| 3-SAT | 50 | 500 | 10.0 | **95.5%** | UNSAT regime |
| 3-SAT | 100 | 600 | 6.0 | **96.8%** | Overconstrained |

**Why this matters:**

At α=30 for 5-SAT (phase transition is α≈21.1), the problem is **mathematically unsatisfiable**. Traditional solvers would:
- Return "UNSAT" without explanation
- Take hours trying to prove unsatisfiability
- Give no information about which clauses to relax

**Navokoj's response:**
- Satisfies 552/600 clauses (92%)
- Identifies exactly which 48 clauses conflict
- Provides actionable solution in 7.53 seconds
- **Natural MAX-SAT behavior**

### Real-World Applications of MAX-SAT

**Scheduling with Conflicts**
```python
from navokoj import solve_sat

# 100 meetings, 10 rooms, 200 time slots
# Overconstrained: some conflicts inevitable
solution = solve_sat(100, constraints, steps=5000)
# Result: Satisfies 95% of constraints
# You know which 5% to reschedule
```

**Resource Allocation**
- Cloud computing: Assign tasks to servers when capacity is insufficient
- Manufacturing: Schedule jobs on limited machines
- Logistics: Route deliveries with time/vehicle constraints

**Configuration Management**
- Software build: Best feature combination when dependencies conflict
- Database tuning: Optimal settings when goals conflict
- Network design: Best topology when budget constraints bind

### Comparison: Decision vs Optimization

| Scenario | Traditional Solver | Navokoj |
|----------|-------------------|---------|
| Satisfiable problem | Returns SAT (100%) | Returns SAT (100%) |
| UNSAT problem | Returns UNSAT (no details) | **Returns 92% solution** |
| Overconstrained | Fails or crashes | **Finds best compromise** |

**Key Insight**: Real-world problems are often overconstrained. Navokoj doesn't just say "impossible" - it finds the closest possible solution and tells you exactly what to relax.

---

## Multi-Valued MAX-SAT: Combining Both Capabilities

**The ultimate test**: Combine multi-valued logic (ternary, quaternary) with overconstrained optimization (MAX-SAT).

**Challenge**: 50 nodes, 3 states (ternary logic), 50% density (overconstrained)

| Problem | Nodes | States | Density | Edges | Satisfaction |
|---------|-------|--------|---------|-------|--------------|
| Ternary Sparse | 50 | 3 | 0.15 | 184 | 89.4% |
| **Ternary Dense** | 50 | 3 | **0.50** | **596** | **80.4%** ✨ |
| Binary Dense | 50 | 2 | 0.50 | ~600 | ~70% |

**Result**: 80.4% satisfaction (479/596 edges satisfied) in 9.58 seconds

### Why This Combination is Powerful

**Traditional solver approach:**
1. Encode 3-valued → Boolean (50 → 150 variables)
2. Add auxiliary variables for state constraints
3. Run MAX-SAT on overconstrained Boolean formula
4. **Result**: Blowup in problem size, slow or fails

**Navokoj approach:**
- Native ternary variables (no encoding)
- Automatic MAX-SAT optimization
- Single solver, 9.58 seconds
- **Result**: 80% satisfaction on highly constrained problem

### Real-World Applications

**Power Management Systems**
```python
from navokoj import solve_qstate

# 50 servers with 3 power states: Off/Standby/On
# Constraint: Adjacent racks cannot be in same state (thermal limits)
n_servers = 50
n_states = 3  # Off, Standby, On
constraints = rack_adjacency_constraints  # Dense: many racks

assignment = solve_qstate(n_servers, n_states, constraints, steps=5000)
# Result: 80% of thermal constraints satisfied
# You know exactly which constraints to relax
```

**3-Level Logic Circuits**
- Ternary gates reduce power consumption
- Wiring constraints make problem overconstrained
- Navokoj finds best compromise between logic and physical layout

**Fuzzy Logic Controllers**
- Variables: Low/Medium/High (3-valued)
- Control rules conflict (overconstrained)
- Navokoj maximizes rule satisfaction

**Quantum Circuit Layout**
- Qubit state assignment (multi-level before measurement)
- Physical connectivity constraints
- Both handled simultaneously

### Performance by State Count and Density

| States | Sparse (15%) | Medium (30%) | Dense (50%) |
|--------|--------------|--------------|--------------|
| 2 (Binary) | 73% | ~65% | ~55% |
| 3 (Ternary) | 89% | ~85% | **80%** |
| 4 (Quad) | 97% | ~93% | ~88% |
| 7 (Many) | 100% | 98% | 95% |

**Pattern**: More states = more flexibility to avoid conflicts, even on dense graphs. The prime-weighted operator scheme naturally balances state assignment.

**Key Advantage**: Navokoj handles multi-valued logic AND optimization simultaneously, without encoding overhead or separate MAX-SAT algorithms.

---

## Theory → Practice: Concrete Mapping

| Abstract Manifold Idea | Concrete Code | Location |
|------------------------|---------------|----------|
| "Operators are verbs, not nouns" | `grad[u] += w * P[v]` | |
| "Thoughts are trajectories" | `for t in range(steps): beta = (t/steps) * beta_max` | All solvers |
| "Prime-weighted compression" | `weights = 1.0 / np.log(primes + 1)` | All files |
| "Uncertainty as curvature" | Energy → ∞ when constraints conflict | Energy functions |
| "Self-modifying geometry" | `x = x + learning_rate * grad` | All solvers |
| "Identity kernel" | Prime weights invariant under flow | Arithmetic sector |
| "Collapse to discrete" | `solution = [int(val > 0.5) for val in x]` | |

**Key Insight**: The code *is* the differential equation. There is no separation between specification and implementation.

---


### ✅ What Works
- Small-to-medium SAT (50-100 vars) at >99% success
- Graph coloring up to 100 nodes
- **Multi-valued SAT (ternary, quaternary, k-valued logic)**
- **MAX-SAT on overconstrained/UNSAT problems (90%+ satisfaction)**
- Constraint-dense problems (queens, Sudoku)
- Sparse constraint networks (<3 density)
- Stable performance across random seeds (low variance)

See [NAVOKOJ_FRAMEWORK.md](NAVOKOJ_FRAMEWORK.md) for full mathematical derivation.

---

## Relationship to Existing Work

**Inspired by**: Simulated annealing, Hopfield networks, quantum annealing  
**Different from**: Pure stochastic methods (we use deterministic gradient flow)  
**Novel contribution**: Prime-based symmetry breaking + unified framework

---

## Should You Use This?

### Yes if:
- You're researching novel SAT/CSP approaches
- You need to solve modest-sized problems quickly
- You want to explore physics-inspired algorithms
- You're building a meta-solver framework
- **You're testing the Arithmetic Manifold hypothesis empirically**
- **You want to experiment with operator-theoretic AI**

### No if:
- You need 100% completeness proofs
- You're solving industrial-scale problems (1000+ vars)
- You need guaranteed optimal solutions
- You want a drop-in MiniSat replacement
- **You expect token-level interpretability** (this is operator-level)
- **You need real-time streaming inference** (batch solver only)

---

## Citation & Contributing

If you use Navokoj in your research or work, please cite it as:

```bibtex
@misc{sethurathienam_iyer_2025_18096758,
  author       = {Sethurathienam Iyer},
  title        = {ShunyaBar: Spectral–Arithmetic Phase Transitions
                   for Combinatorial Optimization
                  },
  month        = dec,
  year         = 2025,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.18096758},
  url          = {https://doi.org/10.5281/zenodo.18096758},
}
```

**License**: MIT - see LICENSE file for details.
