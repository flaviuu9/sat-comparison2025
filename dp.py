def dp_sat(clauses):
    for i in range(len(clauses)):
        new_clause = []
        for x in clauses[i]:
            if x not in new_clause:
                new_clause.append(x)
        clauses[i] = new_clause

    while True:
        # unit propagation
        unit = []
        for c in clauses:
            if len(c) == 1 and c[0] not in unit:
                unit.append(c[0])

        if unit != []:
            for l in unit:
                new_clauses = []
                for c in clauses:
                    if l in c:
                        continue
                    if -l in c:
                        new_c = []
                        for x in c:
                            if x != -l:
                                new_c.append(x)
                        new_clauses.append(new_c)
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            continue

        # clauses containing a literal and its negation (tautologies)
        new_clauses = []
        for c in clauses:
            ok = False
            for x in c:
                if -x in c:
                    ok = True
            if not ok:
                new_clauses.append(c)
        clauses = new_clauses

        # pure literal elimination
        lits = []
        for c in clauses:
            for x in c:
                if x not in lits:
                    lits.append(x)

        pure = []
        for x in lits:
            if -x not in lits:
                pure.append(x)

        if pure != []:
            new_clauses = []
            for c in clauses:
                skip = False
                for x in pure:
                    if x in c:
                        skip = True
                if not skip:
                    new_clauses.append(c)
            clauses = new_clauses
            continue

        for c in clauses:
            if c == []:
                return False
        if clauses == []:
            return True

        # choosing the literal
        chosen = None
        for c in clauses:
            for x in c:
                if -x in lits:
                    chosen = abs(x)
                    break
            if chosen is not None:
                break

        if chosen is None:
            return True

        pos = []
        neg = []
        for c in clauses:
            if chosen in c:
                pos.append(c)
            elif -chosen in c:
                neg.append(c)

        res = []
        for a in pos:
            for b in neg:
                nou = []
                for x in a:
                    if x != chosen and x != -chosen and x not in nou:
                        nou.append(x)
                for x in b:
                    if x != chosen and x != -chosen and x not in nou:
                        nou.append(x)
                if nou == []:
                    return False
                if nou not in res:
                    res.append(nou)

        new_clauses = []
        for c in clauses:
            if chosen not in c and -chosen not in c:
                new_clauses.append(c)
        for r in res:
            new_clauses.append(r)
        clauses = new_clauses

