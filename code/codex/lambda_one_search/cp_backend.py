"""Small CryptoMiniSat-style adapter for direct CP-SAT cardinality models."""
from ortools.sat.python import cp_model


class CpBackend:
    def __init__(self, seed=1, workers=1):
        self.model = cp_model.CpModel()
        self.variables = [None]
        self.seed = seed
        self.workers = workers
        self.calls = 0

    def variable(self, number):
        while len(self.variables) <= abs(number):
            self.variables.append(self.model.new_bool_var(f'x{len(self.variables)}'))
        v = self.variables[abs(number)]
        return v if number > 0 else v.Not()

    def add_clause(self, clause):
        self.model.add_bool_or([self.variable(int(v)) for v in clause])

    def add_clauses(self, clauses):
        for clause in clauses:
            self.add_clause(clause)

    def add_count(self, variables, target):
        self.model.add(sum(self.variable(int(v)) for v in variables) == target)

    def add_xor_clause(self, variables, rhs):
        lits = [self.variable(int(v)) for v in variables]
        if not rhs:
            lits.append(True)
        self.model.add_bool_xor(lits)

    def solve(self, assumptions=None, time_limit=30):
        self.model.clear_assumptions()
        if assumptions:
            self.model.add_assumptions([self.variable(int(v)) for v in assumptions])
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = max(0.001, time_limit)
        solver.parameters.num_search_workers = self.workers
        solver.parameters.random_seed = self.seed + self.calls
        self.calls += 1
        status = solver.solve(self.model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return True, tuple([None] + [bool(solver.value(v)) for v in self.variables[1:]])
        if status == cp_model.INFEASIBLE:
            return False, None
        if status == cp_model.MODEL_INVALID:
            raise ValueError(self.model.validate())
        return None, None
