import itertools, numpy as np
from beta_form_check import check
pts = []
for v in itertools.product(range(3), repeat=4):
    if any(v):
        f = next(x for x in v if x); inv = pow(f, -1, 3); w = tuple(x * inv % 3 for x in v)
        if w not in pts: pts.append(w)
om = lambda x, y: (x[0]*y[1] - x[1]*y[0] + x[2]*y[3] - x[3]*y[2]) % 3
A = [[1 if (i != j and om(a, b) == 0) else 0 for j, b in enumerate(pts)] for i, a in enumerate(pts)]
print(len(pts), set(map(sum, A)))
check('W(3)=GQ(3,3) srg(40,12,2,4)', A, 2, -4, 3)
