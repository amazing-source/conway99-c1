"""Lab session, 2026-10-12. The S3 question at the level of the GAINS (not only their parities): local problem at one
vertex P of the Brouwer-Haemers graph BH = srg(81,20,1,6).

A 3-fold cover of BH whose fibres are triangles is given by gains g_xy in S3 = Sym(fibre) (g_yx = g_xy^-1). It is a
srg(243,22,1,2) iff (lambda = 1) the holonomy of every line of BH is trivial and (mu = 2) for every non-adjacent pair
{x, y} the six permutations h_z = g_zy g_xz (z a common neighbour) cover every (p, r) exactly twice, i.e. the multiset
{h_z} is "A3 twice", "the three transpositions twice" or "S3 once".

Gauge at P (relabelling of the fibres, which loses nothing): g_Pz = id for the 20 neighbours z; then the lines through P
have gain id; for each far vertex R, g_{z0 R} = id for its first common neighbour z0 with P. Then:
  * block R: the multiset {g_zR : z in C(P,R)} contains id, so it is "A3 twice" (FLAT) or "S3 once" (SPLIT);
  * inner pair {z, z'} (non-adjacent neighbours of P): its paths are the one through P (gain id) and those through the
    five far R adjacent to both, of gain g_{z'R}^-1 g_zR; the multiset is again "A3 twice" or "S3 once".
These are all the conditions carried by the pairs through P and the pairs inside N(P): the local problem at P.
If no solution has a split block, then in every such cover every pair of BH is flat, the parities of the gains form a
coboundary, and the cover is a Z3-cover.

S3 is coded as 0..5: the permutations of (0,1,2) in lexicographic order.
python s3_local.py <tmp dir> <seconds> [nontrivial | split=<r0> | free | parity=<A|B>:<k>] [max=<k>]"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L

PERMS = list(itertools.permutations(range(3))); IDX = {p: i for i, p in enumerate(PERMS)}; ID = IDX[(0, 1, 2)]
mul = lambda a, b: IDX[tuple(PERMS[a][PERMS[b][i]] for i in range(3))]          # a after b
inv = lambda a: IDX[tuple(sorted(range(3), key=lambda i: PERMS[a][i]))]
sign = lambda a: sum(1 for i in range(3) for j in range(i) if PERMS[a][j] > PERMS[a][i]) % 2
EVEN = [a for a in range(6) if sign(a) == 0]; ODD = [a for a in range(6) if sign(a) == 1]
assert all(mul(a, inv(a)) == ID for a in range(6)) and len(EVEN) == 3


def build(opts):
    nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    g = {}                                                    # g[(z, R)][a] : the gain g_zR is the permutation a
    for r in L.far:
        for i, z in enumerate(L.C[r]):
            vs = [new() for _ in range(6)]; g[(z, r)] = vs
            cl.append(list(vs))
            for a, b in itertools.combinations(range(6), 2): cl.append([-vs[a], -vs[b]])
            if i == 0: cl.append([vs[ID]])
    def multiset(items, has_id):
        """items: list of one-hot 6-tuples; together with one extra id if has_id, the multiset is A3 twice or S3 once.
        returns the variable 'flat'."""
        F = new(); m = len(items)
        for vs in items:
            for a in ODD: cl.append([-F, -vs[a]])                       # flat: no odd element
        for a in range(6):
            cap_split = 1 if not (has_id and a == ID) else 0            # split: each element once in all (the extra id counts)
            cap_flat = (2 if not (has_id and a == ID) else 1)           # flat: each even element twice in all
            # at most cap_flat always (for even a); at most cap_split unless flat
            if cap_split == 0:
                for vs in items: cl.append([F, -vs[a]])
            else:
                for i, j in itertools.combinations(range(m), 2): cl.append([F, -items[i][a], -items[j][a]])
            if a in EVEN:
                if cap_flat == 1:
                    for i, j in itertools.combinations(range(m), 2): cl.append([-items[i][a], -items[j][a]])
                else:
                    for i, j, k in itertools.combinations(range(m), 3): cl.append([-items[i][a], -items[j][a], -items[k][a]])
        # counting: m items + has_id = 6 in all. flat: no odd, caps 2,2,2 on the even ones => exactly A3 twice.
        # not flat: caps 1 on each of the six elements (the extra id included) => exactly S3 once.
        return F
    flatR = {}
    for r in L.far:
        flatR[r] = multiset([g[(z, r)] for z in L.C[r]], False)
    flatP = {}
    for p in L.pairs:
        a, b = p; ks = []
        for r in L.pblocks[p]:
            kv = [new() for _ in range(6)]; ks.append(kv)
            cl.append(list(kv))
            for u, w in itertools.combinations(range(6), 2): cl.append([-kv[u], -kv[w]])
            for u in range(6):
                for w in range(6): cl.append([-g[(a, r)][u], -g[(b, r)][w], kv[mul(inv(w), u)]])     # g_bR^-1 g_aR
        flatP[p] = multiset(ks, True)
    for o in opts:
        if o == "nontrivial": cl.append([-flatR[r] for r in L.far])
        elif o.startswith("split="): cl.append([-flatR[L.far[int(o[6:])]]])
        elif o.startswith("parity="):                      # parity=<type>:<k> : the parities of the block far[0] are its k-th state of type A or B
            typ, kk = o[7:].split(":"); r = L.far[0]
            sts = [t for t in range(1, 11) if L.state_type(r, L.MASKS[t]) == typ]; m = L.MASKS[sts[int(kk)]]
            for i, z in enumerate(L.C[r]):
                for a in (ODD if not (m >> i) & 1 else EVEN): cl.append([-g[(z, r)][a]])
    return nv[0], cl, g, flatR, flatP


if __name__ == "__main__":
    tmp, tl = sys.argv[1], float(sys.argv[2]); opts = sys.argv[3:]
    mx = next((int(o[4:]) for o in opts if o.startswith("max=")), 5)
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    nv, cl, g, flatR, flatP = build(opts)
    print("S3 local problem at P = 0, options %s: %d variables, %d clauses" % (opts, nv, len(cl)), flush=True)
    path = os.path.join(tmp, "s3loc_%d.cnf" % os.getpid()); nsol = 0; t0 = time.time(); status = "complete (UNSAT after the last one)"
    while True:
        with open(path, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (nv, len(cl)))
            for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
        try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired: status = "TIMEOUT (no decision on the last call)"; break
        if "s UNSATISFIABLE" in out: break
        assert "s SATISFIABLE" in out
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        val = {k: [a for a in range(6) if vs[a] in model][0] for k, vs in g.items()}
        # verification of the model against the definition, independently of the clauses
        for r in L.far:
            ms = sorted(val[(z, r)] for z in L.C[r]); assert ms in (sorted(EVEN * 2), list(range(6))), ms
        for p in L.pairs:
            ms = sorted([ID] + [mul(inv(val[(p[1], r)]), val[(p[0], r)]) for r in L.pblocks[p]]); assert ms in (sorted(EVEN * 2), list(range(6))), ms
        nsplit = sum(1 for r in L.far if flatR[r] not in model); nsp = sum(1 for p in L.pairs if flatP[p] not in model)
        nsol += 1; print("  solution %d (verified): split blocks %d of 60, split inner pairs %d of 180  (%.1f s)" % (nsol, nsplit, nsp, time.time() - t0), flush=True)
        cl.append([-g[k][val[k]] for k in g])
        if nsol >= mx: status = "stopped at max"; break
    print("options %s: %d solution(s); %s; %.1f s" % (opts, nsol, status, time.time() - t0), flush=True)
    try: os.remove(path)
    except OSError: pass
