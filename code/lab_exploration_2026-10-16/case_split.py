"""Case split from LEMMA 3-SPEC:  nu <= 14 + 2 K0 - m3,  m3 = mult_3(Gamma_S), K0 = dim(E_3(Gamma_S) cap ker B).
Conway needs nu >= 14: case A (m3 = 0, D = 0) or case B (K0 >= 1, m3 <= 2 K0).  Tabulate on sides / objects."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, gl_connected
P = 1000000007
Bm = [[1 if r in l else 0 for l in S] for r in range(14)]
K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)
def info(EE):
    G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
    X = [[(3 if i == j else 0) - G[i][j] for j in range(44)] for i in range(44)]
    m3 = 44 - rank_mod(X, P)
    k0 = 44 - rank_mod(X + Bm, P)
    T8 = 24 * np.eye(44, dtype=np.int64) - 8 * np.array(G, dtype=np.int64) - K8
    nu = 44 - rank_mod(T8.tolist(), P)
    psd = bool(np.linalg.eigvalsh(T8 / 8.0)[0] > -1e-9)
    return nu, m3, k0, 14 + 2 * k0 - m3, psd
def main():
  tab = Counter()
  if sys.argv[1] == "cache":
    done = 0
    for line in open(sys.argv[2]):
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
            tab[info(EE)] += 1; done += 1
        if done >= int(sys.argv[3]):
            break
else:
    d = json.load(open(sys.argv[2]))
    lab = [frozenset(x) for x in d["labels"]]
    for s in d["structures"][: int(sys.argv[3])]:
        EE = {frozenset((lab[i], lab[j])) for i, j in s["edges"]}
        tab[info(EE)] += 1
print("(nu, m3 = mult_3 Gamma_S, K0, bound 14+2K0-m3, positive) : count")
for k, v in sorted(tab.items()):
    print("   ", k, v)
