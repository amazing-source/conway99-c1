"""Where do our PSD c = 1 data sides fall in the case list of c1_cases.py? (exploration, LAB 17/10/2026)
For every positive four-star side (T_S >= 0) with c(l) = 1: the e-profile at the root l (e of the rectangle shared
with m, then the five outer ones sorted), whether the root m has a 3-edge rectangle (E3 at m), and the first exact
lemma that kills the side (as in c1_exact_kill.py).  Sides with E3 at l are outside the list (e = 3).
usage: python c1_cases_data.py <distinct cache.jsonl>"""
import itertools
import json
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
sys.path.insert(0, __file__.rsplit("\\", 2)[0] + "\\stars_rank_2026-10-14" if "\\" in __file__ else "../stars_rank_2026-10-14")
from stars_rank import kval  # noqa: E402
from gg_test import orient, line_graph, components  # noqa: E402

ROOTS = [(2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]


def rect_e(L, EE, a0, a1, rt):
    q = [frozenset((r, t)) for r in (a0, a1) for t in rt]
    return sum(1 for x, y in itertools.combinations(q, 2) if frozenset((x, y)) in EE)


def main():
    from c1_cutfilter import tests
    import c1_rlattice as RL
    from c1_exact_kill import c2b_kills
    per_case = defaultdict(Counter)
    out_list = Counter()
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S = [frozenset(x) for x in d["labels"]]
        E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
        n = 44
        G = np.zeros((n, n))
        for i, j in itertools.combinations(range(n), 2):
            if frozenset((S[i], S[j])) in E:
                G[i, j] = G[j, i] = 1
        T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
        if np.linalg.eigvalsh(T)[0] < -1e-9:
            continue
        for side in (0, 1):
            L, EE = orient(S, d["edges"], side)
            V, pos, A = line_graph(L, EE)
            if not all(sum(r) == 3 for r in A) or components(A) != 1:
                continue
            el = [rect_e(L, EE, 0, 1, rt) for rt in ROOTS]
            em = [rect_e(L, EE, 2, 3, rt) for rt in [(0, 1)] + ROOTS[1:]]
            if 3 in el:
                out_list["E3 at l (outside the list)"] += 1
                continue
            key = "%d:%s" % (el[0], "".join(map(str, sorted(el[1:], reverse=True))))
            out, _ = tests(L, EE)
            if 3 in em:
                why = "E3 at m"
            elif "LD" in out:
                why = "C2a"
            elif any(k.startswith("killed") for k in RL.analyse(L, EE)):
                why = "RL"
            elif c2b_kills(V, A):
                why = "C2b"
            else:
                why = "SURVIVOR"
            per_case[key][why] += 1
            out_list["in the list"] += 1
    print("PSD c = 1 sides:", dict(out_list))
    for key in sorted(per_case, key=lambda k: -sum(per_case[k].values())):
        print("  case %s: %s" % (key, dict(per_case[key])))


if __name__ == "__main__":
    main()
