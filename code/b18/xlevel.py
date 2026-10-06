"""Branch 18 (t = 0), level 1: the X-configurations of a support D.

X = E2 (18 zeros, 2 P-neighbours and 2 N-neighbours each).  Forced data (derived):
  * P-pair multiset: {p,p'} with multiplicity 2 - |row_p & row_p'|  (mu = 2 for p,p'; total 18);
    N-pair multiset likewise;  so X is a bijection between the 18 P-slots and the 18 N-slots.
Constraints on an X vertex u = (pi, nu) and on the configuration (all from lambda/mu):
  (a) for p in pi: |nu & row_p| <= 1 ; for v in nu: |pi & col_v| <= 1        (lambda on the edges u-p, u-v)
  (c) x(p,v) = #{u in X: p in pi_u, v in nu_u} <= 2 - D[p][v]                  (common zeros of p and v)
  (d) two X vertices: |pi & pi'| + |nu & nu'| <= 2                              (mu; never 4 common neighbours)
Counts labelled configurations (identical slots ordered) for one support.
"""
import itertools, json, sys, time


def pair_slots(rows, n=9):
    sl = []
    for a, b in itertools.combinations(range(n), 2):
        m = 2 - len(rows[a] & rows[b])
        assert m >= 0
        sl += [(a, b)] * m
    return sl


def count_x(Drows, limit=None, collect=False):
    rows = [set(r) for r in Drows]
    cols = [set(p for p in range(9) if v in rows[p]) for v in range(9)]
    D = [[1 if v in rows[p] else 0 for v in range(9)] for p in range(9)]
    Ps = pair_slots(rows); Ns = pair_slots(cols)
    assert len(Ps) == 18 and len(Ns) == 18
    ok = [[True] * 18 for _ in range(18)]
    for i, pi in enumerate(Ps):
        for j, nu in enumerate(Ns):
            good = all(len(set(nu) & rows[p]) <= 1 for p in pi) and all(len(set(pi) & cols[v]) <= 1 for v in nu)
            good = good and all(D[p][v] == 0 or True for p in pi for v in nu)
            # (c) for a single vertex: x(p,v) >= 1 needs 2 - D >= 1, always true
            ok[i][j] = good
    x = [[0] * 9 for _ in range(9)]
    Nlist = sorted(set(Ns)); Ncnt = {nu: Ns.count(nu) for nu in Nlist}
    okp = {(pi, nu): ok[Ps.index(pi)][Ns.index(nu)] for pi in set(Ps) for nu in Nlist}
    chosen = []
    cnt = [0]
    sols = []

    def rec(i):
        if limit and cnt[0] >= limit:
            return
        if i == 18:
            cnt[0] += 1
            if collect:
                sols.append(list(chosen))
            return
        pi = Ps[i]
        lo = 0
        if i > 0 and Ps[i - 1] == pi:
            lo = Nlist.index(chosen[-1][1]) + 1   # identical P-slots: strictly increasing N-pair
        for jn in range(lo, len(Nlist)):
            nu = Nlist[jn]
            if Ncnt[nu] == 0 or not okp[(pi, nu)]:
                continue
            if any(x[p][v] + 1 > 2 - D[p][v] for p in pi for v in nu):
                continue
            if any(len(set(pi) & set(pk)) + len(set(nu) & set(nk)) > 2 for pk, nk in chosen):
                continue
            Ncnt[nu] -= 1; chosen.append((pi, nu))
            for p in pi:
                for v in nu:
                    x[p][v] += 1
            rec(i + 1)
            for p in pi:
                for v in nu:
                    x[p][v] -= 1
            Ncnt[nu] += 1; chosen.pop()
    rec(0)
    return cnt[0], sols


if __name__ == "__main__":
    sups = json.load(open("supports18.json"))
    which = range(len(sups)) if len(sys.argv) < 2 else [int(a) for a in sys.argv[1].split(",")]
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else None
    for s in which:
        t = time.time()
        c, _ = count_x(sups[s], limit=lim)
        print("support", s, "labelled X-configurations", c, ("(limit hit)" if lim and c >= lim else ""),
              round(time.time() - t, 1), flush=True)
