"""Hidden 3-eigenvectors of A_Omega on positive E3-free c(l) = 1 blocks: quotient of E_3(A_Omega) by
span(psi_0..psi_3, m-component vectors), LLL-reduced representatives, supports by column (outer lines j = 2..6)
and by part (core, Q_0j, Q_1j, letters).  Columns: P_j = {2j, 2j+1} u Q_0j u Q_1j."""
import itertools, json, sys, math
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, relabel, build_H, gl_connected, rank_mod
from c1_hidden import comps_m
from c1_e3free_floor import e3_free
from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix

def name(x):
    if isinstance(x, tuple):
        return str(x[1])
    return "".join("0123456789abcd"[t] for t in sorted(x))

def col_of(x):
    if isinstance(x, tuple):
        if x[0] == "P":
            return "core"
        a = x[1]
        return "core" if a in (2, 3) else "c%d" % (a // 2)
    a, b = sorted(x)
    if b <= 3:
        return "core"
    return "c%d" % (b // 2)

want = int(sys.argv[2]); done = 0
for line in open(sys.argv[1]):
    d = json.loads(line)
    if len(d["labels"]) != 44:
        continue
    S0 = [frozenset(x) for x in d["labels"]]
    E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
    for side in (0, 1):
        L, EE = relabel(S0, E0, side)
        conn, degok = gl_connected(EE)
        if not (conn and degok) or not e3_free(EE):
            continue
        G = np.zeros((44, 44))
        for i, j in itertools.combinations(range(44), 2):
            if frozenset((S[i], S[j])) in EE:
                G[i, j] = G[j, i] = 1
        K8 = np.array([[k8(a, b) for b in S] for a in S], float)
        if np.linalg.eigvalsh((24 * np.eye(44) - 8 * G - K8) / 8)[0] < -1e-9:
            continue
        V, A = build_H(EE, with_l=True)
        n = len(V); pos = {x: i for i, x in enumerate(V)}
        ns = Matrix((A - 3 * np.eye(n, dtype=np.int64)).tolist()).nullspace()
        rows = []
        for v in ns:
            den = 1
            for t in v:
                den = den * t.q // math.gcd(den, t.q)
            rows.append([int(t * den) for t in v])
        # known: psi_r = 1_star(r) - 1_{N(v) minus line(r)} + 3 e_r - 3 e_v
        known = []
        for r in range(4):
            vv = [0] * n
            for w in XL + Y:
                if r in w:
                    vv[pos[w]] += 1
            line_r = (0, 1) if r < 2 else (2, 3)
            for a in [0, 1] + list(range(2, 14)):
                if a in line_r:
                    continue
                key = ("P", a) if a in (0, 1) else ("L", a)
                vv[pos[key]] -= 1
            vv[pos[("P", r)] if r < 2 else pos[("L", r)]] += 3
            vv[pos[("P", "v")]] -= 3
            known.append(vv)
        cm, _ = comps_m(EE)
        # quotient: project rows onto the orthogonal complement of span(known) within span(rows), then LLL
        Kn = np.array(known, float).T
        R = np.array(rows, float).T
        Qk, _ = np.linalg.qr(Kn)
        Rres = R - Qk @ (Qk.T @ R)
        u, s_, wt = np.linalg.svd(Rres, full_matrices=False)
        hid_dim = int(np.sum(s_ > 1e-8))
        dm = DomainMatrix([[ZZ(x) for x in r] for r in rows], (len(rows), n), ZZ)
        red = dm.lll().to_Matrix().tolist()
        print("== %s side %d: c(m) = %d, dim E = %d, beyond psi's = %d (m-comps %d, hidden %d)" % (
            d.get("src", "?")[:28], side, cm, len(rows), hid_dim, cm - 1, hid_dim - (cm - 1)))
        for r in red:
            nz = [i for i in range(n) if r[i]]
            cols = {}
            for i in nz:
                c = col_of(V[i]); cols[c] = cols.get(c, 0) + 1
            inpsi = np.linalg.norm(np.array(r, float) - Qk @ (Qk.T @ np.array(r, float))) < 1e-8
            print("   norm %5d %s |supp| %2d  by column %s" % (sum(int(x) ** 2 for x in r), "(in psi span)" if inpsi else "             ", len(nz), dict(sorted(cols.items()))))
        done += 1
        if done >= want:
            sys.exit(0)
