"""q:7 local invariants per C2 free-star cube (mu class = my tau class, labelled by the block-cycle type),
over all eta (C2's tau) that are FREE at c (no block with mu = eta = sigma on it).
For each cube: distribution of (t = dim ker Q_c mod 7, chi_7(det Q_c) if t = 0)."""
exec(open('x36c_q7_qc_nullity.py', encoding='utf-8').read().split("t0 = time.time()")[0])
from collections import Counter
def cube_label(t):
    seen = set(); lens = []
    for x in X:
        if x in seen: continue
        L = 0; y = x; use_pi = True
        while True:
            seen.add(y); L += 1
            y = pi[y] if use_pi else t[y]; use_pi = not use_pi
            if y == x and use_pi: break
        lens.append(L // 2)
    return 'A' + ''.join(str(l) for l in sorted(lens, reverse=True))
def det_mod(M):
    M = [[x % P for x in r] for r in M]; n = len(M); d = 1
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c]), None)
        if piv is None: return 0
        if piv != c: M[c], M[piv] = M[piv], M[c]; d = -d
        d = d * M[c][c] % P; inv = pow(M[c][c], P-2, P)
        for i in range(c+1, n):
            f = M[i][c] * inv % P
            if f: M[i] = [(a - f*b) % P for a, b in zip(M[i], M[c])]
    return d % P
def chi(a): a %= P; return 0 if a == 0 else (1 if pow(a, 3, P) == 1 else -1)
for tau in reps:
    h = Counter(); nfree = 0
    for eta in ALL:
        if any(tau[2*d] == 2*d+1 and eta[2*d] == 2*d+1 for d in range(6)):
            continue   # a sib pair at c (mu = eta = sigma on block d): not free
        nfree += 1
        Q = [[(tau[w] == v) - (eta[w] == v) - 2*(pi[w] == v) - (w == v) for v in X] for w in X]
        dq = det_mod(Q)
        if dq: h[('t=0', 'sq' if chi(dq) == 1 else 'nsq')] += 1
        else: h[('t=%d' % (12 - rank_mod(Q)),)] += 1
    tot = sum(h.values())
    print(cube_label(tau), 'free eta:', nfree, {k: '%.1f%%' % (100*v/tot) for k, v in sorted(h.items())})
