"""Generic SAT encoder: complete a strongly regular graph srg(n, k, lam, mu) from a partial adjacency.

Pairs may be fixed (0/1) or free.  Extra linear constraints  sum_j c_j * lit_j = rhs  (c_j in {+1,-1}) can be added,
where a lit may be an adjacency literal, an auxiliary boolean, or an AND of literals.
Common-neighbour counts use a bidirectional capped counter (exact for counts <= cap).
Solver: CaDiCaL 1.9.5 via python-sat.
"""
import itertools
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType

TRUE, FALSE = "T", "F"


class SRGCompletion:
    def __init__(self, n, k, lam, mu, fixed):
        """fixed: dict {(i,j): 0/1} with i<j for known pairs."""
        self.n, self.k, self.lam, self.mu = n, k, lam, mu
        self.pool = IDPool()
        self.cnf = CNF()
        self.fixed = {}
        for (i, j), v in fixed.items():
            a, b = min(i, j), max(i, j)
            self.fixed[(a, b)] = v
        self.andcache = {}

    # ---- literals -------------------------------------------------------
    def adj(self, i, j):
        if i == j:
            return FALSE
        a, b = min(i, j), max(i, j)
        if (a, b) in self.fixed:
            return TRUE if self.fixed[(a, b)] else FALSE
        return self.pool.id(("a", a, b))

    def newvar(self, name):
        return self.pool.id(name)

    def AND(self, x, y):
        if x == FALSE or y == FALSE:
            return FALSE
        if x == TRUE:
            return y
        if y == TRUE:
            return x
        key = (min(x, y), max(x, y))
        if key in self.andcache:
            return self.andcache[key]
        z = self.pool.id(("and",) + key)
        self.cnf.append([-z, x]); self.cnf.append([-z, y]); self.cnf.append([z, -x, -y])
        self.andcache[key] = z
        return z

    def NOT(self, x):
        if x == TRUE:
            return FALSE
        if x == FALSE:
            return TRUE
        return -x

    # ---- cardinality ------------------------------------------------------
    def card_eq(self, lits, rhs):
        """sum of lits (may contain TRUE/FALSE) == rhs."""
        lits2 = []
        for l in lits:
            if l == TRUE:
                rhs -= 1
            elif l != FALSE:
                lits2.append(l)
        if rhs < 0 or rhs > len(lits2):
            self.falsum()
            return
        if rhs == 0:
            for l in lits2:
                self.cnf.append([-l])
            return
        if rhs == len(lits2):
            for l in lits2:
                self.cnf.append([l])
            return
        enc = CardEnc.equals(lits=lits2, bound=rhs, vpool=self.pool, encoding=EncType.totalizer)
        self.cnf.extend(enc.clauses)

    def counter(self, lits, cap):
        """bidirectional counter: returns list o[1..cap] with o[j] <-> (sum >= j)  (constants allowed)."""
        base = 0
        L = []
        for l in lits:
            if l == TRUE:
                base += 1
            elif l != FALSE:
                L.append(l)
        # r[j] for current prefix, j = 0..cap ; r[0] = TRUE
        r = [TRUE] + [FALSE] * cap
        for x in L:
            nr = [TRUE]
            for j in range(1, cap + 1):
                # nr[j] <-> r[j] or (x and r[j-1])
                a = r[j]
                b = self.AND(x, r[j - 1])
                if a == TRUE or b == TRUE:
                    nr.append(TRUE); continue
                if a == FALSE and b == FALSE:
                    nr.append(FALSE); continue
                if a == FALSE:
                    nr.append(b); continue
                if b == FALSE:
                    nr.append(a); continue
                z = self.pool.id(("or", a, b))
                self.cnf.append([-z, a, b]); self.cnf.append([z, -a]); self.cnf.append([z, -b])
                nr.append(z)
            r = nr
        # shift by base: sum >= j  <->  prefix >= j - base
        out = [None]
        for j in range(1, cap + 1):
            jj = j - base
            out.append(TRUE if jj <= 0 else (r[jj] if jj <= cap else FALSE))
        return out

    def clause(self, lits):
        c = []
        for l in lits:
            if l == TRUE:
                return
            if l == FALSE:
                continue
            c.append(l)
        if not c:
            self.falsum(); return
        self.cnf.append(c)

    def falsum(self):
        z = self.pool.id(("falsum",))
        self.cnf.append([z]); self.cnf.append([-z])

    # ---- SRG axioms -------------------------------------------------------
    def add_degrees(self):
        for i in range(self.n):
            self.card_eq([self.adj(i, j) for j in range(self.n) if j != i], self.k)

    def add_common(self, pairs=None):
        lam, mu = self.lam, self.mu
        cap = max(lam, mu) + 1
        rng = pairs if pairs is not None else itertools.combinations(range(self.n), 2)
        for i, j in rng:
            prods = [self.AND(self.adj(i, w), self.adj(j, w)) for w in range(self.n) if w != i and w != j]
            o = self.counter(prods, cap)
            e = self.adj(i, j)
            # e -> sum == lam ; not e -> sum == mu
            def eq_if(cond, val):
                # cond -> (sum >= val) and not (sum >= val+1)
                if val >= 1:
                    self.clause([self.NOT(cond), o[val]])
                self.clause([self.NOT(cond), self.NOT(o[val + 1])])
            eq_if(e, lam)
            eq_if(self.NOT(e), mu)

    def add_linear(self, terms, rhs):
        """sum c*lit = rhs with c in {+1,-1}; lit may be TRUE/FALSE/int."""
        lits = []
        for c, l in terms:
            if c == 1:
                lits.append(l)
            elif c == -1:
                lits.append(self.NOT(l)); rhs += 1
            else:
                raise ValueError(c)
        self.card_eq(lits, rhs)

    def solve(self, time_limit=None, solver_name="cadical195"):
        from pysat.solvers import Solver
        import threading
        s = Solver(name=solver_name, bootstrap_with=self.cnf.clauses)
        if time_limit:
            timer = threading.Timer(time_limit, lambda: s.interrupt())
            timer.start()
            res = s.solve_limited(expect_interrupt=True)
            timer.cancel()
        else:
            res = s.solve()
        model = s.get_model() if res else None
        s.delete()
        return res, model

    def decode(self, model):
        ms = set(l for l in model if l > 0)
        A = [[0] * self.n for _ in range(self.n)]
        for i, j in itertools.combinations(range(self.n), 2):
            l = self.adj(i, j)
            v = 1 if l == TRUE else 0 if l == FALSE else (1 if l in ms else 0)
            A[i][j] = A[j][i] = v
        return A


def check_srg(A, n, k, lam, mu):
    import numpy as np
    A = np.array(A)
    A2 = A @ A
    I = np.eye(n, dtype=int); J = np.ones((n, n), dtype=int)
    return bool((A2 == k * I + lam * A + mu * (J - I - A)).all() and (A.sum(1) == k).all() and (A == A.T).all()
                and (np.diag(A) == 0).all())
