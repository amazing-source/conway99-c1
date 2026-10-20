"""oblr_prep for an EXPLICIT connected line graph (used by adversarial.py): rank 37 (rho = 0), generic (d = 1).
usage: python oblr_prep_gt.py '[s01, s12, s20]' <out.bin>"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oblr_prep import P7, build  # noqa: E402
from ll_test import components, gt_matrix  # noqa: E402
from rank7_line import rank_mod  # noqa: E402

s01, s12, s20 = json.loads(sys.argv[1])
G = gt_matrix(12, s01, s12, s20)
nc, comp = components(G)
d = 36 - rank_mod((3 * np.eye(36, dtype=np.int64) - G) % P7, P7)
assert nc == 1 and d == 1, (nc, d)
build("c1", s01, s12, s20, G, nc, comp, d, 0, 1, sys.argv[2])
