"""Audit (15/10/2026): transversal counts t(l), t(m) of the 331 rank-30 PSD four-star objects (bridge G11:
'T, U >= 0 and rank <= 30 force t(l) + t(m) >= 15' would give P >= 867 > 852 = Codex's order-9 census bound).
t(l) = #{x off l : z_{0x} ~ z_{1x}} (fixed points of sigma_l), t(m) = #{x off m : z_{2x} ~ z_{3x}}.
usage: python audit_transversals.py rank30_psd_objects_2026-10-15.json"""
import json
import sys

d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]
idx = {s: i for i, s in enumerate(S)}
hist, sums = {}, {}
for st in d["structures"]:
    E = {frozenset((i, j)) for i, j in st["edges"]}
    tl = sum(1 for x in range(2, 14) if frozenset((idx[frozenset((0, x))], idx[frozenset((1, x))])) in E)
    tm = sum(1 for x in [0, 1] + list(range(4, 14)) if frozenset((idx[frozenset((2, x))], idx[frozenset((3, x))])) in E)
    k = (tuple(st["c"]), tl, tm)
    hist[k] = hist.get(k, 0) + 1
    sums[tl + tm] = sums.get(tl + tm, 0) + 1
print("t(l) + t(m) distribution over %d objects:" % len(d["structures"]), dict(sorted(sums.items())))
print("(c, t(l), t(m)) : count")
for k, v in sorted(hist.items()):
    print("  ", k, v)
