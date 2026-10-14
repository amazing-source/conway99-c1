"""Independent check of Codex's obstruction (14/10/2026): K = {x in F_2^points : every line meets x evenly} for a GQ
given by its lines. If K is doubly even (every vector of weight 0 mod 4), a 3-ovoid O cannot exist when the number of
points minus |O| is 2 mod 4: the complement of O meets every line in (line size - 3) points, an even number when lines
have 9 points, so it lies in K. Exact F_2 elimination with Python integers as bit rows.
usage: python binary_obstruction.py <gq json (key 'lines', points 0..n-1)> <n>"""
import json, sys
G = json.load(open(sys.argv[1])); lines = G["lines"]; n = int(sys.argv[2])
rows = []
for L in lines:
    r = 0
    for p in L: r |= 1 << p
    rows.append(r)
# row echelon form of M (lines x points) over F_2
piv = {}
for r in rows:
    while r:
        h = r.bit_length() - 1
        if h in piv: r ^= piv[h]
        else: piv[h] = r; break
rank = len(piv)
# kernel of M: x with M x = 0  <=> x orthogonal to the row space; basis from the reduced echelon form
# reduce fully
keys = sorted(piv)
for h in keys:
    for h2 in keys:
        if h2 != h and (piv[h2] >> h) & 1: piv[h2] ^= piv[h]
pivcols = set(piv)
free = [c for c in range(n) if c not in pivcols]
basis = []
for f in free:
    x = 1 << f
    for h, r in piv.items():
        if (r >> f) & 1: x |= 1 << h
    basis.append(x)
for x in basis:
    for r in rows:
        assert bin(x & r).count("1") % 2 == 0
w = [bin(x).count("1") for x in basis]
dbl = all(c % 4 == 0 for c in w)
orth = all(bin(basis[i] & basis[j]).count("1") % 2 == 0 for i in range(len(basis)) for j in range(i + 1, len(basis)))
print("points %d, lines %d: F_2 rank of the incidence matrix %d, kernel dimension %d" % (n, len(lines), rank, len(basis)))
print("kernel basis weights mod 4: %s; pairwise intersections all even: %s -> kernel doubly even: %s"
      % (sorted(set(c % 4 for c in w)), orth, dbl and orth))
