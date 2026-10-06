"""After fixing two mate stars S = L_a u L_a' (stage 1), every other label l = {x,y} (x,y not in {a,a'}) has exactly
2 neighbours in L_a and 2 in L_a' (mu with a and with a').  Its frame vector has residual norm (orthogonal to the
22-dim span of stage 1)  (1/7)(5/2 - t^T T_SS^+ t),  t = T_{S,l} = -Gamma_{S,l} - K_{S,l}.  Necessary: >= 0, and the
60 residual norms must sum to 8 (tight frame in R^8).  Measure, for random stage-1 structures, the fraction of
adjacency choices with non-negative residual and the range of the residual norms."""
import random, itertools, numpy as np, sys
from twostar_psd import rand_matching, caps_ok, TS, E, mate
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
import twostar_psd; twostar_psd.rng = rng
# full element set of N(v): a=12, a'=13, E = 0..11 (6 mate pairs (0,1),(2,3),...)
def Kval(l1, l2, mt):
    inter = len(set(l1) & set(l2)); m = sum(1 for x in l1 for y in l2 if mt(x) == y)
    return 3 / 8 * inter + 1 / 8 * m - 1 / 4
mt = lambda x: 13 if x == 12 else 12 if x == 13 else x ^ 1
stage_labels = [(12, x) for x in E] + [(13, x) for x in E]
others = [(x, y) for x, y in itertools.combinations(E, 2) if y != (x ^ 1)]
print("remaining labels:", len(others))
for trial in range(3):
    while True:
        t, tp = rand_matching(), rand_matching(); s = dict(zip(E, rng.sample(E, 12)))
        if caps_ok(t, tp, s): break
    T = TS(t, tp, s); Tp = np.linalg.pinv(T)
    Kc = {l: np.array([Kval(l, sl, mt) for sl in stage_labels]) for l in others}
    fr_ok = []; vals_all = []
    for l in others:
        x, y = l
        vals = []
        for na in itertools.combinations(range(12), 2):
            for nap in itertools.combinations(range(12), 2):
                g = np.zeros(24); g[list(na)] = 1; g[[12 + j for j in nap]] = 1
                tvec = -g - Kc[l]
                vals.append(2.5 - tvec @ Tp @ tvec)
        vals = np.array(vals); vals_all.append(vals)
        fr_ok.append((vals >= -1e-9).mean())
    allv = np.concatenate(vals_all)
    print("stage-1 sample", trial, ": fraction of (2+2)-adjacency choices with residual >= 0, per label: min %.3f median %.3f max %.3f" %
          (min(fr_ok), np.median(fr_ok), max(fr_ok)), "; 7*residual range [%.2f, %.2f]" % (allv.min(), allv.max()),
          "; required mean 7*residual = 56/60 = %.3f" % (56 / 60))
