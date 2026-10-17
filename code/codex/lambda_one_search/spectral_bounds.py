"""Numerical necessary conditions for an SRG completion.

Each nonprincipal spectral projector is positive semidefinite. Its known
rows determine a Schur-complement Gram matrix on the remaining vertices.
Nonnegative diagonal and the 2x2 minors constrain every missing edge.
Conservative floating tolerances are used for constructive pruning only;
these checks are not exported as an exact nonexistence certificate.
"""
import math
import numpy as np


def missing_edge_bounds(A, R, F, k, lam, mu, tolerance=1e-7):
    n=len(A)
    gap=math.sqrt((lam-mu)**2+4*(k-mu))
    r=((lam-mu)+gap)/2
    s=((lam-mu)-gap)/2
    possible0=np.ones((len(F),len(F)),dtype=bool)
    possible1=possible0.copy()
    for other, own in [(r,s),(s,r)]:
        divisor=other-own
        constant=(k-other)/n
        diagonal=(other+constant)/divisor
        PR=(other*np.eye(len(R))-A[np.ix_(R,R)]+constant)/divisor
        D=(-A[np.ix_(R,F)]+constant)/divisor
        values,vectors=np.linalg.eigh(PR)
        if values.min() < -tolerance:
            return None
        positive=values>tolerance
        if (~positive).any() and np.max(np.abs(vectors[:,~positive].T@D),initial=0)>tolerance:
            return None
        Y=(vectors[:,positive].T@D)/np.sqrt(values[positive])[:,None]
        known=Y.T@Y
        residual=diagonal-np.diag(known)
        if residual.min() < -tolerance:
            return None
        bound=np.sqrt(np.maximum(residual,0)[:,None]*np.maximum(residual,0)[None,:])+tolerance
        possible0 &= np.abs(constant/divisor-known)<=bound
        possible1 &= np.abs((constant-1)/divisor-known)<=bound
    np.fill_diagonal(possible0,True)
    np.fill_diagonal(possible1,False)
    if not (possible0|possible1).all():
        return None
    return possible0,possible1
