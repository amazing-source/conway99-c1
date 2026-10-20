"""Cross-check of the vertex block H (-4 side, real) and Sigma (mod 7) on the archive's 331 four-star objects
(work/stars_rank_2026-10-14/rank30_psd_objects_2026-10-15.json: T, U >= 0, rank T = 30).  Prints, per object, the
archive's rank / rank7 and the values computed here.  usage: python rank30_objects_test.py <json>"""
import json
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, ".")
from borne_rang_vertex_block import local_H, rank_mod, sigma_mod7  # noqa: E402

d = json.load(open(sys.argv[1]))
labels = [tuple(l) for l in d["labels"]]
mate = lambda i: i ^ 1
m = len(labels)
stats = Counter()
agree = 0
rows = []
for x in d["structures"]:
    A = np.zeros((m, m))
    for i, j in json.loads(x["edges"]) if isinstance(x["edges"], str) else x["edges"]:
        A[i, j] = A[j, i] = 1
    H, t = local_H(labels, mate, A, 14)
    ev = np.linalg.eigvalsh(H)
    rk = int((np.abs(ev) > 1e-7).sum())
    r7 = rank_mod(sigma_mod7(labels, mate, A.astype(np.int64)), 7)
    psd = ev.min() > -1e-7 and ev.max() < t + 1e-7
    agree += (str(r7) == str(x["rank7"]))
    stats[(rk, r7, psd, x["rank"], x["rank7"])] += 1
for k, v in sorted(stats.items()):
    print("H rank %d, Sigma 7-rank %d, H in [0,7]: %s | archive rank %s rank7 %s : %d objects" % (k + (v,)))
print("objects: %d, Sigma 7-rank equal to archive rank7: %d; with 7-rank <= 28: %d"
      % (len(d["structures"]), agree, sum(v for k, v in stats.items() if k[1] <= 28)))
