from navokoj import solve_sat, generate_3sat, solve_qstate
import time
import math

print("=== NAVOKOJ STRESS TEST SUITE ===\n")

# --- TEST 1: THE CRITICAL DENSITY (3-SAT) ---
print("TEST 1: The Logic Crunch (3-SAT @ Critical Density)")
print("---------------------------------------------------")
N_VARS = 100
CLAUSE_RATIO = 4.26
N_CLAUSES = int(N_VARS * CLAUSE_RATIO)

print(f"Generating random 3-CNF: {N_VARS} variables, {N_CLAUSES} clauses")
print("This is the mathematical 'Phase Transition' - the hardest region for solvers.")

# Generate hard 3-SAT
clauses = generate_3sat(n_vars=N_VARS, alpha=CLAUSE_RATIO, seed=1337)

start = time.time()
# Run the solver
# solve_sat returns float probabilities, we round them to get 0/1
solution_continuous = solve_sat(N_VARS, clauses, steps=3000)
solution_discrete = [int(x > 0.5) for x in solution_continuous]
end = time.time()

# Verify
satisfied = 0
for c in clauses:
    # c is tuple like (1, -5, 3). Positive means Var 1, Negative means NOT Var 5.
    # Vars are 1-indexed in clauses, 0-indexed in solution list
    val1 = solution_discrete[abs(c[0])-1] if c[0] > 0 else 1 - solution_discrete[abs(c[0])-1]
    val2 = solution_discrete[abs(c[1])-1] if c[1] > 0 else 1 - solution_discrete[abs(c[1])-1]
    val3 = solution_discrete[abs(c[2])-1] if c[2] > 0 else 1 - solution_discrete[abs(c[2])-1]
    
    if val1 or val2 or val3:
        satisfied += 1

score = (satisfied / N_CLAUSES) * 100
print(f"Time: {end - start:.4f}s")
print(f"Satisfied: {satisfied}/{N_CLAUSES} ({score:.2f}%)")

if score > 99.0:
    print("VERDICT: PASSED. It eats critical phase transitions for breakfast.")
elif score > 95.0:
    print("VERDICT: SOLID. Standard industrial performance.")
else:
    print("VERDICT: FAILED. The phase transition crushed it.")


print("\n")

# --- TEST 2: THE CRYSTAL LATTICE (2D GRID) ---
print("TEST 2: The Crystal Lattice (400-Node Grid Optimization)")
print("-------------------------------------------------------")
# We want to see if it can form a perfect checkerboard (2-coloring)
# on a 20x20 grid without getting stuck in "grain boundaries".

GRID_SIZE = 20
N_NODES = GRID_SIZE * GRID_SIZE
N_STATES = 2 # Binary states (Black/White)

print(f"Constructing {GRID_SIZE}x{GRID_SIZE} Lattice ({N_NODES} vars)...")
constraints = []

# Build grid edges (Right and Down connections)
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        u = r * GRID_SIZE + c + 1 # 1-based index
        
        # Connect to Right
        if c < GRID_SIZE - 1:
            v = r * GRID_SIZE + (c + 1) + 1
            constraints.append((u, v))
        
        # Connect to Down
        if r < GRID_SIZE - 1:
            v = (r + 1) * GRID_SIZE + c + 1
            constraints.append((u, v))

print(f"Physics Constraints: {len(constraints)} edges")
print("Cooling the crystal...")

start = time.time()
# Use q-state solver for graph coloring
lattice_state = solve_qstate(N_NODES, N_STATES, constraints, steps=4000)
end = time.time()

# Verify Crystal Structure
defects = 0
for u, v in constraints:
    if lattice_state[u-1] == lattice_state[v-1]:
        defects += 1

integrity = 100 * (1 - defects / len(constraints))
print(f"Time: {end - start:.4f}s")
print(f"Crystal Defects: {defects}")
print(f"Lattice Integrity: {integrity:.2f}%")

if defects == 0:
    print("VERDICT: PERFECT CRYSTAL. Pure adiabatic cooling achieved.")
elif defects < 5:
    print("VERDICT: MICRO-FRACTURES. Nearly perfect, minor domain walls.")
else:
    print("VERDICT: AMORPHOUS BLOB. It failed to crystallize.")
