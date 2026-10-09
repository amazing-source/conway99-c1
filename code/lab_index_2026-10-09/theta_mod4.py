"""residue of the odd part of Theta when v2(Theta) = 8, and of tau/9 data; random balls as in tau_theta_valuations.py"""
import random, sys, collections
from tau_theta_valuations import bareiss, ball, val
rng = random.Random(int(sys.argv[1])); NB = int(sys.argv[2]); allow3 = len(sys.argv) > 3
c8 = collections.Counter(); call = collections.Counter(); ct = collections.Counter(); n = 0
while n < NB:
    b = ball(rng, True, allow3)
    if b is None: continue
    A, tri, four = b; n += 1
    H = [[(3 if i == j else 0) - A[i][j] for j in range(36)] for i in range(36)]
    tau = bareiss([r[1:] for r in H[1:]])
    th = bareiss([[(4 if i == j else 0) + A[i][j] for j in range(36)] for i in range(36)]) // 7
    v = val(th, 2); odd = th >> v
    call[(v, odd % 8)] += 1
    if v == 8: c8[odd % 4] += 1
    v2 = val(tau, 2); v3 = val(tau, 3); ct[(v2, (tau >> v2) % 8)] += 1
print("balls", n)
print("v2(Theta) = 8: odd part mod 4:", dict(sorted(c8.items())))
print("(v2(Theta), odd part mod 8):", dict(sorted(call.items())))
print("(v2(tau), odd part of tau mod 8):", dict(sorted(ct.items())))
