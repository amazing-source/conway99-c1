#!/usr/bin/env python3
"""Finite checks for the K7 partial-results note. Python standard library only.
The 99-vertex fixture is PARTIAL, NOT an SRG and NOT a counterexample to K7.
The mathematical connectivity and conditional bounds are proved in PREUVES.md.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def matmul(A, B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]

def rank(A):
    R = [[Fraction(x) for x in row] for row in A]
    i = 0
    for j in range(len(R[0])):
        k = next((k for k in range(i, len(R)) if R[k][j]), None)
        if k is None:
            continue
        R[i], R[k] = R[k], R[i]
        t = R[i][j]
        R[i] = [x/t for x in R[i]]
        for k in range(i+1, len(R)):
            t = R[k][j]
            if t:
                R[k] = [x-t*y for x,y in zip(R[k], R[i])]
        i += 1
        if i == len(R):
            break
    return i

def matchings(items):
    if not items:
        yield []
        return
    a = items[0]
    for b in items[1:]:
        for tail in matchings([x for x in items if x not in (a,b)]):
            yield [(a,b)] + tail

def main():
    # Check Q^2 = 21Q in the four-dimensional commutative algebra.
    # Basis: I,D,N,J; all rules are consequences of the stated SRG/design equations.
    rules = {(0,0):[1,0,0,0], (0,1):[0,1,0,0], (0,2):[0,0,1,0],
             (0,3):[0,0,0,1], (1,1):[12,-1,-1,2], (1,2):[0,0,-1,8],
             (1,3):[0,0,0,10], (2,2):[0,0,12,32], (2,3):[0,0,0,56],
             (3,3):[0,0,0,77]}
    q=[9,-3,-1,1]
    q2=[sum(q[i]*q[j]*rules[min(i,j),max(i,j)][k]
            for i in range(4) for j in range(4)) for k in range(4)]
    assert q2 == [21*x for x in q]
    # An explicit cubic graph disjoint from the prescribed mate matching.
    edges = [(0,2),(0,3),(1,2),(1,3),(0,4),(1,6),(2,8),(3,10)]
    cycle = [4,6,8,10,12,5,7,9,11,13]
    edges += list(zip(cycle,cycle[1:]+cycle[:1]))
    edges += [(12,7),(13,9),(5,11)]
    edges = sorted({tuple(sorted(e)) for e in edges})
    assert len(edges) == 21
    mates = [(a,a+1) for a in range(0,14,2)]
    G = [[0]*14 for _ in range(14)]
    M = [[0]*14 for _ in range(14)]
    for a,b in edges:
        assert a//2 != b//2
        G[a][b] = G[b][a] = 1
    for a,b in mates:
        M[a][b] = M[b][a] = 1
    assert all(sum(row) == 3 for row in G)
    seen = {0}
    todo = [0]
    while todo:
        a = todo.pop()
        for b in range(14):
            if (G[a][b] or M[a][b]) and b not in seen:
                seen.add(b); todo.append(b)
    assert len(seen) == 14
    n = [[sum(G[a][b] for a in mates[i] for b in mates[j])
          for j in range(7)] for i in range(7)]
    assert all(sum(row) == 6 for row in n)
    assert n[0][1] == 4
    L = [[6*(a==b)-G[a][b]-3*M[a][b] for b in range(14)] for a in range(14)]
    assert rank(L) == 13
    G2M = matmul(matmul(G,G),M)
    GM = matmul(G,M)
    GM2 = matmul(GM,GM)
    ti = sum(G2M[a][a] for a in range(14))
    tii = sum(GM2[a][a] for a in range(14))
    square_sum = sum(n[i][j]**2 for i in range(7) for j in range(i))
    assert square_sum == 21 + ti + Fraction(tii,2)
    # Frame cut identities are identities of this Laplacian, not existence claims.
    for i,j in combinations(range(7),2):
        S = mates[i]+mates[j]
        assert sum(L[a][b] for a in S for b in S) == 12-2*n[i][j]

    # Partial rooted matrix: C=0..21, N(c)=22..35, U=36..98.
    # Unassigned adjacencies are None, never silently treated as zero.
    A = [[None]*99 for _ in range(99)]
    for a in range(99): A[a][a] = 0
    def put(a,b,v):
        assert A[a][b] is None or A[a][b] == v
        A[a][b] = A[b][a] = v
    for a,b in combinations(range(22),2): put(a,b,0)
    pair_to_point = {e: 1+i for i,e in enumerate(edges)}
    other = [(a,b) for a,b in combinations(range(14),2) if not G[a][b] and not M[a][b]]
    assert len(other) == 63
    pair_to_far = {e:36+i for i,e in enumerate(other)}
    labels = dict(pair_to_point); labels.update(pair_to_far)
    for z in range(1,99): put(0,z,int(22 <= z < 36))
    for a,b in combinations(range(14),2): put(22+a,22+b,M[a][b])
    for pair,z in labels.items():
        for a in range(14): put(22+a,z,int(a in pair))
    for a in range(22,36):
        assert all(x is not None for x in A[a])
        assert sum(A[a]) == 14
        assert sum(A[a][:22]) == 4
    assert all(x is not None for x in A[0]) and sum(A[0]) == 14
    def cn_exact(a,b):
        result=0
        for z in range(99):
            x,y=A[a][z],A[b][z]
            if x==0 or y==0: continue
            assert x is not None and y is not None
            result += x*y
        return result
    for z in range(1,99): assert cn_exact(0,z) == 2-A[0][z]
    for a,b in combinations(range(22,36),2):
        assert cn_exact(a,b) == 2-A[a][b]
    Q = [labels[tuple(sorted((a,b)))] for a in mates[0] for b in mates[1]]
    assert len(set(Q)) == 4 and all(1 <= x < 22 for x in Q)
    assert all(A[a][b]==0 for a,b in combinations(Q,2))
    unknown = sum(A[a][b] is None for a,b in combinations(range(99),2))
    assert unknown == 21*63 + 63*62//2 == 3276
    result = {
        'status':'PARTIAL_CONFIGURATION_NOT_COUNTEREXAMPLE',
        'G_edges':edges, 'M_edges':mates, 'quotient_multiplicities':n,
        'rank_local_Gram':13, 'tr_G2M':ti, 'tr_GM2':tii,
        'sum_n_squared':square_sum, 'quadruplet_with_four_C_points':Q,
        'unknown_pairs':unknown,
        'known_pair_tests':{'root_to_all':98,'within_Nc':91},
        'not_imposed':['full 2-(22,4,2) design','Hoffman counts for the other 63 block vertices',
                       'remaining SRG pair equations','completion of unknown edges']}
    saved=json.loads((ROOT/'data/local_fixture.json').read_text())
    # JSON tuples become lists.
    assert saved == json.loads(json.dumps(result))

    # Conditional theorem: on the six pure U vertices, equality of T-neighbours
    # is a matching L disjoint from M. Its quotient by M is necessarily K3.
    L0={frozenset((0,1)),frozenset((2,3)),frozenset((4,5))}
    checked=0
    for P in matchings(list(range(6))):
        if any(frozenset(e) in L0 for e in P): continue
        checked += 1
        for e,f in combinations(P,2):
            assert sum(frozenset((a,b)) in L0 for a in e for b in f) == 1
    assert checked == 8
    print('OK: local algebra, exact rational rank, and defect identity.')
    print('OK: partial 99-vertex fixture; 98+91 exact pair conditions; 3276 UNASSIGNED pairs.')
    print('OK: 8 disjoint-matching cases in the conditional n<=3 proof.')
    print('This verifies finite checks. K7 is neither proved nor refuted by the fixture.')

if __name__ == '__main__':
    main()
