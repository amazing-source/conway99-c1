"""Eliminate the neighbourhood of a c = 1 line (exploration, LAB 17/10/2026).
Claim to prove: if a line l = {o,0,1} of a Conway graph has c(l) = 1, then the six other lines through o have c = 1.
Exact global model (Codex's build_global: Gamma on the 84 labels of o, srg equations exact) + c(l) = 1 + E3 on the 21
rectangles.  A node assigns to some lines j in 1..6 a status:
  'c1'      : M_j connected (one clause per cut of the six rectangles at j);
  block B   : the component of Q_{0j} at line j is B (0 in B, the other entries are line indices k, rectangle Q_{jk});
              zero cut at line j around B, and T x = 0 EXACTLY for x = 1_{Q_j(B)} (x^t T x = cut = 0, T = 7 Pi_K >= 0):
              sum_{q in Q_j(B)} Gamma_rq = 3 x_r - (K x)_r for every label r.
Tree (exhaustive): by symmetry the line with c >= 2 is line 1; the root children are 1:B for |B| = 2..5 (four, up to S5).
An UNKNOWN node is split on its first unassigned line j: j:c1 or j:B for every admissible block B.  Nodes are
canonicalised under the permutations of lines 1..6 (identical sub-problems are run once).  INFEASIBLE = closed.
A leaf with all six lines assigned and still UNKNOWN is a survivor.  The all-'c1' configuration (the core) is NOT part
of this tree.
usage: python c1_nbhd_tree.py <state.json> <seconds per node> <wall budget seconds>"""
import itertools
import json
import os
import sys
import time

from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CODEX = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-asymmetry-audit\code\codex"
sys.path.insert(0, CODEX)
from conway_global_cover import build_global  # noqa: E402
from c1_global_list import k8  # noqa: E402

LINES = list(range(1, 7))
PERMS = list(itertools.permutations(LINES))


def all_blocks(j):
    others = [k for k in LINES if k != j]
    return [(0,) + sub for size in range(1, 5) for sub in itertools.combinations(others, size)]


def canon(assign):
    """assign: dict line -> 'c1' or tuple block (with 0 and other line indices). Canonical form under S6 on lines."""
    best = None
    for p in PERMS:
        f = {0: 0}
        for a, b in zip(LINES, p):
            f[a] = b
        img = []
        for j, v in assign.items():
            if v == "c1":
                img.append((f[j], (-1,)))
            else:
                img.append((f[j], tuple(sorted(f[t] for t in v))))
        img = tuple(sorted(img))
        if best is None or img < best:
            best = img
    return best


def key_of(assign):
    return json.dumps(canon(assign))


def build(assign):
    model, labels, graph, _, _ = build_global(normalize_star=False)
    n = len(labels)
    index = {p: i for i, p in enumerate(labels)}
    lab = lambda a, b: index[tuple(sorted((a, b)))]
    pairs = [(2 * j, 2 * j + 1) for j in range(7)]
    rect = {}
    for (i, li), (j, lj) in itertools.combinations(enumerate(pairs), 2):
        q = [lab(a, b) for a in li for b in lj]
        rect[(i, j)] = rect[(j, i)] = q
        model.Add(sum(graph[p][r] for p, r in itertools.combinations(q, 2)) != 3)

    def connected(j):
        Qj = [rect[(j, k)] for k in range(7) if k != j]
        for size in range(1, 6):
            for sub in itertools.combinations(range(6), size):
                if 0 not in sub:
                    continue
                ins = [p for k in sub for p in Qj[k]]
                out = [p for k in range(6) if k not in sub for p in Qj[k]]
                model.AddBoolOr([graph[p][r] for p in ins for r in out])

    connected(0)
    for j, v in assign.items():
        if v == "c1":
            connected(j)
            continue
        inside = set(p for k in v for p in rect[(j, k)])
        rootj = set(p for k in range(7) if k != j for p in rect[(j, k)])
        for p in inside:
            for r in rootj - inside:
                model.Add(graph[p][r] == 0)
        for r in range(n):
            s = sum(k8(labels[r], labels[q]) for q in inside)
            val = 3 * (1 if r in inside else 0) - (s // 8 if s % 8 == 0 else 10 ** 6)
            if s % 8 or val < 0:
                model.Add(graph[0][1] == 0)
                model.Add(graph[0][1] == 1)
                return model
            model.Add(sum(graph[r][q] for q in inside if q != r) == val)
    return model


def solve(model, secs):
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 1
    sv.parameters.max_time_in_seconds = secs
    sv.parameters.cp_model_probing_level = 0
    sv.parameters.linearization_level = 0
    sv.parameters.symmetry_level = 0
    st = sv.Solve(model)
    name = sv.StatusName(st)
    if name in ("OPTIMAL", "FEASIBLE"):
        return "FEASIBLE", sv
    return name, sv


def main():
    statef, secs, budget = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    if os.path.exists(statef):
        state = json.load(open(statef))
    else:
        roots = [{"1": [0] + list(range(2, 2 + k))} for k in range(1, 5)]
        state = {"queue": roots, "done": {}}
    t0 = time.time()
    while state["queue"] and time.time() - t0 < budget - secs - 10:
        raw = state["queue"].pop(0)
        assign = {int(j): ("c1" if v == "c1" else tuple(v)) for j, v in raw.items()}
        key = key_of(assign)
        if key in state["done"]:
            continue
        tb = time.time()
        model = build(assign)
        status, sv = solve(model, secs)
        rec = {"assign": raw, "status": status, "seconds": round(time.time() - tb, 1)}
        state["done"][key] = rec
        if status == "UNKNOWN":
            free = [j for j in LINES if j not in assign]
            if free:
                j = free[0]
                kids = [dict(raw, **{str(j): "c1"})] + [dict(raw, **{str(j): list(B)}) for B in all_blocks(j)]
                seenk = set()
                for kd in kids:
                    a2 = {int(x): ("c1" if v == "c1" else tuple(v)) for x, v in kd.items()}
                    k2 = key_of(a2)
                    if k2 in state["done"] or k2 in seenk:
                        continue
                    seenk.add(k2)
                    state["queue"].append(kd)
                rec["children"] = len(seenk)
            else:
                rec["leaf"] = True
        if status == "FEASIBLE":
            rec["note"] = "a Conway graph would exist: check!"
        json.dump(state, open(statef, "w"))
        print("%s -> %s (%.0f s)%s" % (raw, status, rec["seconds"],
                                         (" +%d children" % rec["children"]) if "children" in rec else ""), flush=True)
    tally = {}
    for r in state["done"].values():
        tally[r["status"]] = tally.get(r["status"], 0) + 1
    print("DONE %d nodes: %s ; queue %d" % (len(state["done"]), tally, len(state["queue"])), flush=True)


if __name__ == "__main__":
    main()
