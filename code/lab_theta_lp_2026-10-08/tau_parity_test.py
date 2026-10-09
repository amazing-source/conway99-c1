"""C1, lab session, 2026-10-09. Is the quadratic character modulo 7 of the number of spanning trees of a near graph G(T)
(the quantity of lemma L23) a function of the parities of the cycle counts of G(T)?
Random layered cubic graphs: three layers of 12 points in 6 mate pairs, three random perfect matchings between layers.
c = number of cross cycles; c01, c12, c20 = numbers of two-layer cycles; F = c + c01 + c12 + c20.
  python tau_parity_test.py [trials]      One process, seconds."""
import random, sys, collections
random.seed(3); TR = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
QR = {1: 1, 2: 1, 4: 1, 3: -1, 5: -1, 6: -1, 0: 0}


def det_mod(M, p):
    M = [r[:] for r in M]; n = len(M); d = 1
    for i in range(n):
        piv = next((r for r in range(i, n) if M[r][i] % p), None)
        if piv is None: return 0
        if piv != i: M[i], M[piv] = M[piv], M[i]; d = -d
        d = d * M[i][i] % p; inv = pow(M[i][i], p - 2, p)
        for r in range(i + 1, n):
            f = M[r][i] * inv % p
            if f: M[r] = [(a - f * b) % p for a, b in zip(M[r], M[i])]
    return d % p


tab = collections.Counter()
for _ in range(TR):
    mate = {}
    for l in range(3):
        for i in range(0, 12, 2): mate[(l, i)] = (l, i + 1); mate[(l, i + 1)] = (l, i)
    nxt = {}                                             # cross neighbour in the next layer, and in the previous one
    prv = {}
    for l in range(3):
        p = list(range(12)); random.shuffle(p)
        for i in range(12): nxt[(l, i)] = ((l + 1) % 3, p[i]); prv[((l + 1) % 3, p[i])] = (l, i)
    pts = [(l, i) for l in range(3) for i in range(12)]; ix = {q: k for k, q in enumerate(pts)}
    L = [[0] * 36 for _ in range(36)]
    for q in pts:
        L[ix[q]][ix[q]] = 3
        for r in (mate[q], nxt[q], prv[q]): L[ix[q]][ix[r]] -= 1
    tau = det_mod([row[:35] for row in L[:35]], 7)
    seen = set(); c = 0
    for q in pts:
        if q[0] == 0 and q not in seen:
            c += 1; z = q
            while z not in seen: seen.add(z); z = nxt[nxt[nxt[z]]]
    two = []
    for l in range(3):                                   # layers l and l+1: mate, cross, mate, cross back
        seen = set(); k = 0
        for i in range(12):
            q = (l, i)
            if q in seen: continue
            k += 1; z = q
            while z not in seen:
                seen.add(z); z1 = mate[z]; seen.add(z1); y = nxt[z1]; y1 = mate[y]; z = prv[y1]
        two.append(k)
    tab[(QR[tau], c % 2, sum(two) % 2)] += 1
print("random layered cubic graphs: (character of tau mod 7, parity of cross cycles, parity of two-layer cycles) -> count")
for k in sorted(tab): print("  ", k, tab[k])
by = collections.Counter()
for (ch, a, b), v in tab.items(): by[(ch, (a + b) % 2)] += v
print("(character, parity of the number of faces F) ->", dict(sorted(by.items())))
