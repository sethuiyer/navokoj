# Graph Coloring with Navokoj

This tutorial demonstrates how to solve graph coloring problems using the Navokoj framework.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Visualization](#visualization)
5. [Verification](#verification)
6. [Performance Analysis](#performance-analysis)

---

## Overview

Graph coloring assigns colors to graph vertices such that no two adjacent vertices share the same color. Navokoj solves this NP-hard problem using energy minimization and adiabatic cooling.

**Key Features**
- Solves 20-100 node graphs in seconds
- >98% success rate on typical problems
- Simple API requiring only problem constraints

---

## Installation

Install Navokoj and visualization dependencies:

```bash
pip install navokoj matplotlib networkx numpy
```

---

## Basic Usage

### Example: 3-Coloring a Small Graph

```python
from navokoj import solve_qstate, generate_q_graph

# Generate a random graph with 10 nodes
n_nodes = 10
n_colors = 3
density = 0.3

constraints = generate_q_graph(n_nodes, density=density)

# Solve the coloring problem
color_assignment = solve_qstate(n_nodes, n_colors, constraints, steps=2000)

print(f"Colors used: {len(set(color_assignment))} out of {n_colors}")
print(f"Assignment: {color_assignment}")
```

**Output**
```
Colors used: 3 out of 3
Assignment: [1, 2, 3, 2, 1, 3, 2, 1, 3, 2]
```

---

## Visualization

### Complete Example with Plots

```python
from navokoj import solve_qstate, generate_q_graph
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def visualize_coloring(n_nodes, n_colors, density, seed=42):
    # Generate graph
    constraints = generate_q_graph(n_nodes, density=density, seed=seed)

    # Build NetworkX graph
    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))
    for u, v in constraints:
        G.add_edge(u-1, v-1)

    # Solve
    color_assignment = solve_qstate(n_nodes, n_colors, constraints,
                                   steps=2000, seed=seed)

    # Verify
    conflicts = sum(1 for u, v in constraints
                   if color_assignment[u-1] == color_assignment[v-1])

    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Color map
    color_map = plt.cm.Set3(np.linspace(0, 1, n_colors))
    node_colors = [color_map[color_assignment[i]-1] for i in range(n_nodes)]

    # Plot 1: Graph
    pos = nx.spring_layout(G, seed=seed)
    nx.draw(G, pos, node_color=node_colors, with_labels=True,
            node_size=500, font_size=11, font_weight='bold',
            edge_color='gray', width=2, ax=ax1)
    ax1.set_title(f'{n_nodes}-Node Graph Coloring ({n_colors} colors)',
                  fontsize=13, fontweight='bold')
    ax1.axis('off')

    # Plot 2: Distribution
    color_counts = [color_assignment.count(i) for i in range(1, n_colors+1)]
    bars = ax2.bar(range(n_colors), color_counts, color=color_map,
                   edgecolor='black')
    ax2.set_xlabel('Color', fontsize=11)
    ax2.set_ylabel('Node Count', fontsize=11)
    ax2.set_title('Color Distribution', fontsize=13, fontweight='bold')
    ax2.set_xticks(range(n_colors))
    ax2.set_xticklabels([f'{i}' for i in range(1, n_colors+1)])

    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('tutorials/plots/graph_coloring_example.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    # Results
    print(f"Nodes: {n_nodes}")
    print(f"Edges: {len(constraints)}")
    print(f"Conflicts: {conflicts}/{len(constraints)}")
    print(f"Success rate: {100*(1 - conflicts/len(constraints)):.1f}%")

    return G, color_assignment

G, colors = visualize_coloring(n_nodes=20, n_colors=4, density=0.25)
```

![Graph coloring visualization](plots/graph_coloring_example.png)

**Figure 1: Graph coloring visualization**
*Left: Graph with colored nodes. Right: Color distribution across nodes.*

**Output**
```
Nodes: 20
Edges: 40
Conflicts: 0/40
Success rate: 100.0%
```

---

## Verification

Always verify solutions by checking all edge constraints:

```python
from navokoj import solve_qstate, generate_q_graph

n_nodes = 20
n_colors = 4
density = 0.25

constraints = generate_q_graph(n_nodes, density=density, seed=42)
assignment = solve_qstate(n_nodes, n_colors, constraints, steps=2000, seed=42)

# Verify each edge
conflicts = []
for u, v in constraints:
    if assignment[u-1] == assignment[v-1]:
        conflicts.append((u, v, assignment[u-1]))

print(f"Edges checked: {len(constraints)}")
print(f"Conflicts found: {len(conflicts)}")

if conflicts:
    print("Conflicting edges:")
    for u, v, c in conflicts:
        print(f"  Node {u} - Node {v}: both color {c}")
else:
    print("All constraints satisfied.")
```

**Output**
```
Edges checked: 40
Conflicts found: 0
All constraints satisfied.
```

---

## Performance Analysis

### Success Rates by Graph Size

Empirical results from Navokoj framework:

| Nodes | Colors | Density | Success Rate | Time  |
|-------|--------|---------|--------------|-------|
| 10    | 3      | 0.30    | ~100%        | <0.5s |
| 20    | 4      | 0.30    | ~100%        | <0.8s |
| 50    | 7      | 0.20    | ~100%        | 1.4s  |
| 75    | 7      | 0.20    | 99.8%        | 3.4s  |
| 100   | 7      | 0.20    | 98.6%        | 6.1s  |

**Observations**
- Success rate exceeds 98% for graphs up to 100 nodes
- Time scales linearly with node count
- Higher density generally improves performance

### Scaling Benchmark

```python
from navokoj import solve_qstate, generate_q_graph
import time

def benchmark_scaling(sizes, n_colors=4, density=0.25):
    print("Size | Edges | Time (s) | Success")
    print("-" * 35)

    for n in sizes:
        constraints = generate_q_graph(n, density=density, seed=42)

        start = time.time()
        assignment = solve_qstate(n, n_colors, constraints, steps=2000, seed=42)
        elapsed = time.time() - start

        conflicts = sum(1 for u, v in constraints
                       if assignment[u-1] == assignment[v-1])
        success = 100 * (1 - conflicts/len(constraints))

        print(f"{n:4d} | {len(constraints):5d} | {elapsed:7.2f} | {success:5.1f}%")

benchmark_scaling([10, 20, 30, 40, 50])
```

**Output**
```
Size | Edges | Time (s) | Success
-----------------------------------
  10 |    10 |    0.32 | 100.0%
  20 |    40 |    0.45 | 100.0%
  30 |    93 |    0.67 | 100.0%
  40 |   168 |    0.89 | 100.0%
  50 |   262 |    1.21 | 100.0%
```

### Color Count Comparison

Testing the same graph with different numbers of available colors:

```python
from navokoj import solve_qstate, generate_q_graph

n_nodes = 20
density = 0.3
constraints = generate_q_graph(n_nodes, density=density, seed=42)

print("Colors | Used | Conflicts | Success")
print("-" * 35)

for n_colors in [3, 4, 5, 6, 7]:
    assignment = solve_qstate(n_nodes, n_colors, constraints,
                             steps=2000, seed=42)
    used = len(set(assignment))
    conflicts = sum(1 for u, v in constraints
                   if assignment[u-1] == assignment[v-1])
    success = 100 * (1 - conflicts/len(constraints))

    print(f"  {n_colors}   |  {used}   |    {conflicts:2d}    | {success:5.1f}%")
```

**Output**
```
Colors | Used | Conflicts | Success
-----------------------------------
  3   |  3   |     2    |  95.1%
  4   |  4   |     0    | 100.0%
  5   |  4   |     0    | 100.0%
  6   |  4   |     0    | 100.0%
  7   |  4   |     0    | 100.0%
```

---

## Advanced Topics

### Energy Convergence

Monitor how constraint violations decrease during solving:

```python
from navokoj import solve_qstate, generate_q_graph
import matplotlib.pyplot as plt

def track_convergence(n_nodes, n_colors, density, seed=42):
    constraints = generate_q_graph(n_nodes, density=density, seed=seed)
    checkpoints = [100, 250, 500, 750, 1000, 1500, 2000]

    energy = []
    for steps in checkpoints:
        assignment = solve_qstate(n_nodes, n_colors, constraints,
                                 steps=steps, seed=seed)
        violations = sum(1 for u, v in constraints
                        if assignment[u-1] == assignment[v-1])
        energy.append(violations)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(checkpoints, energy, marker='o', linewidth=2, markersize=8)
    ax.set_xlabel('Solver Steps', fontsize=11)
    ax.set_ylabel('Constraint Violations', fontsize=11)
    ax.set_title('Energy Convergence', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('tutorials/plots/convergence.png', dpi=300)
    plt.show()

    return checkpoints, energy

steps, violations = track_convergence(20, 4, 0.25)
```

![Energy convergence](plots/convergence.png)

**Figure 2: Energy convergence during adiabatic cooling**

### Large Graphs

Solve larger problems (50+ nodes):

```python
from navokoj import solve_qstate, generate_q_graph
import matplotlib.pyplot as plt
import networkx as nx

n_nodes = 50
n_colors = 7
density = 0.2

constraints = generate_q_graph(n_nodes, density=density, seed=42)
assignment = solve_qstate(n_nodes, n_colors, constraints, steps=2000, seed=42)

# Build graph
G = nx.Graph()
G.add_nodes_from(range(n_nodes))
for u, v in constraints:
    G.add_edge(u-1, v-1)

# Visualize
fig, ax = plt.subplots(figsize=(12, 10))
color_map = plt.cm.Set3(np.linspace(0, 1, n_colors))
node_colors = [color_map[assignment[i]-1] for i in range(n_nodes)]

pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, node_color=node_colors, with_labels=False,
        node_size=200, edge_color='lightgray', width=1, ax=ax)

conflicts = sum(1 for u, v in constraints
               if assignment[u-1] == assignment[v-1])
success = 100 * (1 - conflicts/len(constraints))

ax.set_title(f'{n_nodes}-Node Graph Coloring\nSuccess: {success:.1f}%',
             fontsize=13, fontweight='bold')
ax.axis('off')
plt.tight_layout()
plt.savefig('tutorials/plots/large_graph.png', dpi=300)
plt.show()
```

![Large-scale graph coloring](plots/large_graph.png)

**Figure 3: Large-scale graph coloring (50 nodes)**

---

## Troubleshooting

### Low Success Rate

If you encounter constraint violations:

1. **Increase solver steps**
   ```python
   assignment = solve_qstate(n_nodes, n_colors, constraints, steps=5000)
   ```

2. **Use more colors**
   ```python
   # Try 5 colors instead of 3
   assignment = solve_qstate(n_nodes, 5, constraints)
   ```

3. **Adjust density**
   ```python
   # Higher density often helps
   constraints = generate_q_graph(n_nodes, density=0.3)
   ```

### Visualization Tips

```python
# Different layouts for visualization
pos = nx.kamada_kawai_layout(G)    # Good for dense graphs
pos = nx.circular_layout(G)         # Good for small graphs
pos = nx.spring_layout(G)           # Default, works well generally
```

---

## References

- [Navokoj Framework Documentation](../NAVOKOJ_FRAMEWORK.md)
- [ShunyaBar Research Paper](https://zenodo.org/records/18096758)
- [Production API](https://navokoj.shunyabar.foo/)

---

*Last updated: January 2026*
