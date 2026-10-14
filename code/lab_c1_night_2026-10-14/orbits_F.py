"""Orbits of the choices of the five lines through [+1,+2] (see affine_cube.py) under block permutations and sign
changes of blocks 3..7, by union-find on generators. Writes cube_reps.txt (one representative per orbit)."""
import itertools
import sys

import affine_cube as AC

Fs = AC.all_F()
print("choices:", len(Fs), flush=True)
index = {F: i for i, F in enumerate(Fs)}
parent = list(range(len(Fs)))


def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i


def image(F, pm, fl):
    img = {}
    for X, tm in zip(range(3, 8), F):
        img[pm[X]] = tuple(sorted(tuple(sorted((pm[b], s * fl[b]) for (b, s) in e)) for e in tm))
    return tuple(img[X] for X in range(3, 8))


ident = {b: b for b in range(3, 8)}
noflip = {b: 1 for b in range(3, 8)}
gens = []
for b in range(3, 7):
    pm = dict(ident)
    pm[b], pm[b + 1] = b + 1, b
    gens.append((pm, noflip))
for b in range(3, 8):
    fl = dict(noflip)
    fl[b] = -1
    gens.append((ident, fl))
for i, F in enumerate(Fs):
    for pm, fl in gens:
        j = index[image(F, pm, fl)]
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
orbits = {}
for i in range(len(Fs)):
    orbits.setdefault(find(i), []).append(i)
reps = sorted((len(v), Fs[min(v)]) for v in orbits.values())
print("orbits:", len(reps), " sizes:", sorted(len(v) for v in orbits.values()))
with open("cube_reps.txt", "w") as f:
    for size, F in reps:
        f.write(repr((size, F)) + "\n")
