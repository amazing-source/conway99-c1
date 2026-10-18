"""Summary of run gc1a: Gram covers in the exact all-in-one model (LAB 18/10/2026)."""
import glob, json, os, sys
d0 = sys.argv[1] if len(sys.argv) > 1 else "collect_gc1a"
rows = {}
for f in sorted(glob.glob(os.path.join(d0, "files", "out", "gc*.json"))):
    d = json.load(open(f)); n = os.path.basename(f)[:-5]
    if n.split("_")[0] not in ("gca", "gcf", "gce"):
        continue
    t = int(n.split("_")[1]); v = n.split("_")[0]
    rows.setdefault(t, {})[v] = (d.get("status"), round(d.get("cpu_seconds") or 0), d.get("gram_count"))
print("template  grams  anchors(status,cpu)  full(status,cpu)")
for t in sorted(rows):
    r = rows[t]
    g = next((x[2] for x in r.values()), None)
    print(t, g, r.get("gca", "-")[:2], r.get("gcf", "-")[:2], r.get("gce", "")[:2] if "gce" in r else "")
na = sum(1 for r in rows.values() if r.get("gca", ("",))[0] == "INFEASIBLE")
nf = sum(1 for r in rows.values() if r.get("gcf", ("",))[0] == "INFEASIBLE")
nany = sum(1 for r in rows.values() if any(x[0] == "INFEASIBLE" for x in r.values()))
print("INFEASIBLE: anchors", na, "full", nf, "either", nany, "of", len(rows))
