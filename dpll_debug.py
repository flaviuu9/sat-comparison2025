def dpll(clauses, assignment=None):
    if assignment is None:
        assignment = {}

    clauses = simplify(clauses, assignment)

    if any([clause == [] for clause in clauses]):
        return False
    if not clauses:
        return True

    unit = find_unit_clause(clauses, assignment)
    if unit is not None:
        assignment[abs(unit)] = unit > 0
        return dpll(clauses, assignment)

    pure = find_pure_literal(clauses, assignment)
    if pure is not None:
        assignment[abs(pure)] = pure > 0
        return dpll(clauses, assignment)

    var = choose_variable(clauses, assignment)
    for value in [True, False]:
        assignment_copy = assignment.copy()
        assignment_copy[var] = value
        if dpll(clauses, assignment_copy):
            return True

    return False

def simplify(clauses, assignment):
    simplified = []
    for clause in clauses:
        new_clause = []
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var in assignment:
                if (lit > 0 and assignment[var]) or (lit < 0 and not assignment[var]):
                    satisfied = True
                    break
                continue
            new_clause.append(lit)
        if not satisfied:
            simplified.append(new_clause)
    return simplified

def find_unit_clause(clauses, assignment):
    for clause in clauses:
        unassigned = [lit for lit in clause if abs(lit) not in assignment]
        if len(unassigned) == 1:
            return unassigned[0]
    return None

def find_pure_literal(clauses, assignment):
    counts = {}
    for clause in clauses:
        for lit in clause:
            if abs(lit) in assignment:
                continue
            counts[lit] = counts.get(lit, 0) + 1
    for lit in counts:
        if -lit not in counts:
            return lit
    return None

def choose_variable(clauses, assignment):
    for clause in clauses:
        for lit in clause:
            if abs(lit) not in assignment:
                return abs(lit)

# Test suite
if __name__ == "__main__":
    test_cases = [
        {
            "name": "Test 1 (User, SAT)",
            "clauses": [
                [1, -2, -3],
                [-1, -2, -3],
                [2, 3],
                [3, 4],
                [3, -4]
            ]
        },
        {
            "name": "Test 2 (User, UNSAT)",
            "clauses": [
                [1, 2],
                [1, -3],
                [-1, 3],
                [-1, -2],
                [3, -2],
                [-3, 2]
            ]
        },
        {
            "name": "Test 3 (Assistant, UNSAT)",
            "clauses": [
                [1, 2],
                [-1, 3],
                [-2, -3],
                [-1, -2]
            ]
        },
        {
            "name": "Test 4 (Assistant, SAT)",
            "clauses": [
                [1, 2],
                [-1, 3],
                [-3, 4],
                [2, -4]
            ]
        },
        {
            "name": "Test 5 (Trivial UNSAT)",
            "clauses": [
                [1],
                [-1]
            ]
        }
    ]

    for test in test_cases:
        print(f"\n=== Running {test['name']} ===")
        result = dpll(test["clauses"])
        print(f"{test['name']}: {'SAT' if result else 'UNSAT'}")
