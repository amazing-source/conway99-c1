"""Direct enumeration of class-level twist patterns with exactly k = 3 twisting labels (rules R0, L12, L13a),
up to symmetry. Two shapes: (A) three twisting labels in three different classes, normalised to (0,0),(1,0),(2,0);
(B) both labels of class 0 plus one label of class 1: (0,0),(0,1),(1,0).
A pattern assigns to each twisting label a the set C_a of classes it twists (|C_a| >= 2, [a] not in C_a).
Output: canonical representatives, as 'label:classes' specs usable by rooted_family.py (per-label domains).
"""
import itertools, sys

C7 = range(7)


def rules_ok(pat):
    """pat: dict label -> frozenset of twisted classes (only twisting labels)."""
    W = lambda a, j: j in pat.get(a, ())
    labels = [(c, s) for c in C7 for s in (0, 1)]
    for a, Cs in pat.items():
        if len(Cs) < 2 or a[0] in Cs:
            return False
    for j in C7:  # L13a
        n = sum(1 for a in pat if j in pat[a])
        if n == 1:
            return False
    for a, Cs in pat.items():  # L12
        for j in Cs:
            third = any(W(y, j) for y in pat if y[0] not in (a[0], j))
            for c in [(j, 0), (j, 1)]:
                if not (W(c, a[0]) or third):
                    return False
    return True


def canon(pat, shape):
    best = None
    if shape == 'A':
        movable = [0, 1, 2]
        rest = [3, 4, 5, 6]
        for p3 in itertools.permutations(movable):
            for p4 in itertools.permutations(rest):
                perm = dict(zip(movable, p3)); perm.update(zip(rest, p4))
                img = tuple(sorted(((perm[a[0]], 0), tuple(sorted(perm[j] for j in Cs))) for a, Cs in pat.items()))
                if best is None or img < best:
                    best = img
    else:
        rest = [2, 3, 4, 5, 6]
        for p5 in itertools.permutations(rest):
            perm = {0: 0, 1: 1}; perm.update(zip(rest, p5))
            for swap in (0, 1):
                img = tuple(sorted(((perm[a[0]], a[1] ^ swap if a[0] == 0 else a[1]), tuple(sorted(perm[j] for j in Cs)))
                                   for a, Cs in pat.items()))
                if best is None or img < best:
                    best = img
    return best


def enumerate_shape(shape):
    labs = [(0, 0), (1, 0), (2, 0)] if shape == 'A' else [(0, 0), (0, 1), (1, 0)]
    options = {}
    for a in labs:
        others = [c for c in C7 if c != a[0]]
        options[a] = [frozenset(S) for r in range(2, 7) for S in itertools.combinations(others, r)]
    reps = {}
    for combo in itertools.product(*[options[a] for a in labs]):
        pat = dict(zip(labs, combo))
        if rules_ok(pat):
            c = canon(pat, shape)
            reps.setdefault(c, pat)
    return reps


if __name__ == '__main__':
    allreps = []
    for shape in ('A', 'B'):
        reps = enumerate_shape(shape)
        print(f'shape {shape}: {len(reps)} patterns up to symmetry', flush=True)
        for c, pat in sorted(reps.items()):
            spec = ','.join(f'{a[0]}{a[1]}:' + ''.join(str(j) for j in sorted(Cs)) for a, Cs in sorted(pat.items()))
            allreps.append(spec)
    open('../data/k3_patterns.txt', 'w').write('\n'.join(allreps) + '\n')
    print('total', len(allreps), 'written to data/k3_patterns.txt')
