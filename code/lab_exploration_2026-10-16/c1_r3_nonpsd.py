"""rank_3(A_Omega) on ALL c(l) = 1 sides (positive or not), and on the special non-positive structures."""
import itertools, json, sys, os
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, build_H, gl_connected

def r3_and_psd(EE):
    G = np.zeros((44, 44))
    for i, j in itertools.combinations(range(44), 2):
        if frozenset((S[i], S[j])) in EE:
            G[i, j] = G[j, i] = 1
    K8 = np.array([[k8(a, b) for b in S] for a in S], float)
    lam = np.linalg.eigvalsh((24 * np.eye(44) - 8 * G - K8) / 8)[0]
    V9, A9 = build_H(EE, with_l=True)
    rq = rank_mod((A9 - 3 * np.eye(len(V9), dtype=np.int64)).tolist(), 1000000007)
    return rank_mod(A9.tolist(), 3), rq, lam > -1e-9

tab = Counter()
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
        r3, rq, psd = r3_and_psd(EE)
        tab[(psd, r3 <= 45, rq <= 45)] += 1
print("all c(l)=1 sides of the cache: (positive, rank_3 <= 45 [Conway-compatible mod 3], rank_Q(A-3I) <= 45) : count")
for k, v in sorted(tab.items()):
    print("   ", k, v)
mins = Counter()
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
        r3, rq, psd = r3_and_psd(EE)
        if not psd:
            mins[r3] += 1
print("non-positive c=1 sides, rank_3 histogram:", dict(sorted(mins.items())))
W = sys.argv[2]
for fn in ["odd9_failures_c1_nonpsd.json"]:
    dd = json.load(open(os.path.join(W, fn)))
    recs = dd if isinstance(dd, list) else dd.get("structures", dd.get("records", [dd]))
    for r in recs:
        lab = [frozenset(x) for x in r["labels"]]
        EE = {frozenset((lab[i], lab[j])) for i, j in r["edges"]} if isinstance(r["edges"][0][0], int) else \
             {frozenset((frozenset(a), frozenset(b))) for a, b in r["edges"]}
        r3, rq, psd = r3_and_psd(EE)
        print("ODD9 failure (exact odd kernel vector, non-positive): rank_3 =", r3, " rank_Q(A-3I) =", rq, " psd", psd)
