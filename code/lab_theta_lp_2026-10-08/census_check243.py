"""C1, lab session, 2026-10-08. Independent test of Codex's parametrised census (its note 184, packet at ba41e4a) on a REAL
graph srg(v,k,1,2): bvls243, twin243_switched (or the rook's graph with the (9,4) packet).

  python -I census_check243.py <packet json> rook|<edge file> [seconds] [BF HF F8] [save=<file>] [load=<file>] [orders=9] [measure]
Options: save / load the measured parameters (JSON) so that the measurement and the type checks can be two bounded runs;
orders=a,b restricts the type checks to those orders; "measure" stops after the measurement.

The packet is read as data only (JSON; nothing in it is executed). For the last stage, the parameters (P, H and the
dense 8-vertex invariants) are MEASURED in the real graph by an induced-embedding search written here; then every type of
every stage whose predicted number of embeddings is small enough is counted by the same search and compared with the
packet's affine formula evaluated at the measured parameters. Only connected types can be counted this way; the sparse and
the disconnected ones are skipped and reported as such. The three family counts (bowtie or house minus a far edge, far
pairs of 4-sets with 4 edges) are compared with the brute-force values of testbeds.py given on the command line.
One process; memory below 300 MB; the search stops opening new types after <seconds> (default 200)."""
import sys, json, time
from fractions import Fraction as Fr


def load(arg):
    if arg == "rook":
        V = [(i, j) for i in range(3) for j in range(3)]; E = [(a, b) for a in range(9) for b in range(a + 1, 9) if (V[a][0] == V[b][0]) != (V[a][1] == V[b][1])]
    else: E = [tuple(int(x) for x in l.split()[:2]) for l in open(arg) if l.strip()]
    n = 1 + max(max(e) for e in E); mask = [0] * n
    for a, b in E: mask[a] |= 1 << b; mask[b] |= 1 << a
    k = bin(mask[0]).count("1"); assert all(bin(m).count("1") == k for m in mask)
    for a in range(n):
        for b in range(a + 1, n): assert bin(mask[a] & mask[b]).count("1") == (1 if mask[a] >> b & 1 else 2)
    return n, k, mask


def embeddings(rows, hmask, hn):
    """number of injective maps of the pattern (list of adjacency bitmasks) into the host that are induced embeddings."""
    m = len(rows); deg = [bin(r).count("1") for r in rows]; order = [max(range(m), key=lambda i: deg[i])]; placed = 1 << order[0]
    while len(order) < m:
        best = max((i for i in range(m) if not placed >> i & 1), key=lambda i: (bin(rows[i] & placed).count("1"), deg[i]))
        if not rows[best] & placed: return None                           # disconnected pattern: not handled
        order.append(best); placed |= 1 << best
    nb = [[j for j in range(t) if rows[order[t]] >> order[j] & 1] for t in range(m)]
    nn = [[j for j in range(t) if not rows[order[t]] >> order[j] & 1] for t in range(m)]
    full = (1 << hn) - 1; img = [0] * m; cnt = 0
    def rec(t, used):
        nonlocal cnt
        cand = full
        for j in nb[t]: cand &= hmask[img[j]]
        cand &= ~used
        for j in nn[t]: cand &= ~hmask[img[j]]
        if t == m - 1: cnt += bin(cand).count("1"); return
        while cand:
            low = cand & -cand; cand ^= low; img[t] = low.bit_length() - 1; rec(t + 1, used | low)
    rec(0, 0); return cnt


def main():
    opts = dict(a.split("=", 1) for a in sys.argv[3:] if "=" in a); flags = [a for a in sys.argv[3:] if "=" not in a]
    nums = [a for a in flags if a.replace(".", "").isdigit()]; sys.argv = sys.argv[:3] + nums
    D = json.load(open(sys.argv[1])); hn, hk, hmask = load(sys.argv[2]); budget = float(sys.argv[3]) if len(sys.argv) > 3 else 200.0
    only = [int(x) for x in opts["orders"].split(",")] if "orders" in opts else None
    assert D["srg_parameters"][:2] == [hn, hk], "packet and graph have different parameters"
    stages = D["stages"]; last = stages[-1]; names = last["parameters"]; t0 = time.time()
    graphs = {}
    for st in stages:
        for g in st["new_parameter_graphs"]: graphs[g["name"] if "name" in g else g.get("parameter")] = g
    print("packet: orders %s; parameters of the last stage: %s" % ([s["order"] for s in stages], names), flush=True)
    val = {k_: int(v_) for k_, v_ in json.load(open(opts["load"])).items()} if "load" in opts else {}
    for st in stages:
        for g in st["new_parameter_graphs"]:
            if g.get("name", g.get("parameter")) in val: continue
            nm = g.get("name", g.get("parameter")); rows = g["adjacency_bits"]; emb = embeddings(rows, hmask, hn); aut = embeddings(rows, rows, len(rows))
            assert emb is not None and emb % aut == 0; val[nm] = emb // aut
            print("  measured %-16s = %d   (order %d, %d edges, |Aut| = %d)  [%.0f s]" % (nm, val[nm], len(rows), sum(bin(r).count("1") for r in rows) // 2, aut, time.time() - t0), flush=True)
            if "save" in opts: json.dump(val, open(opts["save"], "w"))
    print("parameters: %d known; non-zero: %s" % (len(val), {k_: v_ for k_, v_ in val.items() if v_}), flush=True)
    if "measure" in flags: return
    t0 = time.time()
    def evaluate(aff, params): return Fr(aff[0]) + sum(Fr(c) * val[p] for c, p in zip(aff[1:], params))
    tot = ok = bad = skipped_disc = skipped_big = 0; todo = []
    for st in stages:
        params = st["parameters"]; assert all(p in val for p in params), (params, list(val))
        if only is not None and st["order"] not in only: continue
        for c in st["counts"]:
            pred = evaluate(c["affine"], params); assert pred.denominator == 1 and pred >= 0, ("non-integral or negative prediction", st["order"], c["code"], pred)
            todo.append((int(pred), st["order"], c))
    todo.sort(key=lambda x: (x[0], x[1])); worst = None
    for pred, order, c in todo:
        tot += 1; rows = c["adjacency_bits"]
        if time.time() - t0 > budget: skipped_big += 1; continue
        aut = embeddings(rows, rows, len(rows))
        if aut is None: skipped_disc += 1; continue
        if pred * aut > 4 * 10 ** 6: skipped_big += 1; continue
        emb = embeddings(rows, hmask, hn)
        if emb == pred * aut: ok += 1
        else:
            bad += 1; print("  MISMATCH order %d code %s: predicted %d, counted %s/%d" % (order, c["code"], pred, emb, aut), flush=True)
    print("types: %d considered; %d counted and equal to the prediction; %d MISMATCHES; skipped: %d disconnected, %d too numerous or out of time (%.0f s)" % (tot, ok, bad, skipped_disc, skipped_big, time.time() - t0), flush=True)
    fam = {}
    for st in stages:
        for nm, aff in st["families"].items(): fam[nm] = evaluate(aff, st["parameters"])
    print("families predicted by the packet at the measured parameters:")
    for nm, v_ in fam.items(): print("  %-40s %s" % (nm, v_))
    if len(sys.argv) > 6:
        BF, HF, F8 = [int(x) for x in sys.argv[4:7]]
        print("brute force (testbeds.py): bowtie-far edge %d, house-far edge %d, far pairs of 4-sets %d" % (BF, HF, F8))
        print("  present among the predictions: %s" % {nm: (v_ in (BF, HF, F8)) for nm, v_ in fam.items()})


if __name__ == "__main__": main()
