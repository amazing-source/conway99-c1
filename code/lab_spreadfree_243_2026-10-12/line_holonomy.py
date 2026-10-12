"""Lab session, 2026-10-12. HOLONOMY OF A LINE in a strongly regular graph srg(v,k,1,2) (own definition).

For an edge {a, b} with third point c of its line, every neighbour x of a outside the line has exactly one neighbour
m_ab(x) among the neighbours of b outside the line (x and b are non-adjacent with common neighbours a and m_ab(x)).
Going round the line L = {p, u, u*}: tau_L = m_{u* p} o m_{u u*} o m_{p u} is a permutation of the k - 2 neighbours of p
outside L (its conjugacy class does not depend on the base point). A fixed point w of tau_L is a line through w joined
to L by a perfect matching ("parallel" to L). L is FLAT when tau_L is the identity. In a regular spread every line is flat.
Two lines L, M through p span a 3x3 grid iff tau_L fixes the two points of M and tau_M fixes the two points of L.

For each graph: distribution of the cycle types of tau_L over all lines; number of flat lines; whether the flat lines
are exactly the lines of the regular spreads (found by verify_drg.spreads).
python line_holonomy.py <edge file> [<edge file> ...]"""
import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "s3_question_2026-10-12"))
import verify_drg


def holonomy(adj, p, u, us):
    """tau as a dict on N(p) minus the line {p,u,us}"""
    L = {p, u, us}
    def m(a, b, x):                      # the neighbour of x (x ~ a, x off the line) among N(b) off the line
        c = [t for t in adj[x] & adj[b] if t != a]; assert len(c) == 1 and c[0] not in L; return c[0]
    return {w: m(us, p, m(u, us, m(p, u, w))) for w in adj[p] if w not in L}


def cycle_type(perm):
    seen = set(); ct = []
    for a in perm:
        if a in seen: continue
        n = 0; b = a
        while b not in seen: seen.add(b); b = perm[b]; n += 1
        ct.append(n)
    return tuple(sorted(ct))


if __name__ == "__main__":
    for path in sys.argv[1:]:
        n, adj = verify_drg.load(path)
        lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(n) for y in adj[x] if x < y})
        types = collections.Counter(); flat = set(); fixes = collections.Counter()
        for (p, u, us) in lines:
            ct = cycle_type(holonomy(adj, p, u, us)); types[ct] += 1; fixes[ct.count(1)] += 1
            if all(c == 1 for c in ct): flat.add((p, u, us))
        sps = verify_drg.spreads(n, adj); spread_lines = {t for sp in sps for t in sp}
        print("%s: %d lines; flat lines: %d; lines of the %d regular spread(s): %d; flat = spread lines: %s" % (
            os.path.basename(path), len(lines), len(flat), len(sps), len(spread_lines), flat == spread_lines))
        print("   number of parallel lines (fixed points of tau): %s" % sorted(fixes.items()))
        print("   cycle types of tau (type: number of lines): %s" % sorted(types.items(), key=lambda t: -t[1])[:12])
