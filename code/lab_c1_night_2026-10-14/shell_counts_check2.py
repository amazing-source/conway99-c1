"""Brute-force control on srg(243,22,1,2) of the general formulas behind NOTE_NIGHT 26.3 (lambda = 1, mu = 2 only):
far set of an induced C4 (n - 4k + 8), of a paw (n - 4k + 7), induced paths inside the far set of a line
(|Z| (C(k-6,2) - (k/2 - 6)) - (3(k-2) - 3p); for k = 14 this is 60 * 27 - (36 - 3p)), disjoint lines with exactly one edge to a line (3(k-2)(k/2 - 3) + 3p)."""
import itertools
import random
from math import comb

exec(open("shell_counts_check.py", encoding="utf-8").read().split("# brute force counts over triples")[0])
rng = random.Random(1)
lines = sorted({tuple(sorted((a, b, c))) for a in range(n) for b in nb[a] for c in nb[a] & nb[b]})
print("lines:", len(lines), "(n k / 6 =", n * k // 6, ")")


def far(S):
    Ss = set(S)
    return [z for z in range(n) if z not in Ss and not any(adj(z, s) for s in S)]


# induced C4s and paws: sample some
c4s, paws = [], []
while len(c4s) < 20 or len(paws) < 20:
    a = rng.randrange(n)
    b, d = rng.sample(sorted(nb[a]), 2)
    if adj(b, d):
        # a, b, d is a line: paw = line + pendant at a
        e = rng.choice(sorted(nb[a] - {b, d}))
        if not adj(e, b) and not adj(e, d):
            paws.append((a, b, d, e))
        continue
    cs = (nb[b] & nb[d]) - {a}
    for c in cs:
        if not adj(a, c):
            c4s.append((a, b, c, d))
print("C4 far sizes:", sorted({len(far(Q)) for Q in c4s[:20]}), " formula", n - 4 * k + 8)
print("paw far sizes:", sorted({len(far(Q)) for Q in paws[:20]}), " formula", n - 4 * k + 7)
# line: prism number, far set, induced paths inside it, lines with exactly one edge to it
for l in rng.sample(lines, 3):
    X = set(v for v in range(n) if v not in l and any(adj(v, s) for s in l))
    Z = far(l)
    Zs = set(Z)
    p = sum(1 for m in lines if not set(m) & set(l) and sum(1 for u in m for s in l if adj(u, s)) == 3)
    one = sum(1 for m in lines if not set(m) & set(l) and sum(1 for u in m for s in l if adj(u, s)) == 1)
    paths = 0
    for y in Z:
        Ny = sorted(nb[y] & Zs)
        paths += sum(1 for a, b in itertools.combinations(Ny, 2) if not adj(a, b))
    print("line: p =", p, " |Z| =", len(Z), " paths in Z:", paths, " formula", len(Z) * (comb(k - 6, 2) - (k // 2 - 6)) - (3 * (k - 2) - 3 * p),
          " lines with one edge:", one, " formula", 3 * (k - 2) * (k // 2 - 3) + 3 * p)
