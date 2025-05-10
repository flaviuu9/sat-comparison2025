def dpll(clauses, assignment=None):
    if assignment is None:
        assignment = {}

    clauses = simplify(clauses, assignment)

    # check for empty clause (unsatisfiable)
    for clause in clauses:
        if clause == []:
            return False
    if len(clauses) == 0:
        return True

    # unit clause propagation
    unit = find_unit_clause(clauses, assignment)
    if unit is not None:
        var = abs(unit)
        if unit > 0:
            assignment[var] = True
        else:
            assignment[var] = False
        return dpll(clauses, assignment)

    # pure literal elimination
    pure = find_pure_literal(clauses, assignment)
    if pure is not None:
        var = abs(pure)
        if pure > 0:
            assignment[var] = True
        else:
            assignment[var] = False
        return dpll(clauses, assignment)

    # choose variable and try both values
    var = choose_variable(clauses, assignment)
    for value in [True, False]:
        new_assignment = {}
        for k in assignment:
            new_assignment[k] = assignment[k]
        new_assignment[var] = value
        if dpll(clauses, new_assignment):
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
                else:
                    continue
            else:
                new_clause.append(lit)
        if not satisfied:
            simplified.append(new_clause)
    return simplified

def find_unit_clause(clauses, assignment):
    for clause in clauses:
        unassigned = []
        for lit in clause:
            if abs(lit) not in assignment:
                unassigned.append(lit)
        if len(unassigned) == 1:
            return unassigned[0]
    return None

def find_pure_literal(clauses, assignment):
    counts = {}
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var in assignment:
                continue
            if lit not in counts:
                counts[lit] = 1
            else:
                counts[lit] += 1
    for lit in counts:
        if -lit not in counts:
            return lit
    return None

def choose_variable(clauses, assignment):
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                return var
    return None