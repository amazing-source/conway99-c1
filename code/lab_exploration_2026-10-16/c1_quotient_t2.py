"""The two-neighbour configurations around a c = 1 line, on the Gram quotient (exploration, LAB 17/10/2026).
List: the 60 classes (under S6 on lines 1..6) of {j: B_j, j': B_j'} = components of Q_{0j} at two other lines j, j'
(c1_vertex_types.entries for the all-equal profile).  Each is tested on the quotient of c1_quotient.py, optionally with
a rectangle profile at line 0 (R[Q_0j, Q_0j] = 8 - 2 e_j; the profile breaks the S6 symmetry, so with a profile the
list is generated for that profile).
usage: python c1_quotient_t2.py <case index or -> <seconds> <out.json>"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c1_quotient as Q  # noqa: E402
import c1_vertex_types as VT  # noqa: E402
import c1_cases as CS  # noqa: E402


def main():
    ci = None if sys.argv[1] == "-" else int(sys.argv[1])
    secs, outf = float(sys.argv[2]), sys.argv[3]
    case = CS.all_cases()[ci] if ci is not None else (0, 0, 0, 0, 0, 0)
    ent = VT.entries(case, 5)
    res = json.load(open(outf)) if os.path.exists(outf) else {}
    extra = None
    if ci is not None:
        def extra(m, R):
            for k, j in enumerate(range(1, 7)):
                m.Add(R[Q.rid(0, j)][Q.rid(0, j)] == 8 - 2 * case[k])
    t0 = time.time()
    for (a, b, A, B) in ent:
        key = "%s|%d:%s|%d:%s" % ("-" if ci is None else ci, a, ",".join(map(str, A)), b, ",".join(map(str, B)))
        if key in res:
            continue
        st, nc, M = Q.quotient_status({a: list(A), b: list(B)}, secs, extra)
        res[key] = st
        json.dump(res, open(outf, "w"), indent=0)
        print("  %s : %s (%d cuts, %.0f s)" % (key, st, nc, time.time() - t0), flush=True)
        if time.time() - t0 > 270:
            print("time budget reached", flush=True)
            break
    tally = {}
    for k, v in res.items():
        if k.startswith(("-" if ci is None else str(ci)) + "|"):
            tally[v] = tally.get(v, 0) + 1
    print("TALLY:", tally, "of", len(ent), flush=True)


if __name__ == "__main__":
    main()
