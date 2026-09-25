"""notes/108, step (4) of the defect lemma: for a complete pair P and y in Q_P, the numbers n_R(y) of generic
neighbours of y in the 10 pairs R disjoint from P form an edge weighting of K5 (the 5 classes outside P)
with every vertex sum = 4, n_R <= 1 when R is a complete grid.  Claim: the all-ones weighting is the only
solution iff the incomplete pairs I (as edges of K5) contain no two disjoint edges.  Exhaustive check over
all 1024 subsets I."""
import itertools
V = range(5)
E = list(itertools.combinations(V, 2))
def solutions(I):
    caps = [4 if e in I else 1 for e in E]
    sols = []
    def rec(k, n):
        if k == len(E):
            if all(sum(n[j] for j, e in enumerate(E) if v in e) == 4 for v in V):
                sols.append(tuple(n))
            return
        for val in range(caps[k] + 1):
            n.append(val)
            # prune: partial vertex sums <= 4
            if all(sum(n[j] for j, e in enumerate(E[:k + 1]) if v in e) <= 4 for v in V):
                rec(k + 1, n)
            n.pop()
    rec(0, [])
    return sols
bad = 0
for mask in range(1 << 10):
    I = {E[j] for j in range(10) if mask >> j & 1}
    has_disjoint = any(not set(e) & set(f) for e, f in itertools.combinations(I, 2))
    unique = solutions(I) == [tuple([1] * 10)]
    if unique == has_disjoint:
        bad += 1
print('subsets I where (unique all-ones) != (no two disjoint incomplete edges):', bad, 'of 1024')
