"""Vertex types around a c = 1 line, run as a whole list on the exact global model (exploration, LAB 17/10/2026).
Root vertex o, line l = line 0 = {o,0,1} with c(l) = 1 and rectangle profile (case of c1_cases.py).  For two other lines
j < j' through o with c >= 2, the component of the rectangle Q_{0j} at line j is a set B_j (0 in B_j, other line indices,
size 2..5) and similarly B_j'; a zero cut at line j around B_j gives x^t T x = 0, hence T x = 0 EXACTLY (x = 1_{Q_j(B_j)}),
added as plain equalities (no reification).  The remaining four lines are free (any c).
Entry = (profile, j, j', B_j, B_j').  Symmetry: lines 1..6 are interchangeable except for the profile values e(Q_{0j});
entries are reduced by relabelling the lines with equal e(Q_{0j}) (canonical form under that group).
Degree pre-filter (exact): a block B at line j is a union of components of M_j, so sum over its rectangles of the
degrees 8 - 2e must be even and every rectangle of B has its M_j-edges inside B; with B = {Q_{0j}, Q_{jk}} this forces
e(Q_{jk}) = e(Q_{0j}).  Entries are generated without the profile constraint on Q_{jk} (unknown), so no filter is applied
beyond the solver itself.
usage: python c1_vertex_types.py <case index> <max block size> <seconds> <status.json> [start] [count]"""
import itertools
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c1_cases as CS  # noqa: E402


def blocks_for(j, maxsize):
    others = [k for k in range(1, 7) if k != j]
    out = []
    for size in range(1, maxsize):
        for sub in itertools.combinations(others, size):
            out.append((0,) + sub)
    return out


def canonical(case, j, jp, Bj, Bjp):
    """relabel lines 1..6 by permutations preserving e(Q_{0k}) (profile values); return the lexicographically
    smallest image of the entry."""
    e = {k: case[k - 1] for k in range(1, 7)}
    classes = {}
    for k in range(1, 7):
        classes.setdefault(e[k], []).append(k)
    best = None
    perms_per_class = [list(itertools.permutations(v)) for v in classes.values()]
    keys = list(classes.values())
    for choice in itertools.product(*perms_per_class):
        f = {0: 0}
        for src, dst in zip(keys, choice):
            for a, b in zip(src, dst):
                f[a] = b
        a, b = f[j], f[jp]
        A = tuple(sorted(f[t] for t in Bj))
        B = tuple(sorted(f[t] for t in Bjp))
        if a > b:
            a, b, A, B = b, a, B, A
        key = (a, b, A, B)
        if best is None or key < best:
            best = key
    return best


def entries(case, maxsize):
    seen = set()
    out = []
    for j, jp in itertools.combinations(range(1, 7), 2):
        for Bj in blocks_for(j, maxsize):
            for Bjp in blocks_for(jp, maxsize):
                key = canonical(case, j, jp, Bj, Bjp)
                if key in seen:
                    continue
                seen.add(key)
                out.append(key)
    return out


def spec(j, B):
    rest = [k for k in range(7) if k != j and k not in B]
    s = "%d:%s" % (j, ",".join(map(str, B)))
    if rest:
        s += "|" + ",".join(map(str, rest))
    return s


def main():
    ci, maxsize, secs, statf = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    start = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    count = int(sys.argv[6]) if len(sys.argv) > 6 else 10 ** 9
    case = CS.all_cases()[ci]
    ent = entries(case, maxsize)
    status = json.load(open(statf)) if os.path.exists(statf) else {}
    print("case %d %s: %d vertex-type entries (two templated lines, block sizes <= %d)" % (ci, case, len(ent), maxsize),
          flush=True)
    py = sys.executable
    t0 = time.time()
    for idx in range(start, min(len(ent), start + count)):
        a, b, A, B = ent[idx]
        key = "%d|%d:%s|%d:%s" % (ci, a, ",".join(map(str, A)), b, ",".join(map(str, B)))
        if key in status:
            continue
        env = dict(os.environ)
        env["VTYPE"] = spec(a, A) + ";" + spec(b, B)
        env.pop("CM", None)
        env.pop("CMP", None)
        env.pop("BRANCH", None)
        tmp = os.path.join(HERE, "unbiased_walks", "_vt_tmp_%d.json" % os.getpid())
        r = subprocess.run([py, os.path.join(HERE, "c1_global_list.py"), "%d-%d" % (ci, ci + 1), str(secs), tmp],
                           env=env, capture_output=True, text=True)
        st = "ERROR"
        for line in r.stdout.splitlines():
            if line.startswith("case "):
                st = "INFEASIBLE" if "INFEASIBLE" in line else ("UNKNOWN" if "UNKNOWN" in line else "FEASIBLE")
        if os.path.exists(tmp):
            os.remove(tmp)
        status[key] = st
        json.dump(status, open(statf, "w"), indent=0)
        print("  [%d] %s : %s (%.0f s)" % (idx, key, st, time.time() - t0), flush=True)
    tally = {}
    for k, v in status.items():
        if k.startswith("%d|" % ci):
            tally[v] = tally.get(v, 0) + 1
    print("TALLY case %d: %s" % (ci, tally), flush=True)


if __name__ == "__main__":
    main()
