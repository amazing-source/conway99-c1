"""Check relabelling on the actual fixed skeleton (not on invented C1 graphs)."""
from pathlib import Path
import json
import sys
import numpy as np
from coclique_global_boundary import build
from coclique_triangle_canonical import canonicalize,add_canonicalization
from coclique_residual_partition import build as strengthened


def check(folder):
    model,variables,fixed,B,M,edge,products = build()
    rng = np.random.default_rng(17)
    checks = []
    for t in (7,14,61,84):
        A = np.zeros((99,99),dtype=np.int64)
        for u in range(99):
            for v in range(u+1,99):
                A[u,v] = A[v,u] = fixed.get((u,v),int(rng.integers(2)))
        A[37:39,:] = 0
        A[:,37:39] = 0
        A[37,38] = A[38,37] = 1
        z = [v for v in range(63,99) if v != t]
        other = [v for v in list(range(21))+list(range(39,63)) if v != t]
        ne,nf = [t]+z[:3]+other[:6],[t]+z[3:4]+other[6:12]
        for u,neighbours in ((37,ne),(38,nf)):
            for v in neighbours:
                A[u,v] = A[v,u] = 1
        C,permutation = canonicalize(A)
        assert sorted(permutation) == list(range(99))
        assert all(C[u,v] == value for (u,v),value in fixed.items())
        assert C[37,M].sum() <= C[38,M].sum()
        common = np.flatnonzero(C[37]*C[38]).tolist()
        expected = 1 if t < 8 else 20 if t < 21 else 44 if t < 63 else common[0]
        assert common == [expected]
        checks.append(dict(original_common=t,canonical_common=common[0],
                           negative_degrees=[int(C[u,M].sum()) for u in (37,38)]))
    model,B,M,edge,meta = strengthened('r1_1_C13')
    meta.update(add_canonicalization(model,edge))
    assert not model.validate(),model.validate()
    report = dict(check='PASS',samples=checks,model_validation='PASS',
                  scope='Canonical labelling encoder checks on structural skeletons, not examples of C1 graphs')
    (folder/'canonical_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    check(Path(sys.argv[1]))
