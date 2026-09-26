# Profile (4,4,4) of G(L) at P=0, S=0: on one part X = A u B = {a, abar, b, bbar} (labels 0,1 | 2,3):
# tau_u, tau_ubar: perfect matchings A <-> B (no loops); sigma: X -> X with sigma(A) = B, sigma(B) = A
# (no fixed point, no sigma(v) = vbar); condition (c): tau_u and sigma^-1 tau_ubar sigma edge-disjoint.
# For each label v: r_v (second common neighbour of {u,v},{ubar,v}) lies in P_u iff sigma(tau_u(v)) = v,
# in P_ubar iff tau_ubar(v) = sigma(v).  Claim: in every admissible configuration, every v has r_v in P_u u P_ubar.
import itertools
A, B = [0, 1], [2, 3]
mate = {0: 1, 1: 0, 2: 3, 3: 2}
def matchings():
    out = []
    for p in itertools.permutations(B):
        t = {}
        for a, b in zip(A, p):
            t[a], t[b] = b, a
        out.append(t)
    return out
cnt = 0; bad = 0
for tu in matchings():
    for tub in matchings():
        for sA in itertools.permutations(B):
            for sB in itertools.permutations(A):
                s = {A[0]: sA[0], A[1]: sA[1], B[0]: sB[0], B[1]: sB[1]}
                if any(s[v] == v or s[v] == mate[v] for v in s): continue
                sinv = {w: v for v, w in s.items()}
                conj = {v: sinv[tub[s[v]]] for v in s}       # sigma^-1 tau_ubar sigma
                if any(conj[v] == tu[v] for v in s): continue  # condition (c)
                cnt += 1
                for v in s:
                    inPu = s[tu[v]] == v
                    inPub = tub[v] == s[v]
                    if not (inPu or inPub): bad += 1
print('admissible local configurations on one part:', cnt, ' labels with r_v in F (should be 0):', bad)
