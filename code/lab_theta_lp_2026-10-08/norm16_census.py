"""C1, lab session, 2026-10-08. Caps on the short vectors of L1 from the census of special supports.

  python norm16_census.py <census2 order-10 json> <codex_norm16_cores.json>

Supports: a Fano vector is the incidence graph of the biplane 2-(7,4,2) (7 + 7, 4-regular, induced); a norm-16 vector
has one of Codex's five cores (note 166: 8 + 8 independent sets, 4-regular bipartite, incidence matrices read from its
data file as data). An induced subgraph S of such a support with minimum degree >= 3 is a special support, i.e. a
parameter of the census. If S contains a vertex with all four of its neighbours (a full seed), a copy of S lies in at
most one Fano or norm-16 vector (one vector per seed, Codex note 173). Hence for every such S:
      sum over supports c of (number of vectors with support c / 2) * mult_c(S)  <=  N(S),
mult_c(S) = number of induced copies of S in the support c that contain a full seed.
The script lists S and the multiplicities, then maximises over the order-10 polytope (floating point HiGHS,
exploration; an exact certificate is needed before use): a_7 alone, a_8 alone per core, and 7 a_7 + 8 a_8."""
import sys, json, time, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import census2 as C2
pc = lambda x: bin(x).count("1")
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
fano = [[0 if i in L else 1 for L in LINES] for i in range(7)]
cores = {"Fano": fano}
for case in json.load(open(sys.argv[2]))["cases"]:
    for rep in case["representatives"]: cores["norm16 " + "+".join(str(x) for x in case["defect_cycle_lengths"])] = rep
t0 = time.time(); D = json.load(open(sys.argv[1])); npar = len(D["params"]); pid = {(n, key): i for i, (n, key, rows) in enumerate(D["params"])}
mult = {}                                                                # (order, key) -> {core: multiplicity with a full seed}
for nm, Bm in cores.items():
    a = len(Bm); n = 2 * a; adj = [0] * n
    for i in range(a):
        for j in range(a):
            if Bm[i][j]: adj[i] |= 1 << (a + j); adj[a + j] |= 1 << i
    assert all(pc(x) == 4 for x in adj), nm
    for size in range(6, 11):
        for S in itertools.combinations(range(n), size):
            sm = sum(1 << v for v in S)
            if any(pc(adj[v] & sm) < 3 for v in S): continue
            if not any(pc(adj[v] & sm) == 4 for v in S): continue          # needs a full seed
            pos = {v: p for p, v in enumerate(S)}; rows = [0] * size
            for v in S:
                for u in S:
                    if adj[v] >> u & 1: rows[pos[v]] |= 1 << pos[u]
            key, _ = C2.canon(size, rows); mult.setdefault((size, key), {}); mult[(size, key)][nm] = mult[(size, key)].get(nm, 0) + 1
print("special sub-supports with a full seed (order, parameter, edges): multiplicities per support")
for (size, key), m in sorted(mult.items()):
    rows = D["params"][pid[(size, key)]][2]; print("   order %d, parameter %3d, %d edges: %s" % (size, pid[(size, key)], sum(pc(x) for x in rows) // 2, m))
ri = []; ci = []; va = []; const = []; r = 0; seen = set()
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in D["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue
        seen.add(sig); f = {int(p): float(Fr(v_)) for p, v_ in form.items()}; sc = max(abs(x) for x in f.values())
        const.append(f.get(0, 0.0) / sc)
        for p, v_ in f.items():
            if p: ri.append(r); ci.append(p - 1); va.append(v_ / sc)
        r += 1
names = list(cores); nc = len(names)                                     # extra variables: number of configurations (vectors / 2) per support
rows_x = []; cols_x = []; vals_x = []; rr = r
for (size, key), m in mult.items():                                      # N(S) - sum mult * n_c >= 0
    rows_x.append(rr); cols_x.append(pid[(size, key)]); vals_x.append(1.0)
    for nm, k_ in m.items(): rows_x.append(rr); cols_x.append(npar + names.index(nm)); vals_x.append(-float(k_))
    const.append(0.0); rr += 1
A = csr_matrix((va + vals_x, (ri + rows_x, ci + cols_x)), shape=(rr, npar + nc)); const = np.array(const)
def mx(c, label):
    res = linprog(-c, A_ub=-A, b_ub=const, bounds=[(0, None)] * (npar + nc), method="highs-ipm")
    print("   max %-40s = %s  [%.0f s]" % (label, "%.8g" % (-res.fun) if res.status == 0 else res.message[:50], time.time() - t0), flush=True)
c = np.zeros(npar + nc); c[npar] = 2.0; mx(c, "a_7")
for i in range(1, nc):
    c = np.zeros(npar + nc); c[npar + i] = 2.0; mx(c, "a_8 with core " + names[i][7:])
c = np.zeros(npar + nc); c[npar + 1:] = 2.0; mx(c, "a_8 (all cores)")
c = np.zeros(npar + nc); c[npar] = 14.0; c[npar + 1:] = 16.0; mx(c, "7 a_7 + 8 a_8")
