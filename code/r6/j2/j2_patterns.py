# J2 model, step 1: all sign patterns a (h on the reps) of the 20 cut labels with V = (5,6,+) (rep e5+e6, a_V = +2).
# Labels (i,j,s), i<j, rep e_i + s e_j; cut = {0,1} | X = {2..6}; balance R^T a = 0 including 2 r_V.
# Also records, per pattern, the positive-rep D7 vectors and the J2 facts that are checkable from a alone.
import itertools, json, numpy as np
cells = [(i, j) for i in range(7) for j in range(i + 1, 7)]
labels = [(c, s) for c in cells for s in (1, -1)]
idx = {L: k for k, L in enumerate(labels)}
cut = [idx[((i, x), s)] for i in (0, 1) for x in range(2, 7) for s in (1, -1)]
R = np.zeros((42, 7), dtype=int)
for k, ((i, j), s) in enumerate(labels): R[k, i] = 1; R[k, j] = s
V = idx[((5, 6), 1)]
pats = []
for signs in itertools.product((1, -1), repeat=20):
    a = np.zeros(42, dtype=int)
    for k, s in zip(cut, signs): a[k] = s
    a[V] = 2
    if np.any(R.T @ a): continue
    pats.append(signs)
print('valid J2 sign patterns (a on 20 cut labels, V fixed at (5,6,+)):', len(pats))
json.dump({'cut': cut, 'V': V, 'patterns': pats}, open('j2_patterns.json', 'w'))
