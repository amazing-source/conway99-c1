"""Shared tools for srg(243,22,1,2) experiments: graph I/O, exact srg check, nauty group data."""
import subprocess, itertools, re
import numpy as np

NAUTY = "/tmp/solvers/nauty_src/nauty2_8_8/"
N, K, LAM, MU = 243, 22, 1, 2


def load_edges(path, n=N):
    M = np.zeros((n, n), dtype=np.int64)
    for line in open(path):
        if line.strip():
            i, j = map(int, line.split()); M[i, j] = M[j, i] = 1
    return M


def save_edges(M, path):
    with open(path, "w") as f:
        for i in range(len(M)):
            for j in range(i + 1, len(M)):
                if M[i, j]:
                    f.write(f"{i} {j}\n")


def srg_defects(M, k=K, lam=LAM, mu=MU):
    """number of violated conditions (0 iff srg(n,k,lam,mu))."""
    n = len(M); M = M.astype(np.int64); M2 = M @ M
    off = ~np.eye(n, dtype=bool)
    bad = int((M != M.T).sum()) + int(np.diag(M).sum()) + int((M.sum(1) != k).sum())
    bad += int((M2[(M == 1)] != lam).sum()) + int((M2[(M == 0) & off] != mu).sum())
    return bad


def is_srg(M, **kw):
    return srg_defects(M, **kw) == 0


def dreadnaut_input(M, extra=""):
    n = len(M)
    lines = [f"n={n} g"] + [" ".join(str(j) for j in np.nonzero(M[i])[0] if j > i) + ";" for i in range(n)]
    return "\n".join(lines) + "\n" + extra


def aut(M, partition=None):
    """nauty: group order (string), orbits (list of lists), generators (list of permutations)."""
    n = len(M)
    extra = ""
    if partition is not None:
        extra += "f=[" + "|".join(",".join(map(str, c)) for c in partition) + "]\n"
    extra += "a\nx\no\nq\n"
    out = subprocess.run([NAUTY + "dreadnaut"], input=dreadnaut_input(M, extra), capture_output=True,
                         text=True).stdout
    m = re.search(r"grpsize=([0-9.e]+)", out)
    order = m.group(1) if m else "?"
    head, tail = out.split("grpsize", 1)
    # generators: a generator starts with '(' in column 0, continuation lines are indented
    gens, cur = [], None
    for line in head.split("\n"):
        if line.startswith("("):
            if cur is not None:
                gens.append(cur)
            cur = line
        elif line.startswith(" ") and cur is not None and line.strip()[:1] in "0123456789(":
            cur += " " + line
        else:
            if cur is not None:
                gens.append(cur); cur = None
    if cur is not None:
        gens.append(cur)
    perms = []
    for g in gens:
        p = list(range(n))
        for cyc in re.findall(r"\(([0-9\s]+)\)", g):
            c = list(map(int, cyc.split()))
            for a, b in zip(c, c[1:] + c[:1]):
                p[a] = b
        perms.append(p)
    lines = tail.split("\n")[1:]
    lines = [l for l in lines if "cpu time" not in l]
    flat = " ".join(" ".join(lines).split())
    orbits = []
    for tok in flat.split(";"):
        tok = re.sub(r"\(\d+\)", "", tok).strip()
        mem = []
        for part in tok.split():
            if ":" in part:
                a, b = map(int, part.split(":")); mem += list(range(a, b + 1))
            elif part.isdigit():
                mem.append(int(part))
        if mem:
            orbits.append(mem)
    return order, orbits, perms


def canon_g6(M):
    import networkx as nx
    g6 = nx.to_graph6_bytes(nx.from_numpy_array(M), header=False)
    return subprocess.run([NAUTY + "labelg", "-q"], input=g6, capture_output=True).stdout.strip()


def triangles(M):
    n = len(M); out = []
    for i in range(n):
        for j in np.nonzero(M[i])[0]:
            if j > i:
                for k in np.nonzero(M[i] & M[j])[0]:
                    if k > j:
                        out.append((i, int(j), int(k)))
    return out


def grids_per_vertex(M):
    """number of induced 3x3 grids through each vertex (lambda=1, mu=2 graphs)."""
    n = len(M); tri = triangles(M)
    lines_at = [[] for _ in range(n)]
    for t in tri:
        for p in t:
            lines_at[p].append(t)
    g = np.zeros(n, dtype=np.int64)
    seen = set()
    for p in range(n):
        for L1, L2 in itertools.combinations(lines_at[p], 2):
            a = [x for x in L1 if x != p]; b = [x for x in L2 if x != p]
            # grid closure: the 4 points a_i + b_j must exist (common neighbours) and form lines
            ok = True; pts = set(L1) | set(L2)
            Q = {}
            for ai in a:
                for bj in b:
                    cn = [c for c in np.nonzero(M[ai] & M[bj])[0] if c != p]
                    if len(cn) != 1:
                        ok = False; break
                    Q[(ai, bj)] = cn[0]
                if not ok:
                    break
            if not ok:
                continue
            q = Q
            if not (M[q[(a[0], b[0])], q[(a[0], b[1])]] and M[q[(a[1], b[0])], q[(a[1], b[1])]]
                    and M[q[(a[0], b[0])], q[(a[1], b[0])]] and M[q[(a[0], b[1])], q[(a[1], b[1])]]):
                continue
            pts |= set(q.values())
            if len(pts) != 9:
                continue
            sub = M[np.ix_(sorted(pts), sorted(pts))]
            if sub.sum() != 36:
                continue
            key = frozenset(pts)
            if key not in seen:
                seen.add(key)
                for x in pts:
                    g[x] += 1
    return g, len(seen)


def twisted_pairs(M):
    """(#pairs of disjoint lines joined by exactly 2 edges, # joined by 3)."""
    tri = triangles(M); n = len(M)
    L = np.zeros((len(tri), n), dtype=np.int64)
    for i, t in enumerate(tri):
        L[i, list(t)] = 1
    E = L @ M @ L.T
    inter = L @ L.T
    disj = inter == 0
    iu = np.triu(np.ones_like(E, dtype=bool), 1)
    return int(((E == 2) & disj & iu).sum()), int(((E == 3) & disj & iu).sum())
