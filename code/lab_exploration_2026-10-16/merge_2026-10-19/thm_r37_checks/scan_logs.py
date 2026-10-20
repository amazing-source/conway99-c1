"""Scan the boost logs: per file, count lines/runs, statuses, leaves, prep errors, variants (read-only)."""
import json, sys, glob, os, collections
for path in sys.argv[1:]:
    recs = [json.loads(l) for l in open(path) if l.strip()]
    st = collections.Counter(); leaves = 0; perr = 0; nodes_max = 0; variants = collections.Counter(); types = collections.Counter()
    nonunsat = []
    for r in recs:
        if "runs" in r:
            types[(r.get("c"), r.get("d"), r.get("rho"))] += 1
            for run in r["runs"]:
                run["variant"] = str(run.get("variant", run.get("delta"))); variants[run["variant"]] += 1
                if "prep_error" in run:
                    perr += 1; nonunsat.append((r.get("spec"), r.get("seed"), run["variant"], "PREP_ERROR", run["prep_error"][-120:])); continue
                res = run["result"]
                if not isinstance(res, dict):
                    nonunsat.append((r.get("spec"), r.get("seed"), run["variant"], "BAD", str(res)[:80])); continue
                st[res["status"]] += 1
                leaves += res.get("leaves", 0)
                nodes_max = max(nodes_max, res.get("nodes", 0))
                if res["status"] != "UNSAT":
                    nonunsat.append((r.get("spec"), r.get("seed"), run["variant"], res["status"]))
        else:
            res = r.get("result")
            types[("tag", r.get("prep", {}).get("rho"))] += 1
            if not isinstance(res, dict):
                nonunsat.append((r.get("tag"), "BAD", str(res)[:80])); continue
            st[res["status"]] += 1; leaves += res.get("leaves", 0); nodes_max = max(nodes_max, res.get("nodes", 0))
            if res["status"] != "UNSAT": nonunsat.append((r.get("tag"), res["status"]))
    print(os.path.basename(path), "records", len(recs), "types", dict(types), "statuses", dict(st), "leaves", leaves,
          "prep_err", perr, "nodes_max", nodes_max)
    print("   variants", dict(variants))
    for x in nonunsat[:10]:
        print("   NON-UNSAT:", x)
