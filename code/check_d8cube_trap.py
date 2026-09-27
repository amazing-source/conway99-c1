"""Finish line (C), C1 27/09: re-verification of Sol's D8^3 exclusion.  All 135 Lagrangian gluings of (D8*/D8)^3; keep the
odd unimodular ones with min >= 2 and root system exactly D8^3 (no glue word of minimal norm 1 or 2); check that each has a
component whose norm-3 classes are all vectorial (0 or v), so that its 8 axes (norm 1 < 8/7) are integral on every norm-3
vector, hence on the 42 u, hence lie in N-perp (dim 2): contradiction.  Output: 135 / 37 norm-1 / 58 extra roots / 8 even /
32 kept, 0 without a trap component."""
import itertools
CLS = {(0, 0): '0', (1, 0): 's', (0, 1): 'c', (1, 1): 'v'}
MIN = {'0': 0, 'v': 1, 's': 2, 'c': 2}


def comp(X, i): return CLS[X[2 * i:2 * i + 2]]


def b1(a, b): return 0 if a == '0' or b == '0' or a == b else 1          # 2*b(x,y) mod 2 on D8*/D8


def B(X, Y): return sum(b1(comp(X, i), comp(Y, i)) for i in range(3)) % 2


def span(gens):
    S = {(0,) * 6}
    for g in gens:
        S |= {tuple((a + b) % 2 for a, b in zip(s, g)) for s in S}
    return S


if __name__ == '__main__':
    vecs = [v for v in itertools.product((0, 1), repeat=6) if any(v)]
    lag = {frozenset(span(g)) for g in itertools.combinations(vecs, 3)
           if len(span(g)) == 8 and all(B(x, y) == 0 for x in span(g) for y in span(g))}
    st = dict(total=len(lag), norm1=0, extra_roots=0, even=0, kept=0, no_trap=0)
    for H in lag:
        words = [w for w in H if any(w)]
        mn = [sum(MIN[comp(w, i)] for i in range(3)) for w in words]
        if 1 in mn: st['norm1'] += 1; continue
        if 2 in mn: st['extra_roots'] += 1; continue
        if not any(sum(comp(w, i) == 'v' for i in range(3)) % 2 for w in words): st['even'] += 1; continue
        st['kept'] += 1
        n3 = [w for w, m in zip(words, mn) if m == 3]
        if not any(all(comp(w, i) in '0v' for w in n3) for i in range(3)): st['no_trap'] += 1
    print(st)
