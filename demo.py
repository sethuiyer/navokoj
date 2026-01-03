"""
Demonstration Script: Professional Usage of Navokoj Framework.

This script demonstrates proper usage of the Navokoj constraint satisfaction
framework across multiple problem classes: SAT, scheduling, and Q-state systems.

Author: Sethu Iyer <sethuiyer95@gmail.com>
License: MIT
"""

from navokoj import (
    solve_sat,
    generate_3sat,
    encode_n_queens,
    encode_sudoku,
    schedule_jobs,
    JobConfig,
    solve_qstate,
    generate_q_graph,
)

from navokoj.benchmark import run_full_benchmark


def demo_sat():
    """Demonstrate SAT solving capabilities."""
    print("\n" + "=" * 70)
    print("DEMO: SAT SOLVING")
    print("=" * 70)

    # Example 1: Simple 3-SAT
    print("\n1. Simple 3-Clause Problem:")
    clauses = [[1, 2, 3], [-1, 4], [-2, -3, -4]]
    solution = solve_sat(4, clauses, steps=1000, seed=42)
    print(f"Clauses: {clauses}")
    print(f"Solution: {solution}")

    # Verify
    satisfied = sum(
        1
        for clause in clauses
        if any(
            (lit > 0 and solution[abs(lit) - 1] == 1)
            or (lit < 0 and solution[abs(lit) - 1] == 0)
            for lit in clause
        )
    )
    print(f"Clauses satisfied: {satisfied}/{len(clauses)}")

    # Example 2: Critical 3-SAT (hard instance)
    print("\n2. Critical 3-SAT (50 variables):")
    clauses = generate_3sat(50, alpha=4.26, seed=42)
    solution = solve_sat(50, clauses, steps=2000, seed=42)
    
    satisfied = sum(
        1
        for clause in clauses
        if any(
            (lit > 0 and solution[abs(lit) - 1] == 1)
            or (lit < 0 and solution[abs(lit) - 1] == 0)
            for lit in clause
        )
    )
    print(f"Variables: 50, Clauses: {len(clauses)}")
    print(f"Clauses satisfied: {satisfied}/{len(clauses)} ({satisfied/len(clauses):.1%})")


def demo_queens():
    """Demonstrate N-Queens solving."""
    print("\n" + "=" * 70)
    print("DEMO: N-QUEENS")
    print("=" * 70)

    n_vars, clauses = encode_n_queens(8)
    solution = solve_sat(n_vars, clauses, steps=2000, seed=42)

    print("\n8×8 Chessboard:")
    valid_queens = 0
    for r in range(8):
        row = ""
        for c in range(8):
            val = solution[r * 8 + c]
            if val == 1:
                row += " Q "
                valid_queens += 1
            else:
                row += " . "
        print(row)

    print(f"\nQueens placed: {valid_queens}")
    print("Solution valid:", valid_queens == 8)


def demo_sudoku():
    """Demonstrate Sudoku solving."""
    print("\n" + "=" * 70)
    print("DEMO: SUDOKU (Arto Inkala's AI Escargot)")
    print("=" * 70)

    hardest_sudoku = """
    8 . . . . . . . .
    . . 3 6 . . . . .
    . 7 . . 9 . 2 . .
    . 5 . . . 7 . . .
    . . . . 4 5 7 . .
    . . . 1 . . . 3 .
    . . 1 . . . . 6 8
    . . 8 5 . . . 1 .
    . 9 . . . . 4 . .
    """

    n_vars, clauses = encode_sudoku(hardest_sudoku)
    print(f"Problem: {n_vars} variables, {len(clauses)} clauses")

    solution = solve_sat(n_vars, clauses, steps=5000, seed=42)
    grid = []
    for r in range(9):
        row = ""
        for c in range(9):
            for v in range(9):
                idx = (r * 9 + c) * 9 + v
                if solution[idx] == 1:
                    row += str(v + 1) + " "
                    break
        grid.append(row)

    print("\nSolution:")
    for row in grid:
        print(row)

    filled = sum(c != "." for row in grid for c in row.split())
    print(f"\nCells filled: {filled}/81")
    print("Valid solution:", filled == 81)


def demo_scheduling():
    """Demonstrate job scheduling."""
    print("\n" + "=" * 70)
    print("DEMO: JOB SCHEDULING")
    print("=" * 70)

    jobs = {
        0: JobConfig(duration=4.0, name="Milling"),
        1: JobConfig(duration=3.0, name="Polishing"),
        2: JobConfig(duration=5.0, name="Assembly"),
        3: JobConfig(duration=2.0, name="QC"),
        4: JobConfig(duration=4.0, name="Packaging"),
    }

    # Pipeline: milling -> polishing -> assembly
    precedences = [(0, 1), (1, 2)]

    # Machine conflicts
    conflicts = [
        (0, 3),  # Milling and QC share inspection station
        (1, 4),  # Polishing and packaging share workspace
        (2, 3),  # Assembly and QC share tools
    ]

    schedule = schedule_jobs(jobs, conflicts, precedences, horizon=100, seed=42)

    from navokoj.scheduler import verify_schedule

    valid, violations = verify_schedule(jobs, schedule, conflicts, precedences)

    print("\nSchedule:")
    print(f"{'Job':>4} {'Start':>8} {'End':>8} {'Duration':>10}")
    print("-" * 40)
    for job_id, start in schedule.items():
        end = start + jobs[job_id].duration
        print(
            f"{job_id:4d} {start:8.1f} {end:8.1f} " f"{jobs[job_id].duration:10.1f}"
        )

    print(f"\nSchedule valid: {valid}")
    if violations:
        for v in violations:
            print(f"  ❌ {v}")
    else:
        print("  ✅ All constraints satisfied")


def demo_qstate():
    """Demonstrate Q-state graph coloring."""
    print("\n" + "=" * 70)
    print("DEMO: GRAPH COLORING (Q-STATE)")
    print("=" * 70)

    # Generate random graph
    n_nodes = 30
    constraints = generate_q_graph(n_nodes, density=0.3, seed=42)
    print(f"Graph: {n_nodes} nodes, {len(constraints)} edges")

    # Color with 7 colors
    n_colors = 7
    assignment = solve_qstate(n_nodes, n_colors, constraints, steps=2000, seed=42)

    # Verify
    conflicts = 0
    for u, v in constraints:
        if assignment[u - 1] == assignment[v - 1]:
            conflicts += 1

    print(f"Colors used: {len(set(assignment))}")
    print(f"Conflicts: {conflicts}/{len(constraints)}")
    print(
        f"Success rate: {(1 - conflicts/len(constraints)):.1%}"
    )


def demo_comprehensive():
    """Run comprehensive demonstration of all capabilities."""
    print("\n" + "=" * 70)
    print("NAVOKOJ COMPREHENSIVE DEMO")
    print("Author: Sethu Iyer <sethuiyer95@gmail.com>")
    print("=" * 70)

    demo_sat()
    demo_queens()
    demo_sudoku()
    demo_scheduling()
    demo_qstate()

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--benchmark":
        run_full_benchmark()
    else:
        demo_comprehensive()