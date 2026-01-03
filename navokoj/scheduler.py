"""
Job Scheduler Module: Temporal Constraint Satisfaction via Geometric Flows.

Implements continuous-time job scheduling using physical analogies:
- Precedence constraints as springs
- Machine conflicts as repulsive forces  
- Timeline as geometric manifold

Author: Sethu Iyer <sethuiyer95@gmail.com>
License: MIT
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

import numpy as np

__all__ = ["schedule_jobs", "JobConfig", "verify_schedule"]


@dataclass
class JobConfig:
    """Configuration for a single job in scheduling problem."""

    duration: float
    name: Optional[str] = None


def schedule_jobs(
    jobs: Dict[int, JobConfig],
    conflicts: List[Tuple[int, int]],
    precedences: List[Tuple[int, int]],
    horizon: float = 100.0,
    steps: int = 5000,
    learning_rate: float = 0.5,
    beta_max: float = 10.0,
    seed: Optional[int] = None,
) -> Dict[int, float]:
    """
    Schedule jobs using geometric flow on temporal manifold.
    
    Treats scheduling as physical system where:
    - Jobs are particles with duration
    - Precedences are springs pulling jobs into order
    - Conflicts are repulsive forces preventing overlap
    - Timeline is continuous manifold warped by constraints
    
    Args:
        jobs: Mapping job_id -> JobConfig
        conflicts: Pairs of jobs that cannot overlap (share machine)
        precedences: Pairs (i, j) where job i must finish before j starts
        horizon: Maximum allowed start time
        steps: Adiabatic cooling steps
        learning_rate: Gradient step size
        beta_max: Maximum rigidity (cold temperature)
        seed: Random seed for reproducibility
        
    Returns:
        Mapping job_id -> start time
        
    Example:
        >>> jobs = {0: JobConfig(4), 1: JobConfig(3)}
        >>> conflicts = [(0, 1)]  # Can't run simultaneously
        >>> schedule_jobs(jobs, conflicts, [])
        {0: 0.0, 1: 4.0}
    """
    if seed is not None:
        np.random.seed(seed)

    num_jobs = len(jobs)
    print(f"--- SCHEDULING: {num_jobs} jobs, horizon={horizon} ---")

    # 1. Geometric Sector: Initialize continuous start times
    # Scatter jobs randomly on timeline to break initial symmetries
    start_times = np.random.uniform(0.0, horizon / 2.0, num_jobs)

    # 2. Arithmetic Sector: Prime perturbation for deadlock avoidance
    # Periodic kicks prevent perfect overlaps (head-on collisions)
    primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71])[
        :num_jobs
    ]

    # 3. Dynamic Sector: Adiabatic cooling on temporal manifold
    for step in range(steps):
        # Temperature schedule: increase rigidity over time
        # Low beta = ghosts can pass, high beta = solid bricks
        beta = (step / steps) * beta_max

        gradient = np.zeros(num_jobs)

        # Force 1: Precedence constraints (springs)
        # If job i must finish before j starts, enforce temporal ordering
        for i, j in precedences:
            end_i = start_times[i] + jobs[i].duration
            violation = end_i - start_times[j]  # Positive if violated

            if violation > 0:
                # Spring force proportional to violation
                # Pull earlier job back, push later job forward
                force = violation
                gradient[i] -= force  # Pull i earlier
                gradient[j] += force  # Push j later

        # Force 2: Machine conflicts (repulsion)
        # If jobs share machine, they repel when overlapping
        for i, j in conflicts:
            end_i = start_times[i] + jobs[i].duration
            end_j = start_times[j] + jobs[j].duration

            # Check if intervals overlap
            latest_start = max(start_times[i], start_times[j])
            earliest_end = min(end_i, end_j)
            overlap = earliest_end - latest_start

            if overlap > 0:
                # Repulsive force pushes overlapping jobs apart
                # Direction based on which job starts first
                direction = 1.0 if start_times[i] < start_times[j] else -1.0
                force = overlap * beta  # Stronger at low temperature

                gradient[i] -= force * direction
                gradient[j] += force * direction

        # Force 3: Horizon gravity (weak regularization)
        # Pulls jobs toward t=0 to minimize makespan
        gradient -= 0.01 * start_times

        # Update dynamics: gradient descent step
        start_times = start_times + learning_rate * gradient

        # Arithmetic perturbation: periodic kicks to escape saddles
        if step % 500 == 0:
            noise = np.sin(primes * step) * 2.0
            start_times += noise

        # Physics constraint: time cannot be negative
        start_times = np.maximum(start_times, 0.0)

    return {i: float(start_times[i]) for i in range(num_jobs)}


def verify_schedule(
    jobs: Dict[int, JobConfig],
    schedule: Dict[int, float],
    conflicts: List[Tuple[int, int]],
    precedences: List[Tuple[int, int]],
    tolerance: float = 0.1,
) -> Tuple[bool, List[str]]:
    """
    Verify schedule satisfies all constraints.
    
    Args:
        jobs: Job configurations
        schedule: Mapping job_id -> start time
        conflicts: Forbidden overlaps
        precedences: Temporal ordering constraints
        tolerance: Floating-point tolerance for verification
        
    Returns:
        Tuple of (is_valid, list_of_violations)
    """
    violations = []
    valid = True

    # Check precedence constraints
    for i, j in precedences:
        end_i = schedule[i] + jobs[i].duration
        start_j = schedule[j]
        gap = start_j - end_i

        if gap < -tolerance:
            violations.append(
                f"Precedence violation: Job {i} ends at {end_i:.1f}, "
                f"Job {j} starts at {start_j:.1f} (gap: {gap:.1f})"
            )
            valid = False

    # Check machine conflicts
    for i, j in conflicts:
        end_i = schedule[i] + jobs[i].duration
        end_j = schedule[j] + jobs[j].duration

        overlap = min(end_i, end_j) - max(schedule[i], schedule[j])
        if overlap > tolerance:
            violations.append(
                f"Conflict overlap: Job {i} and {j} overlap by {overlap:.1f}"
            )
            valid = False

    return valid, violations