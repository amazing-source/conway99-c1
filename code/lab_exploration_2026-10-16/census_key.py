"""S7-canonical key of a root template (LAB, 18/10/2026).  Copied unchanged in substance from compare_census_aws.py
(the rule used for the exact std/la census comparison of run verif1a): orbit minimum of the non-grid graph J under S7,
then the minimum, over the permutations sending J to that minimum, of the relabelled block masks.
The key format is the one decoded by jhat_fg_keys.decode."""
from itertools import combinations, permutations

EDGES = list(combinations(range(7), 2))
EIDX = {e: k for k, e in enumerate(EDGES)}
PERMS = list(permutations(range(7)))
TABLE = {}
_rep = {}


def permute(mask, p):
    r = 0
    for k, (a, b) in enumerate(EDGES):
        if mask >> k & 1:
            x, y = p[a], p[b]
            r |= 1 << EIDX[(x, y) if x < y else (y, x)]
    return r


def to_rep(mask):
    if mask not in _rep:
        imgs = [(permute(mask, p), p) for p in PERMS]
        m = min(i for i, _ in imgs)
        _rep[mask] = (m, [p for i, p in imgs if i == m])
    return _rep[mask]


def ptable(p):
    t = TABLE.get(p)
    if t is None:
        t = [sum(1 << p[j] for j in range(7) if m >> j & 1) for m in range(128)]
        TABLE[p] = t
    return t


def key(mask, bm):
    rep, ps = to_rep(mask)
    best = None
    for p in ps:
        t = ptable(p)
        img = [None] * 7
        for r in range(7):
            img[p[r]] = tuple(sorted(t[b] for b in bm[r]))
        k = tuple(img)
        if best is None or k < best:
            best = k
    return "%d|%s" % (rep, "|".join(".".join("%02x" % b for b in blocks) for blocks in best))


def template_key(t):
    mask = t.get("graph_mask")
    if mask is None:
        mask = sum(1 << EIDX[tuple(e)] for e in t["nongrid_edges"])
    bm = [[sum(1 << j for j in B) for B in blocks] for blocks in t["nontrivial_component_groups"]]
    return key(mask, bm)
