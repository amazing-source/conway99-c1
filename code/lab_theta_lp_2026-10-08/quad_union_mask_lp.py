"""C1, lab session, 2026-10-09. Mask-multiplicity test (the method of Codex's note 222) applied to the union H u H* of the
two kernels of one quadrangle (NOTE 17.83). No rank hypothesis.

For a core U (an induced subgraph on n vertices), every outside vertex x has a mask N(x) n U. A mask m is admissible when
  - two adjacent members have no common neighbour in U (x is then their unique common neighbour) and each has no other
    member as a neighbour; two non-adjacent members have at most one common neighbour in U;
  - a vertex of U outside m has at most two neighbours in m;
  - the two positivity conditions of note 221 hold on U + x (floating test here).
The multiplicities mu_m >= 0 must satisfy: sum = 99 - n; for u in U: sum over masks containing u = 14 - deg_U(u); for
u < v in U: sum over masks containing both = 2 - A_uv - (common neighbours in U). If this linear system has no
non-negative REAL solution, the core cannot occur. The verdict printed here is the verdict of a floating LP solver
(HiGHS): "infeasible" is a NUMERICAL verdict until a rational Farkas certificate is checked.

  control : python quad_union_mask_lp.py <Codex data folder> control
            -> the same test on the 14-vertex kernels of the 310 types of note 222, compared with Codex's exact statuses
  run     : python quad_union_mask_lp.py <Codex data folder> run <output json> <time limit s> <type> [<type> ...]
            -> every completion of H u H* of each listed type, with the verdict of the test on the union
One process, below 500 MB."""
import sys, os, json, time, collections
import numpy as np
from scipy.optimize import linprog
DATA = sys.argv[1]; MODE = sys.argv[2]; _argv = sys.argv[:]
sys.argv = [_argv[0], DATA, "unused.json", "0", "0", "0", "100000"]
import quad_partner_kernels as q
sys.argv = _argv

def masks_of(adj, n):
    cn = [[bin(adj[u] & adj[v]).count("1") for v in range(n)] for u in range(n)]
    out = []
    def rec(u, m, cnt):
        if u == n:
            out.append(m); return
        rec(u + 1, m, cnt)
        au = adj[u]
        if cnt[u] > 1: return                              # u would have two neighbours in the mask
        for w in range(u):
            if m >> w & 1:
                if au >> w & 1:
                    if cn[u][w] != 0 or cnt[w] > 1 or cnt[u] > 1: return
                elif cn[u][w] > 1: return
        c2 = cnt[:]
        for w in range(n):
            if au >> w & 1:
                c2[w] += 1
                if c2[w] > 2 or (c2[w] > 1 and (m >> w & 1)): return
        rec(u + 1, m | 1 << u, c2)
    rec(0, 0, [0] * n)
    good = []
    for m in out:
        cnt = [bin(adj[w] & m).count("1") for w in range(n)]
        if any(cnt[w] > (1 if m >> w & 1 else 2) for w in range(n)): continue
        a = adj[:] + [m]
        for w in range(n):
            if m >> w & 1: a[w] |= 1 << n
        if q.positive(a, n + 1): good.append(m)
        for w in range(n): a[w] &= ~(1 << n)
    return good

def lp_verdict(adj, n):
    masks = masks_of(adj, n)
    rows = []; rhs = []
    rows.append([1.0] * len(masks)); rhs.append(99 - n)
    for u in range(n):
        rows.append([1.0 if m >> u & 1 else 0.0 for m in masks]); rhs.append(14 - bin(adj[u]).count("1"))
    for u in range(n):
        for v in range(u + 1, n):
            need = 2 - (adj[u] >> v & 1) - bin(adj[u] & adj[v]).count("1")
            if need < 0: return "invalid core", len(masks)
            rows.append([1.0 if (m >> u & 1) and (m >> v & 1) else 0.0 for m in masks]); rhs.append(need)
    if not masks: return "infeasible", 0
    r = linprog(np.zeros(len(masks)), A_eq=np.array(rows), b_eq=np.array(rhs, float), bounds=(0, None), method="highs")
    return ("feasible" if r.status == 0 else "infeasible" if r.status == 2 else "solver status %d" % r.status), len(masks)

if MODE == "control":
    ext = json.load(open(os.path.join(DATA, "codex_twisted_prism_extension.json")))["results"]
    t0 = time.time(); agree = collections.Counter(); nm = []
    for r in ext:
        v, k = lp_verdict(q.base_adj(r["bits"]), 14)
        codex = "infeasible" if r["status"] == "excluded_exact" else "feasible"
        agree[(codex, v)] += 1
        if k != r["masks_after_spectral"]: nm.append((r["bits"], k, r["masks_after_spectral"]))
    print("control on the 310 kernels of note 222, (Codex's exact status, verdict here):", sorted(agree.items()))
    print("kernels whose number of admissible masks differs from Codex's: %d %s   [%.0f s]" % (len(nm), nm[:5], time.time() - t0))
else:
    OUT = sys.argv[3]; TLIM = float(sys.argv[4]); types = [int(x) for x in sys.argv[5:]]
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    t0 = time.time()
    for b in types:
        if str(b) in res and res[str(b)].get("complete"): continue
        every = []; q.PER_TYPE = 10 ** 6
        q.partners(b, every=every)
        rec = res.get(str(b), {"completions": len(every), "done": 0, "feasible": 0, "infeasible": 0, "other": 0, "feasible_partners": [], "first_feasible": None})
        for i in range(rec["done"], len(every)):
            if time.time() - t0 > TLIM: break
            c, a = every[i]; v, k = lp_verdict(a, len(a))
            rec["done"] += 1
            if v == "feasible":
                rec["feasible"] += 1
                if q.canon(c) not in rec["feasible_partners"]: rec["feasible_partners"].append(q.canon(c))
                if rec["first_feasible"] is None: rec["first_feasible"] = {"partner_labelled": c, "adjacency_bitmasks": a, "masks": k}
            elif v == "infeasible": rec["infeasible"] += 1
            else: rec["other"] += 1
        rec["complete"] = rec["done"] == len(every); res[str(b)] = rec
        json.dump(res, open(OUT, "w"))
        print("type %d: completions %d, tested %d: feasible %d, infeasible (numerical) %d, other %d; partner types still feasible %s"
              % (b, rec["completions"], rec["done"], rec["feasible"], rec["infeasible"], rec["other"], sorted(rec["feasible_partners"])), flush=True)
        if time.time() - t0 > TLIM: break
    print("elapsed %.0f s" % (time.time() - t0))
