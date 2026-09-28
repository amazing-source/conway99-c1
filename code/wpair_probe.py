# Witness-pair (cross identity) probe: for n=5 witnesses kappa, kappa' of a class, sum_u a_u a'_u = 28(kappa, kappa').
# a, a' are +-1 exactly on the labels of 2|5 cuts S, S'. If S != S' the common cut has 4 or 5 cells (8 or 10 labels), so
# |7(kappa,kappa')| <= 2; hence |7(kappa,kappa')| >= 3 forces S = S' (same skeleton parities).
import sys, json, numpy as np
sys.path.insert(0, '.')
import rank17_skeleton as sk
from envelope_trap import inverse_exact
from fractions import Fraction as Fr
from collections import Counter
op = json.load(open('../data/rank17/open_after_sol.json'))
stats = Counter(); ex = 0; forced = 0; tot = 0
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 60
for key in op[:lim]:
    tag, pid = key.split(':'); pid = int(pid)
    if tag == 'Z17': continue
    K = json.load(open('../data/rank17/K_%s.json' % tag)); rec = [r for r in K['K'] if r['id'] == pid][0]
    GK = np.array(rec['K_gram'], dtype=np.int64)
    W = sk.witnesses(GK, 8)
    Gi = inverse_exact([[int(x) for x in r] for r in GK])
    def ip(x, y): return sum(Fr(int(x[i])) * Gi[i][j] * int(y[j]) for i in range(15) for j in range(15) if x[i] and y[j])
    n5 = [x for x, n in W if n == 5]
    ms = []
    for i in range(len(n5)):
        for j in range(i + 1, len(n5)):
            ms.append(abs(int(7 * ip(n5[i], n5[j]))))
    stats.update(ms); tot += 1
    if any(m >= 3 for m in ms): forced += 1
    if ex < 8:
        print(key, 'witness n:', [n for _, n in W], ' |7(k,k2)| over n5 pairs:', sorted(ms)); ex += 1
print('classes', tot, ' with an n5 pair forcing S = S2:', forced)
print('|7(k,k2)| distribution over n5 pairs:', sorted(stats.items()))
