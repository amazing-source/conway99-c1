"""Target T1 (locally affine vertex): fix the five lines through the outer vertex [+1,+2] and write the CNF.

Inner vertices: block b in 1..7, sign s in {+1,-1}  ->  index 1 + 2(b-1) + (0 if s > 0 else 1).
Fact used (NOTE_NIGHT section 4): the ten disjoint neighbours of [a,b] are the points of five lines through [a,b],
one line for each block X outside {A,B}; the line "missing X" consists of [a,b] and two outer vertices [d,e], [f,g]
with d,e,f,g in the four remaining blocks, one in each. Each inner vertex outside A, B is used by exactly two of
the ten.

usage: python affine_cube.py list            -> number of choices for the five lines, and number up to symmetry
       python affine_cube.py cnf K out.cnf   -> CNF of T1 with the K-th representative fixed
"""
import itertools
import sys

import srg_sat as S


def iv(b, s):
    return 1 + 2 * (b - 1) + (0 if s > 0 else 1)


def two_matchings(blocks4):
    """All signed 2-matchings on four blocks: ((b1,s1),(b2,s2)), ((b3,s3),(b4,s4))."""
    a, b, c, d = blocks4
    out = []
    for (p, q), (r, t) in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))):
        for signs in itertools.product((1, -1), repeat=4):
            e1 = tuple(sorted(((p, signs[0]), (q, signs[1]))))
            e2 = tuple(sorted(((r, signs[2]), (t, signs[3]))))
            out.append(tuple(sorted((e1, e2))))
    return out


def all_F():
    """All choices of the five lines through [+1,+2] with every inner vertex of blocks 3..7 used exactly twice."""
    res = []
    opts = {X: two_matchings([b for b in range(3, 8) if b != X]) for X in range(3, 8)}

    def rec(X, chosen, use):
        if X == 8:
            if all(use.get((b, s), 0) == 2 for b in range(3, 8) for s in (1, -1)):
                res.append(tuple(chosen))
            return
        for tm in opts[X]:
            ok = True
            touched = []
            for e in tm:
                for v in e:
                    use[v] = use.get(v, 0) + 1
                    touched.append(v)
                    if use[v] > 2:
                        ok = False
            if ok:
                rec(X + 1, chosen + [tm], use)
            for v in touched:
                use[v] -= 1

    rec(3, [], {})
    return res


def canon(F):
    """Canonical form under permutations of blocks 3..7 and sign changes of blocks 3..7."""
    best = None
    for perm in itertools.permutations(range(3, 8)):
        pm = dict(zip(range(3, 8), perm))
        for flips in itertools.product((1, -1), repeat=5):
            fl = dict(zip(range(3, 8), flips))
            img = {}
            for X, tm in zip(range(3, 8), F):
                new = tuple(sorted(tuple(sorted((pm[b], s * fl[b]) for (b, s) in e)) for e in tm))
                img[pm[X]] = new
            cand = tuple(img[X] for X in range(3, 8))
            if best is None or cand < best:
                best = cand
    return best


def representatives():
    Fs = all_F()
    seen = {}
    for F in Fs:
        c = canon(F)
        seen.setdefault(c, 0)
        seen[c] += 1
    return Fs, sorted(seen.items())


if __name__ == "__main__":
    if sys.argv[1] == "list":
        Fs, reps = representatives()
        print("choices:", len(Fs), " up to symmetry:", len(reps))
        for i, (c, mult) in enumerate(reps):
            print(i, mult, c)
    else:
        K, out = int(sys.argv[2]), sys.argv[3]
        Fs, reps = representatives()
        F = reps[K][0]
        mate = {a: (a + 1 if a % 2 == 1 else a - 1) for a in range(1, 15)}
        n, k, lam, mu, fixed, _, outer, idx = S.local_view(lambda a, b: mate[b])
        enc, e = S.encode(n, k, lam, mu, fixed)

        def ov(p, q):
            a, b = iv(*p), iv(*q)
            return idx[(min(a, b), max(a, b))]

        base = ov((1, 1), (2, 1))
        for tm in F:
            pts = [ov(*edge) for edge in tm]
            for u, v in ((base, pts[0]), (base, pts[1]), (pts[0], pts[1])):
                lit = e[(min(u, v), max(u, v))]
                enc.assert_true(lit)
        S.write_dimacs(enc, out)
        print("representative", K, "of", len(reps), ": variables", enc.nv, "clauses", len(enc.clauses))
