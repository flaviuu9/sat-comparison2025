import os
import time
from parser import parse
from resolution import resolution_solver
from dp import dp_sat
from dpll import dpll
from cdcl import cdcl_solver

benchmark_dirs = {
    "SAT": "benchmarks/uf20-91",
    "UNSAT": "benchmarks/uuf50-218"
}

output_file = "results.txt"

def safe_run(func, *args):
    try:
        start = time.time()
        result = func(*args)
        elapsed = (time.time() - start) * 1000
        return result, elapsed
    except Exception as e:
        return f"error ({e})", 0.0

def log_result(name, result, elapsed, out):
    status = "SAT" if result is True else "UNSAT" if result is False else result
    print(f"   {name:<9}: {status:<10} | Time: {elapsed:.4f} ms")
    out.write(f"{name}: {status}, Time: {elapsed:.4f} ms\n")

def run_solver_on_file(filepath, label, filename, out):
    print(f"Processing {label} file: {filename}")
    clauses = parse(filepath)
    print(f"   → Parsed {len(clauses)} clauses.")

    if not clauses:
        print(f"Skipping {filename}, no clauses found.")
        out.write(f"{label} | File: {filename}\nSKIPPED: No clauses found.\n\n")
        return

    variables = list({abs(lit) for clause in clauses for lit in clause})
    out.write(f"{label} | File: {filename}\n")

    if len(clauses) <= 40:
        result, elapsed = safe_run(resolution_solver, [cl.copy() for cl in clauses])
    else:
        result, elapsed = "timeout (too many clauses)", 0.0
    log_result("Resolution", result, elapsed, out)

    result, elapsed = safe_run(dp_sat, [cl.copy() for cl in clauses])
    log_result("DP", result, elapsed, out)

    result, elapsed = safe_run(dpll, [cl.copy() for cl in clauses])
    log_result("DPLL", result, elapsed, out)

    result, elapsed = safe_run(cdcl_solver, [cl.copy() for cl in clauses])
    log_result("CDCL", result, elapsed, out)

    out.write("\n")

with open(output_file, "w") as out:
    for label, folder in benchmark_dirs.items():
        print(f"Checking folder: {folder}")
        if not os.path.exists(folder):
            print(f"Folder not found: {folder}")
            continue

        cnf_files = [f for f in os.listdir(folder) if f.endswith(".cnf")]
        if not cnf_files:
            print(f"No .cnf files found in {folder}")
            continue

        for filename in cnf_files:
            filepath = os.path.join(folder, filename)
            run_solver_on_file(filepath, label, filename, out)

    # Custom manual tests
    print("\nRunning additional test cases...")

    custom_tests = [
        {
            "label": "Manual SAT",
            "clauses": [
                [1, -2, -3],
                [-1, -2, -3],
                [2, 3],
                [3, 4],
                [3, -4]
            ]
        },
        {
            "label": "Manual UNSAT",
            "clauses": [
                [1, 2],
                [1, -3],
                [-1, 3],
                [-1, -2],
                [3, -2],
                [-3, 2]
            ]
        }
    ]

    for test in custom_tests:
        print(f"\nTesting {test['label']}")
        out.write(f"\n{test['label']}\n")
        clauses = test["clauses"]
        print(f"   → Manual test with {len(clauses)} clauses.")
        out.write(f"Parsed {len(clauses)} clauses.\n")

        result, elapsed = safe_run(resolution_solver, [cl.copy() for cl in clauses])
        log_result("Resolution", result, elapsed, out)

        result, elapsed = safe_run(dp_sat, [cl.copy() for cl in clauses])
        log_result("DP", result, elapsed, out)

        result, elapsed = safe_run(dpll, [cl.copy() for cl in clauses])
        log_result("DPLL", result, elapsed, out)

        result, elapsed = safe_run(cdcl_solver, [cl.copy() for cl in clauses])
        log_result("CDCL", result, elapsed, out)

        out.write("\n")

print(f"Results saved to {output_file}")