import sys, json, glob
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from modp_germ import t8
from intmult import rank_big, hperm
C = [(0, 2), (0, 3), (1, 2), (1, 3)]
def info(f):
    d = json.load(open(f))
    labels = [tuple(sorted(l)) for l in d["labels"]]
    idx = {l: i for i, l in enumerate(labels)}
    E = set(tuple(sorted(e)) for e in d["edges"])
    g = all(tuple(sorted((idx[a], idx[b]))) in E for a, b in [((0,2),(0,3)), ((1,2),(1,3)), ((0,2),(1,2)), ((0,3),(1,3))])
    M8, G = t8(labels, d["edges"])
    r7 = rank_big((M8 % 7).tolist(), 7)
    return g, r7
pats = sys.argv[1:]
files = sorted(set(sum((glob.glob(p) for p in pats), [])))
for f in files:
    print(f.split("/")[-1].split("\\")[-1], "grid(l,m) =", *info(f))
