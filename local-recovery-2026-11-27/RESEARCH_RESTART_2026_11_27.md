# Global defect support: bridge obstruction

This work resumes research at the user's express request. It uses the corrected defining identities in the November3 journal. No maximal-triangle or uniform-alpha hypothesis.

At each vertex x of a putative SRG(99,14,1,2), the seven paired neighbours define21 rectangles F. Their defect columns satisfy sum_{j!=i}H_ij=0, and ||H_F||²=56-14e(F). A nonzero defect column has28<=||H_F||²<=56, using E3 (a non-grid rectangle has at most two edges).

Define D on the seven indices by ij in E(D) iff H_ij is nonzero.

**Proposition. D has no bridges.** First, D has no vertex of degree1, by the sum relation. If uv is a bridge, both sides of D-uv have at least three vertices: a side of size1 gives a leaf, and a side of size2 also has a nonboundary leaf. Since there are only seven indices, at least one side has exactly three vertices a,b,c. The two vertices other than the bridge endpoint a must each have degree at least2, so that side is a triangle. Its equations give H_ab=H_ac=-H_bc, and H_uv=-2H_ab. Thus ||H_uv||²=4||H_ab||²>=112, contradicting the universal upper bound56. This also handles isolated indices elsewhere.

More generally a triangle joined to its complement by a single defect edge is impossible regardless of the total number of indices, under the same norm ratio bound. A cut identity explains the factor2: for a vertex set S, sum of columns on its edge boundary equals minus twice the sum of its internal edge columns.

This is a universal restriction at every root, not a claim that every root has a maximal triangle. It excludes all bridged defect supports. Novelty relative to every historical note is not established. No conclusion about all surviving supports or the global existence question follows yet.

`defect_supports.py` enumerates all unlabelled seven-vertex graphs, checks unsigned-incidence kernel support and the bridge restriction, and writes a complete list of surviving support representatives. Its kernel test is exact graph theory: rank of the unsigned incidence matrix is n minus the number of bipartite connected components; deleting any edge must preserve rank if a nonzero dependence uses that edge. This enumeration is a coverage catalogue of supports, not of graph completions.

Next target: extend the cut argument to2-edge boundaries, where the sum of two columns is twice an internal sum. Unlike the bridge case, cancellation is possible; it requires the actual mixed inner products or coordinate bounds, not only individual norms.

## Two-edge cut: triangle with distinct exit vertices

Suppose a triangle abc in D has exactly two edges to its complement, one at a and one at b. Write their columns p,q. The relation at c gives H_ac=u=-H_bc. With v=H_ab the other relations give p=-v-u and q=-v+u. Therefore ||p||²+||q||²=2||u||²+2||v||². Both internal columns have norm at least28, both exit columns at most56, so equality is forced throughout: ||u||²=||v||²=28, ||p||²=||q||²=56, and <u,v>=0. The three internal rectangles each have exactly two edges; the two exit rectangles have zero edges. This is another universal implication and forces both numerical norm types and an orthogonality constraint. It does not apply when the two exits share a triangle vertex, or when the three-vertex side has extra exits.

Enumeration outcome:1044 unlabelled seven-index graphs;511 nonempty supports pass the exact unsigned-incidence kernel condition; the bridge argument removes5, leaving506 necessary supports before already-known small-support exclusions and all coordinate constraints. This is not506 full graph candidates. In particular the surviving4-edge square is already excluded by the November3 proof; no novelty is claimed for that case.
