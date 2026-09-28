# CHECK (exploratory, on structures' 13 sampled survivors; not a proof):
# do the group-constant compressions (6-dim: 1_{G_k}, e_{V_k}) of the odd and even matrices already fail?
import json, numpy as np
d = json.load(open('C:/home/researcher/Desktop/conway99-rank17/r8_data/j1a_v_odd_survivors.json'))
for e in d:
    a = e['a']; g = e['group(W index 1..3, v_k = e_k - e_{k+1 mod 3})']
    Q = e['Q_pairs(rep-rep adjacent in O_c+)']; P = e['P_pairs(rep_u ~ sigma rep_w)']
    labs = sorted(a.keys()) + ['W1', 'W2', 'W3']; ix = {L: i for i, L in enumerate(labs)}; n = 15
    G = np.zeros((n, n))
    for x, y in Q + P: G[ix[x], ix[y]] = G[ix[y], ix[x]] = 1
    for L in a: k = g[L]; G[ix[L], ix['W%d' % k]] = G[ix['W%d' % k], ix[L]] = 1
    for x, y in [('W1', 'W2'), ('W2', 'W3'), ('W1', 'W3')]: G[ix[x], ix[y]] = G[ix[y], ix[x]] = 1
    R = np.zeros((n, 7))
    for L in a:
        K = int(L[1]); s = 1 if L[2] == '+' else -1
        R[ix[L], 0] = a[L]; R[ix[L], K] = a[L] * s
    for k in (1, 2, 3):
        R[ix['W%d' % k], k] = 1; R[ix['W%d' % k], k % 3 + 1] = -1
    av = np.array([1.0] * 12 + [2.0] * 3)
    assert np.allclose(G @ av, 4 * av) and np.allclose(R.T @ av, 0)
    Mo = 12 * np.eye(n) + 4 * G - R @ R.T
    Me = 6 * np.eye(n) - 2 * G - np.abs(R) @ np.abs(R).T + np.ones((n, n))
    Phi = np.zeros((n, 6))
    for L in a: Phi[ix[L], g[L] - 1] = 1
    for k in (1, 2, 3): Phi[ix['W%d' % k], 2 + k] = 1
    co = np.linalg.eigvalsh(Phi.T @ Mo @ Phi); ce = np.linalg.eigvalsh(Phi.T @ Me @ Phi)
    print('group-quotient odd min %.3f   even min %.3f   (full: odd %.3f even %.3f)' % (co[0], ce[0], e['odd_min_eig'], e['even_min_eig']))
    fo = np.linalg.eigvalsh(Mo)[0]; fe = np.linalg.eigvalsh(Me)[0]
    print('      recomputed full: odd %.3f even %.3f' % (fo, fe))
