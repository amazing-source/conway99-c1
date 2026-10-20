"""Why do the symmetric connected lines die at once?  (LAB 20/10/2026)  For the Z6 x Z2 line graphs with c = 1, d = 1,
(tau|7) = -1: candidates per p-pair (L2 + Green norm 0), the root p-pair (smallest domain), how many root candidates
leave every other domain non-empty under the pure pairwise Green test (value in {3,4}), and the killer p-pairs."""
import collections
import sys

import numpy as np
import sympy

sys.path.insert(0, ".")
from sym_gt import groups, line_graph  # noqa: E402
from oblr_prep import P7  # noqa: E402
from ll_test import components, gt_matrix, k_matrix, pairs_of  # noqa: E402
from rank7_line import rank_mod  # noqa: E402
from adversarial import det_mod  # noqa: E402

done = 0
for name, H, mul, z in groups()[1:4]:
    for t in H:
        s01, s12, s20 = line_graph(H, mul, z, t)
        G = gt_matrix(12, s01, s12, s20)
        if (k_matrix(12, G) < 0).any():
            continue
        nc, comp = components(G)
        L = (3 * np.eye(36, dtype=np.int64) - G) % P7
        if nc != 1 or 36 - rank_mod(L, P7) != 1 or pow(det_mod(L[1:, 1:], P7), 3, P7) != P7 - 1:
            continue
        Om = np.array(sympy.Matrix(((L + 1) % 7).tolist()).inv_mod(7).tolist(), dtype=np.int64)
        P = pairs_of(12)
        nb = [set(int(y) for y in np.nonzero(G[x])[0]) for x in range(36)]
        cands, trip = [], []
        for pp in P:
            cl, tl = [], []
            for qq in P:
                for ss in P:
                    names = [pp[0], pp[1], 12 + qq[0], 12 + qq[1], 24 + ss[0], 24 + ss[1]]
                    nm = set(names)
                    if any(len(nb[x] & nm) > 1 for x in names):
                        continue
                    cnt = collections.Counter(x for y in names for x in nb[y] if x not in nm)
                    if any(v > 2 for v in cnt.values()):
                        continue
                    e = np.zeros(36, dtype=np.int64)
                    e[names] = 1
                    if int(e @ Om @ e) % 7 == 0:
                        cl.append(e)
                        tl.append((qq, ss))
            cands.append(np.array(cl))
            trip.append(tl)
        sizes = [len(c) for c in cands]
        root = int(np.argmin(sizes))
        killers = collections.Counter()
        alive = 0
        for e in cands[root]:
            dead = [q for q in range(60) if q != root and not np.isin((cands[q] @ Om @ e) % 7, (3, 4)).any()]
            if dead:
                killers.update(dead)
            else:
                alive += 1
        print("%s t=%s: cands per p-pair %d..%d; root %s with %d cands; survive pairwise FC: %d; killers (p-pair: count) %s"
              % (name, t, min(sizes), max(sizes), P[root], sizes[root], alive,
                 {str(P[q]): c for q, c in killers.most_common(6)}), flush=True)
        # Green values between the root p-pair's candidates and a killer's candidates
        if killers:
            q = killers.most_common(1)[0][0]
            vals = collections.Counter(((cands[q] @ Om @ cands[root].T) % 7).ravel().tolist())
            print("   values root x top killer %s: %s ; Omega restricted to C0 (row of vertex 0): %s"
                  % (P[q], dict(sorted(vals.items())), Om[0, :12].tolist()), flush=True)
        done += 1
        if done >= 3:
            sys.exit(0)
