"""Conjecture test (LAB 17/10/2026, night): hidden 3-eigenvectors of A_Omega occur only with a forbidden configuration.
For every c(l) = 1 side of the cache (positive or not): first exact lemma that kills it (E3 at the l- or m-rectangles,
C2a, RL, C2b, as in c1_exact_kill.py), and hidden = mult_3(A_Omega) - 3 - c(m) (Conway needs >= 11 - c(m)).
usage: python c1_hidden_vs_lemmas.py <distinct_cache.jsonl>"""
import itertools, json, sys, time
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, build_H, gl_connected, relabel
from c1_hidden import comps_m
from c1_e3free_floor import e3_free
from gg_test import orient, line_graph, components
from c1_cutfilter import tests
import c1_rlattice as RL
from c1_exact_kill import c2b_kills

t0 = time.time()
tab = Counter()
free = []
START = int(sys.argv[2]) if len(sys.argv) > 2 else 0
STOP = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
BUDGET = float(sys.argv[4]) if len(sys.argv) > 4 else 250
nside = -1
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
        nside += 1
        if nside < START or nside >= STOP or time.time() - t0 > BUDGET:
            continue
        G = np.zeros((44, 44))
        for i, j in itertools.combinations(range(44), 2):
            if frozenset((S[i], S[j])) in EE:
                G[i, j] = G[j, i] = 1
        K8 = np.array([[k8(a, b) for b in S] for a in S], float)
        psd = bool(np.linalg.eigvalsh((24 * np.eye(44) - 8 * G - K8) / 8)[0] > -1e-9)
        V9, A9 = build_H(EE, with_l=True)
        nu = 59 - rank_mod((A9 - 3 * np.eye(59, dtype=np.int64)).tolist(), 1000000007)
        cm, _ = comps_m(EE)
        hidden = nu - 3 - cm
        # lemmas (orientation with l = {0,1}); cheap ones first; C2b only if hidden > 0 or not yet killed
        Lo, EEo = orient(S0, d["edges"], side)
        if not e3_free(EE):
            k = "E3"
        else:
            out, _ = tests(Lo, EEo)
            if out:
                k = "C2a/cut"
            elif any(o.startswith("killed") for o in RL.analyse(Lo, EEo)):
                k = "RL"
            else:
                Vg, pos, Ag = line_graph(Lo, EEo)
                k = "C2b" if c2b_kills(Vg, Ag) else "FREE"
        tab[(k, psd, hidden)] += 1
        if k == "FREE":
            free.append((d.get("src"), side, psd, cm, nu, hidden))
print("c(l)=1 sides: (first killing lemma, positive, hidden) : count   [Conway: hidden >= 11 - c(m) >= 6]")
for key, c in sorted(tab.items()):
    print("   ", key, c)
print("lemma-free sides:", len(free))
for f in free:
    if f[-1] > 0:
        print("   HIDDEN>0", f)
json.dump([f for f in free if f[-1] > 0], open("unbiased_walks/lemma_free_hidden_%d_%d.json" % (START, STOP), "w"))
print("sides %d..%d processed up to index %d, time %.0f s" % (START, STOP, nside, time.time() - t0))
