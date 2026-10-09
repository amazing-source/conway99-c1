# P3/N25 register for the rank-43 integer design search

Exported by Codex on 2026-10-09, in response to LAP's request relayed
in bridge message 508. Source research snapshot: `ee50cd2`, notes 245–246.

- `supports_all_6899.jsonl`: all 6,899 supports in the finite register,
  before the spectral and local matching filters.
- `supports_open_4581.jsonl`: the 4,581 supports still open after those
  filters. Use this file for the proposed integer design pilot.
- `manifest.json`: sizes, SHA-256 hashes, counts and encoding.
- The two accompanying notes state the reductions and their scope.

The initial register already uses the analytic forest reductions and
the original delta>=2 inequality. “All” refers to that register, not
to arbitrary graphs on 28 vertices. IDs are stable across both files
and match the research records. No remaining support is claimed to
extend to a SRG. S0 remains open.

## Encoding

Files are UTF-8 JSON Lines with LF endings, one object per support.
Vertices are the integers 0 through 27. In every record:

    P = [0, 1, 2]
    N = [3, 4, ..., 27]

`edges` lists all 36 edges as pairs `[u,v]`, with `u<v`. The graph is
simple and undirected. P is independent, P--N has 24 edges, and N has
12 edges. All unlisted pairs are nonedges.

`labels_N[i]` is the bit mask of the positive neighbours of vertex
`3+i`: bit p corresponds to positive vertex p. For example mask 5
means adjacency to vertices 0 and 2. This field is redundant with
the explicit edges and is provided to retain the original labels.

`delta` counts N--N edges whose unique triangle in the full SRG must
have its third vertex outside the support. `star` is 0 or 1 and counts
K1,3 components of N. `path_counts[l-1]` counts components with l edges,
for l=1,...,6. `isolates` counts isolated vertices of N; `degree2`
counts degree-two vertices of N. These are support-graph quantities.

Status counts in the full file:

| Status | Number |
|---|---:|
| open | 4581 |
| excluded_spectral | 1469 |
| excluded_delta2 | 85 |
| excluded_local_matching | 764 |

The 85 delta2 exclusions were originally certified at the LP boundary.
The later per-positive matching theorem also proves delta>=3 directly.
All records in the open file have status `open`. Their counts for
delta=3,...,9 are 209,496,914,1155,1054,596,157.

## Load a support

```python
import json
from pathlib import Path

folder = Path("data/p3_n25_register")
with (folder / "supports_open_4581.jsonl").open(encoding="utf-8") as f:
    supports = [json.loads(line) for line in f]
row = next(s for s in supports if s["id"] == 4)
A = [[0] * 28 for _ in range(28)]
for u, v in row["edges"]:
    A[u][v] = A[v][u] = 1
```

## Answer about the integer design stage

Codex has **not run an exact integer design search on any support**.
Its previous searches used fractional multiplicities of outside
neighbourhood masks, or direct spectral certificates. Some LP
infeasibilities have integer Farkas certificates; that is not an
integer-design solver run.

For support ID 4, delta=3, the fractional boundary model is numerically
feasible, with maximum equality residual 2.714e-13. The complete
command took about 2.4 seconds on the local lab PC. It did not enforce
the pairwise intersection bound between selected outside blocks.

The next stage described by LAP therefore adds a substantive constraint.
No duplicate integer search is being launched by Codex.

## Compact exact formulation of the intersection bound

For admissible outside masks B, use nonnegative integer variables x_B.
All masks have size at least four. The condition that two selected
blocks share at most two points is exactly imposed by

    sum_{B containing T} x_B <= 1

for each three-subset T of the 28 support vertices. There are at most
binom(28,3)=3276 such inequalities. They also imply x_B<=1 because
every B contains a three-subset. This is equivalent to all pairwise
block-conflict constraints, and avoids explicitly listing every
incompatible pair of candidate masks.

The other rows are the proposed degree, pair-cover and total-71-block
equalities. Any search result remains a result on the necessary
outside design until adjacency among its 71 vertices is handled.
