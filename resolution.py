def resolve(ci, cj):
    common = []
    for lit in ci:
        for other in cj:
            if lit == -other:
                common.append(lit)

    if len(common) != 1:
        return None

    l = common[0]
    combined = []

    # Add literals from first clause
    for lit in ci:
        if lit != l and lit != -l:
            combined.append(lit)

    # Add literals from second clause
    for lit in cj:
        if lit != l and lit != -l and lit not in combined:
            combined.append(lit)

    return combined

def resolution_solver(clauses, max_steps=1000, max_total_clauses=10000):
    known = []
    for clause in clauses:
        clause_sorted = sorted(clause)
        if clause_sorted not in known:
            known.append(clause_sorted)

    steps = 0

    while steps < max_steps and len(known) < max_total_clauses:
        new_clauses = []
        for i in range(len(known)):
            for j in range(i + 1, len(known)):
                res = resolve(known[i], known[j])
                if res is None:
                    continue
                if res == []:
                    return False
                res_sorted = sorted(res)
                if res_sorted not in known and res_sorted not in new_clauses:
                    new_clauses.append(res_sorted)

        if len(new_clauses) == 0:
            break

        for new_clause in new_clauses:
            known.append(new_clause)

        steps = steps + 1

    if steps >= max_steps or len(known) >= max_total_clauses:
        return "timeout"
    return True

