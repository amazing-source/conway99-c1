# Ranks of the odd (12I+4G-RR^T) and even (6I-2G-|R||R|^T+J) support Grams on the survivors (exploratory).
import numpy as np
from collections import Counter
exec(open('postfilter.py').read().split('recs = [tuple')[0])
recs = [tuple(map(int, l.split())) for l in open('vertex_even_left.txt')]
I = np.eye(15); J = np.ones((15, 15)); ro = Counter(); re = Counter(); both = Counter()
for (b, q, p1, p2, kind) in recs:
    alpha, g, ed = config(b, q, p1, p2)
    R, G = mats(alpha, g, ed); Ra = np.abs(R)
    wo = np.linalg.eigvalsh(12 * I + 4 * G - R @ R.T); we = np.linalg.eigvalsh(6 * I - 2 * G - Ra @ Ra.T + J)
    no = int(np.sum(np.abs(wo) < 1e-7)); ne = int(np.sum(np.abs(we) < 1e-7))
    ro[15 - no] += 1; re[15 - ne] += 1; both[(15 - no, 15 - ne)] += 1
print('odd rank histogram ', sorted(ro.items()))
print('even rank histogram', sorted(re.items()))
print('(odd, even) ranks  ', both.most_common())
