"""Lab session, 2026-10-12. Local problem at the vertex P = 0 of the Brouwer-Haemers graph, second encoding (states).

BH: V = F_3^4, x ~ y iff q(y - x) = 0, q = x0^2 + x1^2 + x2 x3.
Blocks = the 60 far vertices v (non-neighbours of P); Oct(v) = N(P) & N(v) (6 points of N(P)), with its three GRID PAIRS
{z, v - z}. State of a block: 0 = flat, or a partition 3+3 of Oct(v):
   type A = every grid pair is separated (4 partitions), type B = exactly one grid pair is separated (6 partitions).
Pairs = the 180 non-adjacent pairs {a, b} inside N(P); each lies in exactly five blocks: the grid block a + b and two
grid pairs of blocks {v, a + b - v}. Constraint: the number of blocks separating a from b is 0 or 3.
A split pair is of type A when its separators are the grid block and one block of each of the two grid pairs of blocks
(then the pair {a, b}, seen from a, is a type A block of the local problem at a), and of type B otherwise.

Variables: x[r][s] (block r in state s, exactly one s), y[p][i] (the i-th block of the pair p separates it).
python local_cnf2.py <tmp dir> <seconds per call> [options]
  options:  cube=<r0>:<s>     the block far[r0] is in state s (1..10)
            split=<r0>        the block far[r0] is split (any partition)
            typeB=<r0>        the block far[r0] is split of type B
            typeA=<r0>        the block far[r0] is split of type A
            noB               no block is of type B
            noA               no block is of type A
            pairsB            every split pair is of type B
            count             add the two counting identities at every point u of N(P), as cardinality constraints
                              (implied by the other clauses, but not accessible to resolution):
                              #(split blocks through u) = #(split pairs through u), and
                              #(type B blocks through u with u off the separated grid pair) = #(split pairs through u
                              whose grid block does not separate them)
            pairsA            every split pair is of type A
            nontrivial        some block is split
            max=<k>           stop after k solutions (default 50)
All solutions are enumerated with cadical and blocking clauses; each is identified as "trivial", "line <delta>" or OTHER."""
import sys, os, subprocess, itertools, time

V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}; n = 81
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
Bf = lambda x, y: (2 * x[0] * y[0] + 2 * x[1] * y[1] + x[2] * y[3] + x[3] * y[2]) % 3
add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b))
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
S = [v for v in V if any(v) and q(v) == 0]
nbs = [set(I[add(V[i], s)] for s in S) for i in range(n)]
P = 0; NP = sorted(nbs[P]); far = [r for r in range(n) if r != P and r not in nbs[P]]
C = {r: sorted(nbs[P] & nbs[r]) for r in far}
partner = {r: {z: I[sub(V[r], V[z])] for z in C[r]} for r in far}          # grid partner of z in the block r
for r in far: assert all(partner[r][z] in C[r] and partner[r][z] != z for z in C[r])
# states: masks on the six positions of C[r], bit 0 = 0, weight 3
MASKS = [0] + [m for m in range(64) if not (m & 1) and bin(m).count("1") == 3]
def state_type(r, m):
    if m == 0: return "flat"
    pos = {z: i for i, z in enumerate(C[r])}
    sep = sum(1 for z in C[r] if ((m >> pos[z]) ^ (m >> pos[partner[r][z]])) & 1) // 2
    assert sep in (1, 3); return "A" if sep == 3 else "B"
pairs = [(a, b) for a, b in itertools.combinations(NP, 2) if b not in nbs[a]]; assert len(pairs) == 180
pblocks = {}
for (a, b) in pairs:
    g = I[add(V[a], V[b])]; assert g in far and a in C[g] and b in C[g]
    others = [r for r in far if a in C[r] and b in C[r] and r != g]; assert len(others) == 4
    v = others[0]; w = I[sub(add(V[a], V[b]), V[v])]; assert w in others
    rest = [r for r in others if r not in (v, w)]; assert I[sub(add(V[a], V[b]), V[rest[0]])] == rest[1]
    pblocks[(a, b)] = [g, v, w, rest[0], rest[1]]                           # grid block, grid pair, grid pair
iso = []
for z in NP:
    if I[tuple((-c) % 3 for c in V[z])] not in iso: iso.append(z)


def build(opts):
    nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    x = {r: [new() for _ in MASKS] for r in far}
    for r in far:
        cl.append(list(x[r]))
        for s, t in itertools.combinations(range(11), 2): cl.append([-x[r][s], -x[r][t]])
    y = {}
    for p in pairs:
        a, b = p; ys = []
        for r in pblocks[p]:
            pa, pb = C[r].index(a), C[r].index(b); v = new(); ys.append(v)
            sepst = [s for s in range(11) if ((MASKS[s] >> pa) ^ (MASKS[s] >> pb)) & 1]
            for s in range(11): cl.append([-x[r][s], v] if s in sepst else [-x[r][s], -v])
        y[p] = ys
        for four in itertools.combinations(range(5), 4): cl.append([-ys[i] for i in four])
        for i in range(5):
            for three in itertools.combinations([j for j in range(5) if j != i], 3): cl.append([-ys[i]] + [ys[j] for j in three])
        if "pairsA" in opts:                       # split pair: grid block and exactly one of each grid pair of blocks
            g, v, w, v2, w2 = ys
            for u1, u2 in ((v, w), (v2, w2)):
                cl += [[-g, u1, u2], [-g, -u1, -u2], [g, -u1], [g, -u2]]
        if "pairsB" in opts:                       # split pair: not (grid block and one of each grid pair of blocks)
            g, v, w, v2, w2 = ys
            for u1 in (v, w):
                for u2 in (v2, w2): cl.append([-g, -u1, -u2])
    if "count" in opts:
        def exactly(lits, k):                      # sequential counter: exactly k of the literals are true
            prev = None
            for i, l in enumerate(lits):
                cur = [new() for _ in range(k + 2)]            # cur[j] : at least j among lits[0..i], j = 0..k+1
                cl.append([cur[0]])
                for j in range(1, k + 2):
                    pj = prev[j] if prev else None; pj1 = prev[j - 1] if prev else (None if j > 1 else "T")
                    # cur[j] <-> pj or (l and pj1)
                    if pj is not None: cl.append([-pj, cur[j]])
                    if pj1 == "T": cl.append([-l, cur[j]])
                    elif pj1 is not None: cl.append([-l, -pj1, cur[j]])
                    a = [-cur[j]] + ([pj] if pj is not None else [])
                    cl.append(a + [l])
                    if pj1 != "T": cl.append(a + ([pj1] if pj1 is not None else []))
                prev = cur
            cl.append([prev[k]]); cl.append([-prev[k + 1]])
        sp = {}; b0 = {}
        for p in pairs:
            v = new(); sp[p] = v; cl.append([-v] + list(y[p]))
            for t in y[p]: cl.append([-t, v])
            w = new(); b0[p] = w; cl += [[-w, v], [-w, -y[p][0]], [w, -v, y[p][0]]]
        for u in NP:
            blocks_u = [r for r in far if u in C[r]]; pairs_u = [p for p in pairs if u in p]
            assert len(blocks_u) == 18 and len(pairs_u) == 18
            exactly([-x[r][0] for r in blocks_u] + [-sp[p] for p in pairs_u], 18)
            off = []
            for r in blocks_u:
                iu, ip = C[r].index(u), C[r].index(partner[r][u])
                sts = [s for s in range(1, 11) if state_type(r, MASKS[s]) == "B" and not (((MASKS[s] >> iu) ^ (MASKS[s] >> ip)) & 1)]
                v = new(); off.append(v); cl.append([-v] + [x[r][s] for s in sts])
                for s in sts: cl.append([-x[r][s], v])
            exactly(off + [-b0[p] for p in pairs_u], 18)
    for o in opts:
        if o.startswith("cube="):
            r0, s = o[5:].split(":"); cl.append([x[far[int(r0)]][int(s)]])
        elif o.startswith("split="): cl.append([-x[far[int(o[6:])]][0]])
        elif o.startswith("typeB="):
            r = far[int(o[6:])]; cl.append([x[r][s] for s in range(1, 11) if state_type(r, MASKS[s]) == "B"])
        elif o.startswith("typeA="):
            r = far[int(o[6:])]; cl.append([x[r][s] for s in range(1, 11) if state_type(r, MASKS[s]) == "A"])
        elif o == "noB":
            for r in far:
                for s in range(1, 11):
                    if state_type(r, MASKS[s]) == "B": cl.append([-x[r][s]])
        elif o == "noA":
            for r in far:
                for s in range(1, 11):
                    if state_type(r, MASKS[s]) == "A": cl.append([-x[r][s]])
        elif o == "nontrivial": cl.append([-x[r][0] for r in far])
    return nv[0], cl, x, y


def identify(st):
    split = sorted(r for r in far if st[r])
    if not split: return "trivial"
    for d in iso:
        if split == sorted(r for r in far if Bf(V[r], V[d]) == 0):
            ok = True
            for r in split:
                cls = {z: Bf(V[z], V[d]) for z in C[r]}; m = MASKS[st[r]]
                if len({(cls[z], (m >> i) & 1) for i, z in enumerate(C[r])}) != 2: ok = False
            return "line %s%s" % (V[d], "" if ok else " BUT other partitions")
    types = {}
    for r in split: t = state_type(r, MASKS[st[r]]); types[t] = types.get(t, 0) + 1
    return "OTHER (%d split, types %s)" % (len(split), types)


if __name__ == "__main__":
    tmp, tl = sys.argv[1], int(sys.argv[2]); opts = sys.argv[3:]
    mx = 50
    for o in opts:
        if o.startswith("max="): mx = int(o[4:])
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    nv, cl, x, y = build(opts)
    path = os.path.join(tmp, "loc2_%d.cnf" % os.getpid()); nsol = 0; t0 = time.time(); status = "complete (UNSAT after the last one)"
    print("options %s: %d variables, %d clauses" % (opts, nv, len(cl)), flush=True)
    while True:
        with open(path, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (nv, len(cl)))
            for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
        try:
            out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired:
            status = "TIMEOUT (no decision on the last call)"; break
        if "s UNSATISFIABLE" in out: break
        assert "s SATISFIABLE" in out
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        st = {r: [s for s in range(11) if x[r][s] in model][0] for r in far}
        nsol += 1; print("  solution %d: %s  (%.1f s)" % (nsol, identify(st), time.time() - t0), flush=True)
        cl.append([-x[r][st[r]] for r in far])
        if nsol >= mx: status = "stopped at max"; break
    print("options %s: %d solution(s); %s; %.1f s" % (opts, nsol, status, time.time() - t0), flush=True)
    try: os.remove(path)
    except OSError: pass
