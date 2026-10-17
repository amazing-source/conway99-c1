"""Root component templates for the branch min c <= 3 (exploration, LAB 17/10/2026), extending Codex's
root_component_quotient.py (c >= 4) to all degrees and all partitions.  Not a modification of his file.

Template at a vertex v (7 root lines): J = graph of non-grid pairs; for each root i a partition of its J-neighbours
into blocks of size >= 2 (= components of G_{l_i}; singletons are grid partners, so they are J-non-edges).
c_i = (6 - deg_i) + #blocks.  Branch c_min = k (v chosen on a line of globally minimal c): all c_i >= k, some c_i = k.

Vectors v_e = T^{1/2} 1_{Q_e} (e in E(J)), Gram R = P^t T P (Codex).  Facts used (all proved; see EXPLORATION.md):
  (N) for every block B at root i: sum_{j in B} v_ij = 0 (T kills the component indicator);
  (O) same root, different blocks: <v_ij, v_ik> = 0 (no edges between the two rectangles, K-sum 0);
  (S) same root, same block: <v_ij, v_ik> = -e(Q_ij, Q_ik) <= 0, and ||v_e||^2 = 8 - 2 e(Q_e) > 0 (non-grid).
Consequences tested here (exact, no solver):
  (P) a block {j, k} of size 2 gives v_ij = -v_ik; signed classes by union-find; an odd cycle gives v = -v = 0: reject;
  (O') two links at one root in different blocks cannot be in one class (orthogonal and +-equal, nonzero): reject;
  (S') two links in one block of size >= 3 cannot be in one class (+equal contradicts <= 0; -equal makes the pair a
       closed component, i.e. the block would be the pair): reject;
  (Z) Codex: a link on which every scalar solution of (N) vanishes: reject;
  (K) at root i the Gram of {v_ij} is block diagonal, each block the Laplacian of the connected rectangle multigraph of
      that component, so the v_ij span exactly 6 - c_i dimensions; rank R <= dim ker C (Codex) forces
      dim ker C >= max_i (6 - c_i): otherwise reject.
Output: counts by c_min, rejection reasons, survivors up to Aut(J), histogram of dim ker C (rank bound for R).
usage: python cle3_templates.py <c_min> [--max-graphs n] [--out file.json]"""
import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
import time

EDGES = tuple(combinations(range(7), 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}


def relabel(mask, perm):
    r = 0
    for k, (a, b) in enumerate(EDGES):
        if mask & (1 << k):
            r |= 1 << EDGE_INDEX[tuple(sorted((perm[a], perm[b])))]
    return r


def graph_reps():
    seen, reps = set(), []
    deg = [0] * 7
    prev = 0
    for index in range(1 << 21):
        mask = index ^ (index >> 1)
        if index:
            ch = mask ^ prev
            k = ch.bit_length() - 1
            inc = 1 if mask & ch else -1
            a, b = EDGES[k]
            deg[a] += inc
            deg[b] += inc
        prev = mask
        if 1 in deg or deg != sorted(deg) or mask in seen:
            continue
        groups = [[i for i, d in enumerate(deg) if d == v] for v in sorted(set(deg))]
        orbit = set()
        for imgs in product(*(permutations(g) for g in groups)):
            perm = list(range(7))
            for g, t in zip(groups, imgs):
                for x, y in zip(g, t):
                    perm[x] = y
            orbit.add(relabel(mask, perm))
        seen.update(orbit)
        reps.append(min(orbit))
    return sorted(reps)


def automorphisms(mask):
    deg = [sum(1 for k, e in enumerate(EDGES) if mask & (1 << k) and i in e) for i in range(7)]
    groups = [[i for i, d in enumerate(deg) if d == v] for v in sorted(set(deg))]
    out = []
    for imgs in product(*(permutations(g) for g in groups)):
        perm = list(range(7))
        for g, t in zip(groups, imgs):
            for x, y in zip(g, t):
                perm[x] = y
        if relabel(mask, perm) == mask:
            out.append(perm)
    return out


def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for sub in set_partitions(rest):
        for i in range(len(sub)):
            yield sub[:i] + [[first] + sub[i]] + sub[i + 1:]
        yield [[first]] + sub


def admissible(items, kmin):
    out = []
    for P in set_partitions(list(items)):
        if all(len(b) >= 2 for b in P):
            c = 6 - len(items) + len(P)
            if c >= kmin:
                out.append((tuple(tuple(sorted(b)) for b in P), c))
    return out


class UF:
    """Signed union-find with rollback: v_x = sign(x) * v_root(x)."""

    def __init__(self, n):
        self.p = list(range(n))
        self.s = [1] * n
        self.log = []

    def find(self, x):
        s = 1
        while self.p[x] != x:
            s *= self.s[x]
            x = self.p[x]
        return x, s

    def relate_opposite(self, a, b):
        """impose v_a = -v_b; return False on an odd cycle."""
        ra, sa = self.find(a)
        rb, sb = self.find(b)
        if ra == rb:
            return sa == -sb
        # v_a = sa v_ra, v_b = sb v_rb, v_a = -v_b  =>  v_rb = -(sa / sb) v_ra
        self.p[rb] = ra
        self.s[rb] = -sa * sb
        self.log.append(rb)
        return True

    def mark(self):
        return len(self.log)

    def undo(self, m):
        while len(self.log) > m:
            x = self.log.pop()
            self.p[x] = x
            self.s[x] = 1


def nullity(nv, links, omit=None):
    adj = [[] for _ in range(nv)]
    for i, (a, b) in enumerate(links):
        if i != omit:
            adj[a].append(b)
            adj[b].append(a)
    col, bip = {}, 0
    for s in range(nv):
        if s in col:
            continue
        col[s] = 0
        st, ok = [s], True
        while st:
            a = st.pop()
            for b in adj[a]:
                if b not in col:
                    col[b] = 1 - col[a]
                    st.append(b)
                elif col[b] == col[a]:
                    ok = False
        bip += ok
    return len(links) - int(omit is not None) - nv + bip


def canonical(groups, auts):
    encs = []
    for perm in auts:
        img = [()] * 7
        for i, parts in enumerate(groups):
            img[perm[i]] = tuple(sorted(tuple(sorted(perm[a] for a in part)) for part in parts))
        encs.append(tuple(img))
    return min(encs)


def run(kmin, max_graphs=None, exact=True, start=0, end=None, verbose=False):
    t0 = time.time()
    reps = graph_reps()
    stats = Counter()
    hist = Counter()
    survivors = []
    for gnum, mask in enumerate(reps):
        if max_graphs is not None and gnum >= max_graphs:
            break
        if gnum < start or (end is not None and gnum >= end):
            continue
        tg = time.time()
        lv0 = stats["leaves"]
        edges = [e for i, e in enumerate(EDGES) if mask & (1 << i)]
        eidx = {}
        for k, (a, b) in enumerate(edges):
            eidx[(a, b)] = eidx[(b, a)] = k
        nb = [[b if a == i else a for a, b in edges if i in (a, b)] for i in range(7)]
        opts = [admissible(nb[i], kmin) for i in range(7)]
        if any(not o for o in opts):
            continue
        if exact and not any(any(c == kmin for _, c in o) for o in opts):
            continue
        order = sorted(range(7), key=lambda i: -len(nb[i]))
        uf = UF(len(edges))
        choice = [None] * 7
        seen_keys = set()
        auts = None

        def root_ok(i):
            parts = choice[i]
            cls = {}
            for bi, part in enumerate(parts):
                for j in part:
                    r, _ = uf.find(eidx[(i, j)])
                    if r in cls:
                        bj = cls[r]
                        if bj != bi:
                            return "O"            # different blocks, one class
                        if len(part) >= 3:
                            return "S"            # same block of size >= 3, one class
                    cls[r] = bi
            return None

        def rec(depth):
            nonlocal auts
            if depth == 7:
                stats["leaves"] += 1
                if exact and not any(c == kmin for _, c in choice_c):
                    stats["no_root_at_cmin"] += 1
                    return
                groups = [choice[i] for i in range(7)]
                nodes, lookup = [], {}
                for r, parts in enumerate(groups):
                    for part in parts:
                        nd = len(nodes)
                        nodes.append((r, part))
                        for j in part:
                            lookup[(r, j)] = nd
                links = [(lookup[(a, b)], lookup[(b, a)]) for a, b in edges]
                nul = nullity(len(nodes), links)
                need = max(6 - c for _, c in choice_c)
                if nul < need:
                    stats["K_rank_below_root_span"] += 1
                    return
                if any(nullity(len(nodes), links, i) == nul for i in range(len(links))):
                    stats["Z_forced_zero_link"] += 1
                    return
                stats["survivor_labelled"] += 1
                if auts is None:
                    auts = automorphisms(mask)
                key = canonical(groups, auts)
                if key in seen_keys:
                    return
                seen_keys.add(key)
                hist[nul] += 1
                survivors.append({"graph_mask": mask, "nongrid_edges": edges,
                                  "component_count_by_root_line": [c for _, c in choice_c_sorted()],
                                  "nontrivial_component_groups": [list(map(list, g)) for g in groups],
                                  "kernel_dimension": nul})
                return
            i = order[depth]
            for parts, c in opts[i]:
                mk = uf.mark()
                ok = True
                for part in parts:
                    if len(part) == 2:
                        if not uf.relate_opposite(eidx[(i, part[0])], eidx[(i, part[1])]):
                            ok = False
                            break
                if not ok:
                    stats["P_odd_cycle"] += 1
                    uf.undo(mk)
                    continue
                choice[i] = parts
                choice_c[depth] = (i, c)
                bad = None
                for d2 in range(depth + 1):
                    bad = root_ok(order[d2])
                    if bad:
                        break
                if bad:
                    stats["O_cross_block_class" if bad == "O" else "S_block_class"] += 1
                else:
                    rec(depth + 1)
                choice[i] = None
                uf.undo(mk)

        choice_c = [None] * 7

        def choice_c_sorted():
            return sorted(choice_c)

        rec(0)
        if verbose and time.time() - tg > 2:
            print("graph %d mask %d degs %s: %.1f s, leaves %d, survivors so far %d" % (
                gnum, mask, sorted(len(x) for x in nb), time.time() - tg, stats["leaves"] - lv0, len(survivors)), flush=True)
    stats["graph_reps"] = len(reps)
    return {"c_min": kmin, "stats": dict(stats), "kernel_dimension_histogram": dict(sorted(hist.items())),
            "survivors_up_to_aut": len(survivors), "elapsed_s": round(time.time() - t0, 1), "survivors": survivors}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("c_min", type=int)
    ap.add_argument("--max-graphs", type=int, default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--no-exact", action="store_true", help="all c_i >= c_min, no root required at c_min")
    a = ap.parse_args()
    res = run(a.c_min, a.max_graphs, exact=not a.no_exact, start=a.start, end=a.end, verbose=a.verbose)
    print(json.dumps({k: v for k, v in res.items() if k != "survivors"}), flush=True)
    if a.out:
        json.dump(res, open(a.out, "w"), indent=1)
