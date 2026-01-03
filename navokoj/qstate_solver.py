"""
Q-State Solver Module: Discrete State Assignment via Geometric Operators.

Implements Q-state constraint satisfaction (graph coloring, register allocation)
using softmax relaxation and repulsive forces between adjacent nodes.

Each node has a continuous potential over Q states; gradient flow pushes
connected nodes toward different states.

Author: Sethu Iyer <sethuiyer95@gmail.com>
License: MIT
"""

import random
from typing import List, Tuple, Dict, Any

import numpy as np

__all__ = ["solve_qstate", "generate_q_graph", "verify_qstate"]


def _softmax(x: np.ndarray, beta: float) -> np.ndarray:
    """
    Softmax with temperature control and numerical stability.
    
    As beta → ∞, approaches hard argmax (discrete state selection).
    As beta → 0, approaches uniform distribution (maximum uncertainty).
    
    Args:
        x: Input potential matrix [n_nodes, n_states]
        beta: Inverse temperature parameter
        
    Returns:
        Probability matrix [n_nodes, n_states]
    """
    # Shift for numerical stability (prevent overflow in exp)
    shift_x = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(beta * shift_x)
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


def solve_qstate(
    n_nodes: int,
    n_states: int,
    constraints: List[Tuple[int, int]],
    steps: int = 2000,
    learning_rate: float = 0.1,
    beta_max: float = 5.0,
    seed: int = None,
) -> List[int]:
    """
    Solve Q-state assignment using geometric operator flow.
    
    Maps discrete state assignment to continuous potential landscape:
    1. Each node has potential vector over Q states
    2. Softmax converts potentials to probabilities
    3. Adjacent nodes repel via gradient of overlap energy
    4. Adiabatic cooling forces classical collapse
    
    Args:
        n_nodes: Number of nodes in graph
        n_states: Number of possible states per node
        constraints: Edge list (u, v) requiring different states
        steps: Cooling steps
        learning_rate: Gradient descent step size
        beta_max: Final inverse temperature (forces collapse)
        seed: Random seed
        
    Returns:
        List of assigned states (1-indexed)
        
    Example:
        >>> # Graph coloring with 7 colors
        >>> constraints = [(1, 2), (2, 3), (1, 3)]  # Triangle
        >>> solve_qstate(3, 7, constraints)
        [1, 2, 3]  # Each vertex different color
    """
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    print(f"--- Q-STATE SOLVE: {n_nodes} nodes, {n_states} states ---")

    # 1. Arithmetic Sector: Prime-weighted operators
    # Each edge gets unique spectral signature to break symmetries
    primes = []
    candidate = 2
    while len(primes) < len(constraints):
        is_prime = all(candidate % p != 0 for p in primes)
        if is_prime:
            primes.append(candidate)
        candidate += 1
    weights = 1.0 / np.log(np.array(primes) + 1.0)

    # 2. Geometric Sector: Continuous potential matrix
    # X[i, k] = potential of node i being in state k
    # Initialize with small random potentials (symmetry breaking)
    potentials = np.random.normal(0.0, 0.1, (n_nodes, n_states))

    # Preprocess constraints for fast lookup
    edges = [(u - 1, v - 1) for u, v in constraints]  # Convert to 0-indexed

    # 3. Dynamic Sector: Adiabatic sweep toward classical state
    for step in range(steps):
        # Temperature schedule: smooth annealing to force decision
        # Low beta = quantum superposition (all states likely)
        # High beta = classical collapse (one state selected)
        beta = (step / steps) * beta_max

        # Convert potentials to probabilities via softmax
        probabilities = _softmax(potentials, beta)

        # Compute gradient: repulsive force between adjacent nodes
        # If neighbor j is strongly in state k, node i should avoid state k
        gradient = np.zeros_like(potentials)

        for edge_idx, (u, v) in enumerate(edges):
            weight = weights[edge_idx]

            # Repulsive force: push away from neighbor's state distribution
            gradient[u] += weight * probabilities[v]
            gradient[v] += weight * probabilities[u]

        # Update dynamics: minimize overlap energy
        potentials = potentials - learning_rate * gradient

        # Arithmetic perturbation: escape saddle points with noise
        if step % 100 == 0:
            noise = np.random.normal(0.0, 0.05, potentials.shape)
            potentials += noise

    # 4. Collapse: Argmax over state potentials to get discrete assignment
    # As beta → ∞ during sweep, this approaches classical measurement
    return (np.argmax(potentials, axis=1) + 1).tolist()  # 1-indexed states


def generate_q_graph(
    n_nodes: int, density: float = 0.2, seed: int = None
) -> List[Tuple[int, int]]:
    """
    Generate random graph for Q-state coloring.
    
    Creates undirected graph where each edge represents a constraint
    requiring the two nodes to have different states.
    
    Args:
        n_nodes: Number of nodes
        density: Probability of edge between any two nodes
        seed: Random seed
        
    Returns:
        List of edge constraints (u, v)
        
    Example:
        >>> edges = generate_q_graph(50, density=0.2)
        >>> len(edges)  # ~245 edges
        245
    """
    if seed is not None:
        random.seed(seed)

    constraints = []
    for i in range(1, n_nodes + 1):
        for j in range(i + 1, n_nodes + 1):
            if random.random() < density:
                constraints.append((i, j))

    return constraints


def verify_qstate(
    constraints: List[Tuple[int, int]], assignment: List[int]
) -> int:
    """
    Verify Q-state solution by counting constraint violations.
    
    Args:
        constraints: Edge constraints requiring different states
        assignment: Assigned state for each node
        
    Returns:
        Number of violated constraints
        
    Example:
        >>> constraints = [(1, 2), (2, 3)]
        >>> assignment = [1, 2, 2]
        >>> verify_qstate(constraints, assignment)
        1  # Node 2 and 3 have same state
    """
    conflicts = 0
    for u, v in constraints:
        if assignment[u - 1] == assignment[v - 1]:
            conflicts += 1
    return conflicts