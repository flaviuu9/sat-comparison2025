# SAT Comparison 2025

This repository contains a comparative implementation of four classical SAT (Boolean Satisfiability) solving algorithms:

- Resolution
- Davis–Putnam (DP)
- Davis–Putnam–Logemann–Loveland (DPLL)
- Conflict-Driven Clause Learning (CDCL)

The purpose is educational — to understand and evaluate the theoretical and practical behavior of each solver across different SAT problem instances.

## 📂 Project Structure
- `cdcl.py`: CDCL solver (basic clause learning + backjumping)
- `dpll.py`: DPLL solver
- `dp.py`: Davis–Putnam solver
- `resolution.py`: Resolution-based solver
- `parser.py`: DIMACS CNF parser
- `run_all.py`: Script that runs all solvers and logs the output
- `results.txt`: Output results (runtime, SAT/UNSAT, etc.)
- `benchmarks/`: SATLIB benchmark files (CNF)



