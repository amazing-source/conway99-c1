import gzip, json, runpy, sys, time, random
pyext, codex, covdir, mydir = sys.argv[1:5]
cores = [int(c) for c in sys.argv[5].split(",")]; nb = int(sys.argv[6]); budget = float(sys.argv[7])
sys.path.insert(0, mydir)
from indep_model import setup, solve
GR = [(4, 5), (4, 6), (1, 3)]
K, O = setup(GR)
t0 = time.time(); out = {}
tot = {"attachments": 0, "both_excluded": 0, "both_open": 0, "theirs_excl_mine_SAT": 0, "theirs_open_mine_UNSAT": 0}
disc = []; stc = {}
for ci in cores:
    cov = "%s/core_%03d.json.gz" % (covdir, ci)
    sys.argv = [pyext, codex, "P3NB", cov, "0", "0", "--sat", "--lean", "--enc=seq"]
    ns = runpy.run_path(pyext, run_name="__notmain__")
    assert [tuple(q) for q in ns["LABELS"]] == K
    rec = json.loads(gzip.decompress(open(cov, "rb").read())); core = rec["core"]; recs = rec["boundaries_hex"]
    sel = random.Random(ci * 31337 + 11).sample(range(len(recs)), min(nb, len(recs)))
    for bi in sel:
        if time.time() - t0 > budget: break
        bd = tuple(bytes.fromhex(recs[bi]))
        for a, _ in ns["p3nb_attachments"](core, bd):
            rows = ns["materialize"](core, bd, a)
            st = ns["frontier"](rows, True)["status"]; stc[st] = stc.get(st, 0) + 1
            mine = solve(GR, list(rows))[0]
            tot["attachments"] += 1
            te = st.startswith("EXCLUDED")
            if te and not mine: tot["both_excluded"] += 1
            elif not te and mine: tot["both_open"] += 1
            elif te: tot["theirs_excl_mine_SAT"] += 1; disc.append([ci, bi, a, st])
            else: tot["theirs_open_mine_UNSAT"] += 1; disc.append([ci, bi, a, st])
print(json.dumps({"cores": cores, **tot, "their_status_counts": stc, "discrepancies": disc[:10], "sec": round(time.time() - t0, 1)}))
