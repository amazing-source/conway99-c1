"""Histogram of t_c = dim ker Q_c and of chi7(det Q_c) (t = 0) restricted to blocks with NO D-digon (tau and eta share no
edge: no orbit pivots at c) -- the 'all dis' / free-star core (structures' question, 26/09 night).
tau up to Aut(X,pi), eta over all 10395 (weights: each eta counted once per tau class)."""
exec(open('q7_qc_nullity.py', encoding='utf-8').read().split("t0 = time.time()")[0])
from collections import Counter
def det_mod(M):
    M = [r[:] for r in M]; n = len(M); d = 1
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] % P), None)
        if piv is None: return 0
        if piv != c: M[c], M[piv] = M[piv], M[c]; d = -d
        d = d * M[c][c] % P; inv = pow(M[c][c] % P, P-2, P)
        for i in range(c+1, n):
            if M[i][c] % P:
                f = M[i][c]*inv % P; M[i] = [(a - f*b) % P for a, b in zip(M[i], M[c])]
    return d % P
SQ = {1, 2, 4}
hist = Counter(); byq = Counter()
for tau in reps:
    for eta in ALL:
        if any(tau[w] == eta[w] for w in X): continue
        Q = [[(tau[w] == v) - (eta[w] == v) - 2*(pi[w] == v) - (w == v) for v in X] for w in X]
        t = 12 - rank_mod(Q)
        key = t if t else ('0sq' if det_mod(Q) in SQ else '0nsq')
        hist[key] += 1
        ntd = sum(tau[2*d] == 2*d+1 for d in range(6)); ned = sum(eta[2*d] == 2*d+1 for d in range(6))
        byq[(ntd, ned, key)] += 1
print('no-digon blocks, (tau class x eta) counts:', dict(hist))
for k in sorted(byq, key=str): print(k, byq[k])
