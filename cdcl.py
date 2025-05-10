def unit_propagate(clauses, assignment):
    while True:
        changed = False
        for clause in clauses:
            unassigned = []
            has_true = False

            for lit in clause:
                var = abs(lit)
                if var in assignment:
                    if (lit > 0 and assignment[var]) or (lit < 0 and not assignment[var]):
                        has_true = True
                        break
                else:
                    unassigned.append(lit)

            if has_true:
                continue
            if len(unassigned) == 0:
                return "conflict", clause  # clause is false
            if len(unassigned) == 1:
                lit = unassigned[0]
                var = abs(lit)
                val = lit > 0
                if var in assignment:
                    if assignment[var] != val:
                        return "conflict", clause
                else:
                    assignment[var] = val
                    changed = True

        if not changed:
            break

    return "ok", None

def is_all_assigned(clauses, assignment):
    # collect all variables from the clauses
    vars_in_formula = []
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in vars_in_formula:
                vars_in_formula.append(var)

    for var in vars_in_formula:
        if var not in assignment:
            return False

    return True

def choose_literal(clauses, assignment):
    # pick the first unassigned literal
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                return lit
    return None

def analyze_conflict(conflict_clause):
    # return the clause itself
    return conflict_clause

def backjump(assignment, levels, level):
    # remove assignments from levels above the jump level
    to_remove = []
    for var in levels:
        if levels[var] > level:
            to_remove.append(var)

    for var in to_remove:
        del assignment[var]
        del levels[var]

def cdcl_solver(clauses):
    assignment = {}
    decision_level = 0
    levels = {}

    while True:
        result, conflict_clause = unit_propagate(clauses, assignment)
        if result == "conflict":
            if decision_level == 0:
                return "UNSAT"
            learned_clause = analyze_conflict(conflict_clause)
            clauses.append(learned_clause)
            backjump_level = 0
            backjump(assignment, levels, backjump_level)
            decision_level = backjump_level
        else:
            if is_all_assigned(clauses, assignment):
                return "SAT"
            decision_level += 1
            lit = choose_literal(clauses, assignment)
            if lit is None:
                return "SAT"
            var = abs(lit)
            val = lit > 0
            assignment[var] = val
            levels[var] = decision_level