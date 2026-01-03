from navokoj import solve_qstate, generate_q_graph
import time

# --- CONFIGURATION ---
GUESTS = 50          # Nodes
TABLES = 5           # Colors/States
DENSITY = 0.25       # 25% of guests hate each other (High conflict!)
STEPS = 5000         # Give the physics engine time to cool down
SEED = 666           # The seed of chaos

print(f"--- The Wedding Seating Plan From Hell ---")
print(f"Guests: {GUESTS} | Tables: {TABLES} | Hatred Density: {DENSITY}")

# 1. Generate the 'Hatred' Graph
# If an edge exists between u and v, they cannot sit at the same table.
constraints = generate_q_graph(GUESTS, density=DENSITY, seed=SEED)
print(f"Total Feuds (Constraints): {len(constraints)}")
print("----------------------------------------")

# 2. Run the Physics Engine
print(" heating up social dynamics...")
start_time = time.time()

# This is where the magic happens. 
# It tries to minimize energy (fights) in 5-dimensional space.
seating_plan = solve_qstate(GUESTS, TABLES, constraints, steps=STEPS)

end_time = time.time()
print(f" cooled down in {end_time - start_time:.4f} seconds.")

# 3. Analyze the Damage
conflicts = 0
for u, v in constraints:
    # Check if enemies ended up at the same table
    # Note: Navokoj usually returns 1-based or 0-based depending on internal logic,
    # but the list 'seating_plan' is accessed 0-indexed.
    # The tutorial implies constraints are 1-based indices.
    table_u = seating_plan[u-1]
    table_v = seating_plan[v-1]
    
    if table_u == table_v:
        conflicts += 1

total_edges = len(constraints)
success_rate = 100 * (1 - conflicts / total_edges)

print("\n--- VERDICT ---")
print(f"Total Fights Break Out: {conflicts}")
print(f"Peaceful Interactions:  {total_edges - conflicts}")
print(f"Social Harmony Score:   {success_rate:.2f}%")

if success_rate > 90:
    print("RESULT: MAGIC. The prime weights successfully navigated the chaos.")
elif success_rate > 80:
    print("RESULT: IMPRESSIVE. A few arguments, but the wedding goes on.")
else:
    print("RESULT: DISASTER. The physics engine failed.")
