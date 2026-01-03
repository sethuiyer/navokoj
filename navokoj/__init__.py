"""
Navokoj: The Arithmetic Manifold Framework for Constraint Satisfaction.

This package implements the Arithmetic Manifold theory for NP-hard constraint
satisfaction problems (SAT, scheduling, graph coloring) using geometric operators
and adiabatic flows instead of combinatorial search.

Author: Sethu Iyer <sethuiyer95@gmail.com>
Version: 0.1.0
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Sethu Iyer"
__email__ = "sethuiyer95@gmail.com"
__license__ = "MIT"

from .sat_solver import solve_sat, generate_3sat, encode_n_queens, encode_sudoku
from .scheduler import schedule_jobs, JobConfig
from .qstate_solver import solve_qstate, generate_q_graph

__all__ = [
    "solve_sat",
    "generate_3sat", 
    "encode_n_queens",
    "encode_sudoku",
    "schedule_jobs",
    "JobConfig",
    "solve_qstate",
    "generate_q_graph",
]