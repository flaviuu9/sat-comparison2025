def parse(file_path):
    #Parses a CNF file and returns a list of clauses. Each clause is a list of integers representing literals.
    clauses = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(('c', 'p', '%')):
                continue
            try:
                literals = list(map(int, line.split()))
                if literals and literals[-1] == 0:
                    clauses.append(literals[:-1])
            except ValueError:
                continue
    return clauses

