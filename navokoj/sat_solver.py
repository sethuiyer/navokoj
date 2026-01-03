"""
SAT Solver Module: Constraint Satisfaction via Geometric Operators.

This module implements a physics-inspired SAT solver that treats boolean
satisfaction as energy minimization on a continuous manifold. Uses prime-weighted
operators and adiabatic cooling to find solutions without combinatorial search.

Key innovations:
- Prime-weighted constraints for symmetry breaking
- Continuous probability relaxation of boolean variables
- Adiabatic flow (temperature schedule) for basin convergence
- Gradient-based energy minimization

Author: Sethu Iyer <sethuiyer95@gmail.com>
License: MIT
"""

import random
from typing import List, Tuple, Dict, Any

import numpy as np

__all__ = [
    "solve_sat",
    "generate_3sat",
    "encode_n_queens",
    "encode_sudoku",
]


def _generate_primes(n: int) -> np.ndarray:
    """
    Generate first n prime numbers for constraint weighting.
    
    Why primes? Primes provide an irreducible basis where each constraint
    gets a unique spectral signature. This breaks permutation symmetry
    and prevents degenerate trade-offs between constraints.
    
    Args:
        n: Number of primes to generate
        
    Returns:
        Array of n prime numbers
    """
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = all(candidate % p != 0 for p in primes)
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return np.array(primes)


def solve_sat(
    num_vars: int,
    clauses: List[List[int]],
    steps: int = 1000,
    learning_rate: float = 0.1,
    beta_max: float = 2.5,
    seed: int = None,
) -> List[int]:
    """
    Solve SAT problem using geometric flow minimization.
    
    This implements the core Navokoj algorithm:
    1. Arithmetic Sector: Assign prime weights to each constraint
    2. Geometric Sector: Initialize continuous state space (probabilities)
    3. Dynamic Sector: Perform adiabatic sweep with gradient descent
    4. Collapse: Threshold continuous state to discrete solution
    
    Args:
        num_vars: Number of boolean variables
        clauses: List of clauses, each clause is list of ints (positive=variable, negative=negated)
        steps: Number of adiabatic cooling steps
        learning_rate: Step size for gradient descent
        beta_max: Maximum inverse temperature (controls cooling schedule)
        seed: Random seed for reproducibility
        
    Returns:
        List of 0/1 assignments for each variable
        
    Example:
        >>> clauses = [[1, 2], [-1, 3]]  # (x1 OR x2) AND (NOT x1 OR x3)
        >>> solve_sat(3, clauses, steps=1000)
        [1, 0, 1]  # Solution: x1=True, x2=False, x3=True
    """
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    # 1. Arithmetic Sector: Prime-weighted operators for symmetry breaking
    # Each constraint gets unique spectral signature via prime weighting
    primes = _generate_primes(len(clauses))
    weights = 1.0 / np.log(primes + 1.0)  # w_c = 1/log(p_c)

    # 2. Geometric Sector: Continuous state initialization
    # Start at maximum entropy (0.5) with small noise to break symmetries
    state = np.full(num_vars, 0.5) + np.random.normal(0, 0.001, num_vars)

    # 3. Dynamic Sector: Adiabatic sweep with gradient flow
    for step in range(steps):
        # Temperature schedule: linear ramp from 0 to beta_max
        # Low beta = hot (exploration), high beta = cold (exploitation)
        beta = (step / steps) * beta_max

        # Compute gradient of energy landscape
        gradient = np.zeros(num_vars)

        for clause_idx, clause in enumerate(clauses):
            # Soft logic: compute probability clause is satisfied
            # P(clause=False) = Product(1 - P(literal=True))
            unsat_prob = 1.0
            lit_probs = []

            for lit in clause:
                var_idx = abs(lit) - 1
                # For positive literal: P=true = state[var]
                # For negative literal: P=true = 1 - state[var]
                prob = state[var_idx] if lit > 0 else (1.0 - state[var_idx])
                unsat_prob *= 1.0 - prob
                lit_probs.append(prob)

            sat_prob = 1.0 - unsat_prob + 1e-9  # Add epsilon to avoid log(0)

            # Energy: E = -w_c * log(P(satisfied))
            # We want to minimize energy, so follow negative gradient
            # Coefficient comes from chain rule: dE/dx = dE/dP * dP/dx
            coeff = weights[clause_idx] / sat_prob * unsat_prob

            # Add gradient contribution from each literal in clause
            for lit_idx, lit in enumerate(clause):
                var_idx = abs(lit) - 1
                # Derivative sign: d/dx(x) = +1, d/dx(1-x) = -1
                sign = 1.0 if lit > 0 else -1.0

                # Gradient contribution: the arithmetic "nudge"
                gradient[var_idx] += coeff * sign * (1.0 / (1.0 - lit_probs[lit_idx] + 1e-9))

        # Update dynamics: gradient descent with temperature scaling
        # As beta increases, system becomes more rigid (less exploration)
        effective_lr = learning_rate * beta
        state = state + effective_lr * gradient

        # Project to valid probability space (0,1) with small epsilon
        # This prevents numerical instability in log calculations
        state = np.clip(state, 0.001, 0.999)

    # 4. Collapse: Convert continuous probabilities to discrete boolean values
    # Threshold at 0.5: probability > 0.5 becomes True (1), else False (0)
    return [int(val > 0.5) for val in state]


def generate_3sat(n_vars: int, alpha: float = 4.26, seed: int = None) -> List[List[int]]:
    """
    Generate random 3-SAT instance at critical density.
    
    The critical density α ≈ 4.26 is where 3-SAT undergoes phase transition
    from easy to hard. Problems at this density are maximally difficult.
    
    Args:
        n_vars: Number of variables
        alpha: Clause-to-variable ratio (critical value = 4.26)
        seed: Random seed for reproducibility
        
    Returns:
        List of clauses, each clause is list of 3 literals
        
    Example:
        >>> clauses = generate_3sat(50, alpha=4.26)
        >>> len(clauses)  # ~213 clauses
        213
    """
    if seed is not None:
        random.seed(seed)

    n_clauses = int(n_vars * alpha)
    clauses = []

    print(f"Generating Critical 3-SAT: {n_vars} vars, {n_clauses} clauses...")

    while len(clauses) < n_clauses:
        # Select 3 distinct variables
        var_indices = random.sample(range(1, n_vars + 1), 3)
        # Randomly negate each variable with 50% probability
        clause = [v if random.random() > 0.5 else -v for v in var_indices]
        clauses.append(clause)

    return clauses


def encode_n_queens(board_size: int) -> Tuple[int, List[List[int]]]:
    """
    Encode N-Queens problem as SAT clauses.
    
    Variables: N×N boolean grid where True = queen at position
    Constraints:
    1. At least one queen per row
    2. At most one queen per row
    3. At most one queen per column
    4. At most one queen per diagonal
    
    Args:
        board_size: Size of N×N board (N)
        
    Returns:
        Tuple of (num_vars, clauses)
        
    Example:
        >>> n_vars, clauses = encode_n_queens(8)
        >>> n_vars  # 64 variables for 8×8 board
        64
    """
    print(f"Encoding {board_size}-Queens ({board_size*board_size} vars)...")
    clauses = []

    def var(row: int, col: int) -> int:
        """Map (row, col) to SAT variable index (1-indexed)"""
        return (row * board_size + col) + 1

    # Constraint 1: At least one queen per row
    for r in range(board_size):
        clauses.append([var(r, c) for c in range(board_size)])

    # Constraint 2: At most one queen per row (pairwise exclusion)
    for r in range(board_size):
        for c1 in range(board_size):
            for c2 in range(c1 + 1, board_size):
                clauses.append([-var(r, c1), -var(r, c2)])

    # Constraint 3: At most one queen per column (pairwise exclusion)
    for c in range(board_size):
        for r1 in range(board_size):
            for r2 in range(r1 + 1, board_size):
                clauses.append([-var(r1, c), -var(r2, c)])

    # Constraint 4: At most one queen per diagonal
    # Naive O(N^4) encoding, sufficient for typical board sizes
    for r1 in range(board_size):
        for c1 in range(board_size):
            for r2 in range(r1 + 1, board_size):
                for c2 in range(board_size):
                    if abs(r1 - r2) == abs(c1 - c2):
                        clauses.append([-var(r1, c1), -var(r2, c2)])

    return board_size * board_size, clauses


def encode_sudoku(grid_str: str) -> Tuple[int, List[List[int]]]:
    """
    Encode 9×9 Sudoku puzzle as SAT clauses.
    
    Uses 729 variables (9×9×9) where each variable represents
    "cell (r,c) has value v". Constraints enforce:
    1. Each cell has at least one value
    2. Each value appears at most once per row/column/box
    3. Given clues are fixed as unit clauses
    
    Args:
        grid_str: 9×9 grid with 1-9 for values, '.' or '0' for empty
        
    Returns:
        Tuple of (num_vars, clauses)
        
    Example:
        >>> grid = "8... ... etc"
        >>> n_vars, clauses = encode_sudoku(grid)
        >>> n_vars  # 729 variables
        729
    """
    N = 9
    clauses = []

    def var(row: int, col: int, val: int) -> int:
        """Map (row, col, value) to SAT variable (1-indexed)"""
        return (row * N + col) * N + val + 1

    print("Encoding Sudoku constraints...")

    # Constraint 1: Each cell has at least one value
    for r in range(N):
        for c in range(N):
            clauses.append([var(r, c, v) for v in range(N)])

    # Constraint 2: Each value appears at most once per row/column/box
    for v in range(N):
        # Row uniqueness
        for r in range(N):
            for c1 in range(N):
                for c2 in range(c1 + 1, N):
                    clauses.append([-var(r, c1, v), -var(r, c2, v)])

        # Column uniqueness
        for c in range(N):
            for r1 in range(N):
                for r2 in range(r1 + 1, N):
                    clauses.append([-var(r1, c, v), -var(r2, c, v)])

        # Box uniqueness (3×3 subgrids)
        for br in range(3):
            for bc in range(3):
                cells = []
                for i in range(3):
                    for j in range(3):
                        cells.append((br * 3 + i, bc * 3 + j))

                for i in range(len(cells)):
                    for j in range(i + 1, len(cells)):
                        r1, c1 = cells[i]
                        r2, c2 = cells[j]
                        clauses.append([-var(r1, c1, v), -var(r2, c2, v)])

    # Constraint 3: Fixed clues as unit clauses
    grid_clean = grid_str.replace("\n", "").replace(" ", "")
    for i, char in enumerate(grid_clean):
        if char in "123456789":
            val = int(char) - 1
            r, c = i // 9, i % 9
            clauses.append([var(r, c, val)])  # Unit clause: must be true

    return 729, clauses


def decode_sudoku(assignment: List[int]) -> List[List[str]]:
    """
    Convert SAT assignment back to Sudoku grid.
    
    Args:
        assignment: Boolean assignment from SAT solver
        
    Returns:
        9×9 grid as list of strings ('1'-'9' or '.' for empty)
    """
    N = 9
    grid = [["." for _ in range(N)] for _ in range(N)]

    for r in range(N):
        for c in range(N):
            for v in range(N):
                idx = (r * N + c) * N + v
                if assignment[idx] == 1:
                    grid[r][c] = str(v + 1)
                    break

    return grid


def verify_solution(clauses: List[List[int]], assignment: List[int]) -> float:
    """
    Verify SAT solution by checking clause satisfaction rate.
    
    Args:
        clauses: List of SAT clauses
        assignment: Boolean assignment to verify
        
    Returns:
        Fraction of clauses satisfied (0.0 to 1.0)
    """
    satisfied = 0
    for clause in clauses:
        clause_satisfied = False
        for lit in clause:
            var_val = assignment[abs(lit) - 1]
            if (lit > 0 and var_val == 1) or (lit < 0 and var_val == 0):
                clause_satisfied = True
                break
        if clause_satisfied:
            satisfied += 1

    return satisfied / len(clauses) if clauses else 1.0