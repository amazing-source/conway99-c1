"""Single-block identity scan (C1, 27/09).  For a block type (mu, tau) at c, any label set S (slots counted with
multiplicity: a non-pivot label is the secant centre of exactly one quadruple) and any block p != c:
    a3 + 3 a4 + sum_{Q in S_p} (k_Q - 1)+ + #{Q not in S_p : k_Q = 0} = slack(S, p) := 20 - 10|S| + Lambda(S) + C_p(S),
with k_Q = #slots of Q in S, Lambda(S) = sum_{b<d in S} ([non-mu] + K3[b,d]) + sum_{b in S} K3[b,b]/2 and
C_p(S) = sum_{b in S} (K2[p+,b] + K2[p-,b]).  It uses only (i), (ii) summed over p, and (iii) (notes/134 s.6-7);
anchored Sp (slack 1 - [digon]) and twisted S3 (slack 3) are special cases.  A negative slack kills the type.
Writes, for every class of classes_t_ge(0), all (p, S, slack) with slack <= SMAX.
Usage: python ident_scan.py OUT.json [SMAX]"""
import sys, json
import numpy as np
sys.path.insert(0, r'C:/home/researcher/Desktop/c99_structures_lab/involution')
from iota_design import K2K3
from q7_g16_test import classes_t_ge

L = range(12)
X = np.array([[(s >> b) & 1 for b in L] for s in range(1, 4096)], dtype=np.int64)
SIZE = X.sum(1)


def slacks(mu, tau):
    K2, K3 = K2K3(mu, tau)
    Lm = np.zeros((12, 12), dtype=np.int64)
    for b in L:
        for d in L:
            Lm[b, d] = ((1 if mu[b] != d else 0) + K3[b, d]) if b != d else K3[b, b] // 2
    Lam = (((X @ Lm) * X).sum(1) + X @ np.diag(Lm)) // 2
    Cm = np.array([[K2[2 * p, b] + K2[2 * p + 1, b] for b in L] for p in range(6)])
    return 20 - 10 * SIZE[:, None] + Lam[:, None] + X @ Cm.T


if __name__ == '__main__':
    smax = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    out = []
    for (mu, tau, t, osz) in classes_t_ge(0):
        sl = slacks(mu, tau)
        idents = [[int(p), [b for b in L if X[si, b]], int(sl[si, p])] for (si, p) in zip(*np.nonzero(sl <= smax))]
        out.append({'mu': list(map(int, mu)), 'tau': list(map(int, tau)), 't': int(t), 'min_slack': int(sl.min()),
                    'idents': idents})
    json.dump({'smax': smax, 'types': out}, open(sys.argv[1], 'w'))
    print('classes', len(out), 'with an identity of slack <=', smax, ':', sum(1 for o in out if o['idents']),
          '| negative slack:', sum(1 for o in out if o['min_slack'] < 0))
