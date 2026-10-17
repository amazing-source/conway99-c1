"""Integer basis (LLL-reduced) of E_3(A_H), H = N(l) u Y, for a few positive c(l) = c(m) = 1 sides; print supports."""
import itertools, json, sys
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, relabel, build_H, gl_connected
from c1_hidden import comps_m
from sympy import Matrix
from sympy.polys.matrices import DomainMatrix
from sympy import ZZ

def name(x):
    if isinstance(x, tuple):
        return "%s" % x[1]
    return "".join(str(t) if t < 10 else "abcd"[t - 10] for t in sorted(x))

def main():
    want = int(sys.argv[2])
    done = 0
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
        for side in (0, 1):
            L, EE = relabel(S0, E0, side)
            conn, degok = gl_connected(EE)
            if not (conn and degok):
                continue
            G = np.zeros((44, 44))
            for i, j in itertools.combinations(range(44), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            K8 = np.array([[k8(a, b) for b in S] for a in S], float)
            if np.linalg.eigvalsh((24 * np.eye(44) - 8 * G - K8) / 8)[0] < -1e-9:
                continue
            cm, _ = comps_m(EE)
            if cm != 1:
                continue
            V, A = build_H(EE)
            M = Matrix((A - 3 * np.eye(len(V), dtype=np.int64)).tolist())
            ns = M.nullspace()
            # clear denominators, LLL
            rows = []
            for v in ns:
                den = 1
                for t in v:
                    den = den * t.q // __import__("math").gcd(den, t.q)
                rows.append([int(t * den) for t in v])
            dm = DomainMatrix([[ZZ(x) for x in r] for r in rows], (len(rows), len(V)), ZZ)
            red = dm.lll().to_Matrix().tolist()
            print("== %s side %d: mult_3 = %d (c(m) = 1)" % (d.get("src", "?")[:30], side, len(rows)))
            for r in red:
                supp = [(name(V[i]), int(r[i])) for i in range(len(V)) if r[i]]
                nN = sum(1 for i in range(36) if r[i])
                nY = sum(1 for i in range(36, len(V)) if r[i])
                print("   norm %3d  |supp| N(l) %2d  Y %2d :" % (sum(int(x) ** 2 for x in r), nN, nY), supp)
            done += 1
            if done >= want:
                return

main()
