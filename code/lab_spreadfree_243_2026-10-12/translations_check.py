"""Lab session, 2026-10-12. Which translations of F_3^5 (vertex = base-3 digits) are automorphisms of the stored graphs.
python -I translations_check.py <directory srg243>"""
import sys, itertools, collections
def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    adj = [set() for _ in range(243)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    return adj
def dig(x): return tuple((x // 3 ** i) % 3 for i in range(5))
def num(d): return sum(d[i] * 3 ** i for i in range(5))
names = ["bvls243.edges", "twin243_switched.edges", "family/gamma3_aut864.edges", "family/gamma4_aut3888.edges"]
for nm in names:
    adj = load(sys.argv[1] + "/" + nm)
    T = []
    for t in range(243):
        dt = dig(t); f = [num(tuple((a + b) % 3 for a, b in zip(dig(x), dt))) for x in range(243)]
        if all({f[y] for y in adj[x]} == adj[f[x]] for x in range(243)): T.append(t)
    print(nm, ": translations of F_3^5 (digit labelling) that are automorphisms:", len(T), [dig(t) for t in T][:10])
    # orders of semiregularity: is the translation group's orbit partition into cosets?
# the stored generators of Aut for gamma3, gamma4
import os
for nm in ["family/gamma3_aut864.autgens", "family/gamma4_aut3888.autgens"]:
    p = sys.argv[1] + "/" + nm
    txt = open(p).read(); print(nm, "size", len(txt), "head:", txt[:300].replace("\n", " | "))
