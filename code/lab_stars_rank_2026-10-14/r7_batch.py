"""Seven-label witnesses and their extension to the eighth label (LAB 16/10/2026).
Uses the R7 CNF written by five_cnf.py (stars 0..3 exact + labels {4,6},...,{4,12}, letter 4 bounded, reified products).
For each cadical seed: solve the R7 CNF, decode the structure (edge variables are 1..C(n,2) in combinations order, as in
five_cnf.py), check it independently, then ask (five_cnf.py --base) whether its four-star block accepts all eight labels
{4,t} (letter 4 bounded) and the full fifth star (letter 4 exact).
usage: python r7_batch.py <R7 cnf> <cadical exe> <seeds, e.g. 1-6> <seconds> <out dir>"""
import itertools
import json
import os
import subprocess
import sys
import time

cnf, cad, seeds, secs, out = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
os.makedirs(out, exist_ok=True)
lo, hi = (int(t) for t in seeds.split("-"))
K = 14
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]
S = [l for l in LABELS if any(y in l for y in (0, 1, 2, 3))]
S = S + [frozenset((4, t)) for t in range(6, 14) if frozenset((4, t)) not in S][:7]
n = len(S)
pairs = list(itertools.combinations(range(n), 2))


def need(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def check(edges):
    adj = [[0] * n for _ in range(n)]
    for i, j in edges:
        adj[i][j] = adj[j][i] = 1
    for i, l in enumerate(S):
        for y in range(K):
            cnt = sum(adj[i][j] for j in range(n) if y in S[j] and j != i)
            if (y in (0, 1, 2, 3) and cnt != need(l, y)) or cnt > need(l, y):
                return False
    for i, j in pairs:
        if sum(adj[i][t] and adj[j][t] for t in range(n)) + len(S[i] & S[j]) + adj[i][j] > 2:
            return False
    return True


def cadical(path, seed, limit):
    t0 = time.time()
    mp = path + ".model"
    with open(mp, "w") as mf:
        p = subprocess.Popen([cad, "-q", "--seed=%d" % seed, path], stdout=mf, stderr=subprocess.DEVNULL)
        try:
            p.wait(timeout=limit)
            st = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "UNKNOWN")
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            st = "TIMEOUT"
    return st, round(time.time() - t0, 1), mp


here = os.path.dirname(os.path.abspath(__file__))
py = sys.executable
for seed in range(lo, hi + 1):
    st, t, mp = cadical(cnf, seed, secs)
    rec = {"seed": seed, "r7": st, "t7": t}
    if st == "SAT":
        vals = set()
        for line in open(mp):
            if line.startswith("v "):
                vals.update(int(x) for x in line.split()[1:] if x != "0")
        edges = [list(pairs[k]) for k in range(len(pairs)) if (k + 1) in vals]
        rec["check"] = check(edges)
        bj = os.path.join(out, "r7_seed%d.json" % seed)
        json.dump({"K": K, "labels": [sorted(l) for l in S], "edges": edges}, open(bj, "w"))
        for tag, stars, extra in (("x8", "0,1,2,3", ["--xk", "8"]), ("five", "0,1,2,3,4", [])):
            c2 = os.path.join(out, "r7_seed%d_%s.cnf" % (seed, tag))
            r = subprocess.run([py, os.path.join(here, "five_cnf.py"), "14", stars, c2, "--reify", "--base", bj,
                                "--base-stars", "0,1,2,3", "--cadical", cad, "--seconds", str(secs)] + extra,
                               capture_output=True, text=True)
            line = [x for x in r.stdout.splitlines() if x.startswith("cadical:")]
            rec[tag] = line[0][9:] if line else "ERROR " + r.stderr[-200:]
            for suffix in ("", ".model"):
                try:
                    os.remove(c2 + suffix)
                except OSError:
                    pass
    print(json.dumps(rec), flush=True)
    with open(os.path.join(out, "r7_batch.jsonl"), "a") as fh:
        fh.write(json.dumps(rec) + "\n")
