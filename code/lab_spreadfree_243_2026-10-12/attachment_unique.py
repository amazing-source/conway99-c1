"""Lab session, 2026-10-13. The attachment of a folded Hamming third is forced (finite check used in the proof of
NOTE_SPREADFREE.md section 6j): in the graph induced on the block 0..80, non-adjacent pairs have 0 or 2 common
neighbours; the "distance 3" graph (0 common neighbours) is 30-regular and has exactly 12 cliques of size 6 through a
vertex, hence 162 in all; the 12 outside neighbourhoods through vertex 0 in the fifth graph are these 12 cliques.
python -I attachment_unique.py <directory of aut_tools.py> <edge file of the fifth graph>"""
import sys, itertools, collections
sys.path.insert(0, sys.argv[1])
import numpy as np, aut_tools as T
A = T.load(sys.argv[2]); R = range(81); AR = A[:81, :81]
cn = AR @ AR
dist3 = [[(i != j and AR[i, j] == 0 and cn[i, j] == 0) for j in R] for i in R]
print("common neighbours inside the third for non-adjacent pairs:", sorted(collections.Counter(int(cn[i, j]) for i in R for j in R if i < j and AR[i, j] == 0).items()))
nb = [set(j for j in R if dist3[i][j]) for i in R]; print("degree of the distance-3 graph:", sorted(set(len(x) for x in nb)))
# 6-cliques through vertex 0
cl0 = []
def ext(cur, cand):
    if len(cur) == 6: cl0.append(tuple(cur)); return
    for v in sorted(cand):
        if v > cur[-1] or len(cur) == 1: ext(cur + [v], {w for w in cand if w in nb[v] and w > v})
ext([0], set(nb[0]))
print("6-cliques of the distance-3 graph through vertex 0:", len(cl0))
# the blocks of the known attachment through vertex 0
out_nb = [v for v in range(81, 243) if A[0, v]]
blocks0 = [tuple(sorted(int(r) for r in np.nonzero(A[f, :81])[0])) for f in out_nb]
print("blocks of the known attachment through vertex 0: %d, all are 6-cliques of the distance-3 graph: %s" % (len(blocks0), all(b in set(cl0) for b in blocks0)))
# pairs of cliques through 0 meeting in at least 3 points
big = sum(1 for a, b in itertools.combinations(cl0, 2) if len(set(a) & set(b)) >= 3)
print("pairs of cliques through 0 sharing at least 3 points:", big)
