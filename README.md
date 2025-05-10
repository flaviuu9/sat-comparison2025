# SAT Comparison 2025

This repository contains a comparative implementation of four classical SAT (Boolean Satisfiability) solving algorithms:

- Resolution
- Davis–Putnam (DP)
- Davis–Putnam–Logemann–Loveland (DPLL)
- Conflict-Driven Clause Learning (CDCL)

The purpose is educational — to understand and evaluate the theoretical and practical behavior of each solver across different SAT problem instances.

## 📂 Project Structure
sat-comparison2025/
├── benchmarks/              # SATLIB benchmark files (CNF)
│   ├── uf20-91/             # Satisfiable formulas
│   └── uuf50-218/           # Unsatisfiable formulas
├── cdcl.py                  # CDCL solver (basic clause learning + backjumping)
├── dp.py                    # Davis–Putnam solver
├── dpll.py                  # DPLL solver
├── resolution.py            # Resolution-based solver
├── parser.py                # DIMACS CNF parser
├── run_all.py               # Script that runs all solvers on all benchmarks
├── results.txt              # Output results (runtime, SAT/UNSAT, etc.)
└── README.md
