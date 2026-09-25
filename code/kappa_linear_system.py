"""notes/104: given the non-isometric edge set nu of a Hamming point configuration, the orientation bits
x(P->R) = [kappa(P->R) = min R] satisfy a LINEAR system over F_2:
  (Z_A)  for each pair P and class m outside P:  sum_{R in G_P, m in R} [kappa(P->R) = m] = 0;
  (i)    for each triangle {P, P'', R} with PP'' isometric and PR, P''R not: x(P->R) = x(P''->R);
  (C')   for each triple (i; j, k), P = ij, P' = ik, pages R in F = [7]-{i,j,k}:
         #(0,0) pages + #{(1,1) pages with kappa(P->R) = kappa(P'->R)} = 0.
Gaussian elimination decides consistency (no search)."""
import itertools

pairs = list(itertools.combinations(range(7), 2))
def disjoint(a, b): return not set(a) & set(b)
kedges = [frozenset((P, R)) for P, R in itertools.combinations(pairs, 2) if disjoint(P, R)]
triangles = [t for t in itertools.combinations(pairs, 3) if all(disjoint(a, b) for a, b in itertools.combinations(t, 2))]

def system(nu):
    """nu: set of frozenset({P,R}) non-isometric edges.  returns list of (var-set, const)"""
    var = {}
    def x(P, R):
        key = (P, R)
        if key not in var:
            var[key] = len(var)
        return var[key]
    eqs = []
    for P in pairs:
        G = [R for R in pairs if disjoint(P, R) and frozenset((P, R)) in nu]
        for m in range(7):
            if m in P:
                continue
            vs, c = set(), 0
            for R in G:
                if m in R:
                    vs ^= {x(P, R)}
                    c ^= int(m == max(R))
            eqs.append((vs, c))
    for t in triangles:
        for R in t:
            P, P2 = [Q for Q in t if Q != R]
            if frozenset((P, P2)) not in nu and frozenset((P, R)) in nu and frozenset((P2, R)) in nu:
                eqs.append(({x(P, R)} ^ {x(P2, R)}, 0))
    for i in range(7):
        for j, k in itertools.combinations([c for c in range(7) if c != i], 2):
            P, P2 = tuple(sorted((i, j))), tuple(sorted((i, k)))
            F = [c for c in range(7) if c not in (i, j, k)]
            vs, c = set(), 0
            for R in itertools.combinations(F, 2):
                a = frozenset((P, R)) in nu
                b = frozenset((P2, R)) in nu
                if not a and not b:
                    c ^= 1
                elif a and b:
                    c ^= 1
                    vs ^= {x(P, R)}
                    vs ^= {x(P2, R)}
            eqs.append((vs, c))
    return eqs, var

def consistent(eqs):
    rows = []
    for vs, c in eqs:
        r = 0
        for v in vs:
            r |= 1 << (v + 1)
        rows.append(r | c)
    basis = {}
    for r in rows:
        while r >> 1:
            top = r.bit_length() - 1
            if top in basis:
                r ^= basis[top]
            else:
                basis[top] = r
                break
        else:
            if r & 1:
                return False, len(basis)
    return True, len(basis)

def check(name, nu):
    eqs, var = system(nu)
    ok, rk = consistent(eqs)
    print('%-40s |nu| = %3d, unknowns %3d, equations %3d, rank %3d : %s' %
          (name, len(nu), len(var), len(eqs), rk, 'CONSISTENT' if ok else 'inconsistent'))
    return ok

if __name__ == '__main__':
    check('case II (all non-isometric)', set(kedges))
    D, E = (0, 1), (2, 3, 4, 5, 6)
    V0 = {P for P in pairs if len(set(P) & set(D)) == 1}
    check('cut D x E', {e for e in kedges if len([Q for Q in e if Q in V0]) == 1})
    # near-1-factorisations of K7: cyclic one  T_v = {{v+d, v-d} : d = 1,2,3}
    T = [[tuple(sorted(((v + d) % 7, (v - d) % 7))) for d in (1, 2, 3)] for v in range(7)]
    iso = {frozenset(e) for tv in T for e in itertools.combinations(tv, 2)}
    check('triangle factor (cyclic near-1-factorisation)', set(kedges) - iso)
