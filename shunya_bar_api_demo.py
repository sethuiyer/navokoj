import requests
import json
import time

# --- CONFIGURATION ---
API_URL = "https://api.navokoj.shunyabar.foo/v1/solve"
# Using the Public Beta Key from the docs
API_KEY = "nvkj_CG3kWXy7A61WHQ8WwlNnuBdkur+akKsa7EKdsoYfj1c"

# --- PROBLEM GENERATION (20x20 Lattice) ---
GRID_SIZE = 20
N_VARS = GRID_SIZE * GRID_SIZE

print(f"--- GENERATING CRYSTAL LATTICE ({GRID_SIZE}x{GRID_SIZE}) ---")
clauses = []

# Logic: For every edge (u, v), they must be different colors.
# In Boolean SAT (CNF), "u != v" is represented by TWO clauses:
# 1. (u OR v)      -> At least one is True
# 2. (NOT u OR NOT v) -> At least one is False
# Result: One is True, One is False. Perfect Checkerboard.

edges_count = 0
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        u = r * GRID_SIZE + c + 1 # 1-based index
        
        # Connect Right
        if c < GRID_SIZE - 1:
            v = r * GRID_SIZE + (c + 1) + 1
            clauses.append([u, v])       # (u OR v)
            clauses.append([-u, -v])     # (!u OR !v)
            edges_count += 1
        
        # Connect Down
        if r < GRID_SIZE - 1:
            v = (r + 1) * GRID_SIZE + c + 1
            clauses.append([u, v])       # (u OR v)
            clauses.append([-u, -v])     # (!u OR !v)
            edges_count += 1

print(f"Variables: {N_VARS}")
print(f"Constraints: {len(clauses)} clauses (representing {edges_count} edges)")
print(f"Target Engine: PRO ('The Mind') - Expecting 100% accuracy")

# --- API REQUEST ---
payload = {
    "num_vars": N_VARS,
    "clauses": clauses,
    "engine": "pro",  # <--- CRITICAL: We are asking for the heavy GPU engine
    "timeout": 5000   # Give it 5 seconds
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

print("\nSending to ShunyaBar H100 Cluster...")
try:
    start = time.time()
    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
    end = time.time()
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(result)
        
        if result['success']:
            print(f"\nSUCCESS! Solved in {result['solve_time_seconds']}s")
            print(f"Satisfaction Rate: {result['satisfaction_rate'] * 100}%")
            
            # Verify the crystal locally
            assignment = result['assignment'] # List of True/False
            
            defects = 0
            # Re-verify edges manually
            # Note: The API returns assignment [True, False...]. 
            # Variable 1 is at index 0.
            
            # Re-generate edges to check
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    u = r * GRID_SIZE + c + 1
                    u_val = assignment[u-1]
                    
                    # Check Right
                    if c < GRID_SIZE - 1:
                        v = u + 1
                        v_val = assignment[v-1]
                        if u_val == v_val: defects += 1
                            
                    # Check Down
                    if r < GRID_SIZE - 1:
                        v = u + GRID_SIZE
                        v_val = assignment[v-1]
                        if u_val == v_val: defects += 1

            print(f"Local Verification Defects: {defects}")
            if defects == 0:
                print("VERDICT: The Paid API fixed the grain boundaries. It's a perfect crystal.")
            else:
                print("VERDICT: The Paid API also failed. The theory is flawed.")
                
        else:
            print("API returned failure.")
            print(result)
            
    else:
        print("Error response:")
        print(response.text)

except Exception as e:
    print(f"\nCONNECTION FAILED: {e}")
    print("NOTE: The docs say the API is 'DOWN TILL 2026'.") 
    print("If this failed, the author might have actually taken the server offline.")
