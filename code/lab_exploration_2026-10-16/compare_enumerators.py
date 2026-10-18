"""Compare the survivors of the two template enumerators up to S7 (LAB, 18/10/2026).
  cle_templates.cpp (union-find pruning, its own graph representatives) writes jsonl lines with graph_mask and
  nontrivial_component_groups; cle_templates_la.cpp (linear-algebra pruning, orbit-minimum representatives) writes
  "mask|blocks of root 0|...|blocks of root 6".  Every template is mapped to a key that is canonical under S7:
  min over the permutations pi with pi(J) = orbit minimum of J of the relabelled partition (own code).
usage: python compare_enumerators.py --std <jsonl or jsonl.gz>... --la <txt or txt.gz>... [--out report.json]"""
import gzip
import json
import sys
from itertools import combinations, permutations

EDGES = list(combinations(range(7), 2))
EIDX = {e: k for k, e in enumerate(EDGES)}
PERMS = list(permutations(range(7)))


def permute(mask, p):
    r = 0
    for k, (a, b) in enumerate(EDGES):
        if mask >> k & 1:
            x, y = p[a], p[b]
            r |= 1 << EIDX[(x, y) if x < y else (y, x)]
    return r


_to_rep = {}


def to_rep(mask):
    """(orbit minimum, list of permutations mapping mask onto it)."""
    if mask not in _to_rep:
        imgs = [(permute(mask, p), p) for p in PERMS]
        m = min(i for i, _ in imgs)
        _to_rep[mask] = (m, [p for i, p in imgs if i == m])
    return _to_rep[mask]


_tables = {}


def perm_table(p):
    t = _tables.get(p)
    if t is None:
        t = [0] * 128
        for m in range(128):
            r = 0
            for j in range(7):
                if m >> j & 1:
                    r |= 1 << p[j]
            t[m] = r
        _tables[p] = t
    return t


def key(mask, parts):
    """canonical under S7: the orbit minimum of J, then the minimum over the permutations onto it of the relabelled
    blocks (as bit masks) of every root."""
    rep, ps = to_rep(mask)
    bm = [[sum(1 << j for j in B) for B in parts[r]] for r in range(7)]
    best = None
    for p in ps:
        t = perm_table(p)
        img = [None] * 7
        for r in range(7):
            img[p[r]] = tuple(sorted(t[b] for b in bm[r]))
        k = tuple(img)
        if best is None or k < best:
            best = k
    return (rep, best)


def opener(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


args = sys.argv[1:]
std_files = args[args.index("--std") + 1: args.index("--la")]
la_files = [a for a in args[args.index("--la") + 1:] if not a.startswith("--") and a not in (args[args.index("--out") + 1] if "--out" in args else [],)]
if "--out" in args:
    out = args[args.index("--out") + 1]
    la_files = [a for a in la_files if a != out]
std, la = set(), set()
n_std = n_la = 0
for f in std_files:
    for line in opener(f):
        t = json.loads(line)
        std.add(key(t["graph_mask"], [[tuple(B) for B in blocks] for blocks in t["nontrivial_component_groups"]]))
        n_std += 1
for f in la_files:
    for line in opener(f):
        fields = line.strip().split("|")
        mask = int(fields[0])
        parts = [[tuple(int(ch) for ch in b) for b in fld.split(".")] if fld else [] for fld in fields[1:]]
        la.add(key(mask, parts))
        n_la += 1
rep = {"std_lines": n_std, "la_lines": n_la, "std_up_to_S7": len(std), "la_up_to_S7": len(la),
       "only_std": len(std - la), "only_la": len(la - std), "identical": std == la}
print(json.dumps(rep))
if std - la:
    print("ONLY STD:", sorted(std - la)[:3])
if la - std:
    print("ONLY LA:", sorted(la - std)[:3])
if "--out" in args:
    json.dump(rep, open(out, "w"))
