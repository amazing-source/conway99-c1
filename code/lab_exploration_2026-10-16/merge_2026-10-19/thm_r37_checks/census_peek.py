"""Read-only peek at the order-9 census JSON: top-level keys, the order-2/3 counts, and the entry whose count is the parameter P."""
import json, sys
cen = json.load(open(sys.argv[1]))
print("keys:", list(cen.keys())[:20])
for k, v in cen.items():
    if k != "counts":
        s = json.dumps(v)
        print(k, ":", s[:300])
cs = cen["counts"]
print("n counts:", len(cs), "fields:", list(cs[0].keys()))
for c in cs:
    if c.get("order", 0) <= 3 or "29327" in str(c.get("code")) or c.get("count") in ("P",):
        print({k: (str(v)[:120]) for k, v in c.items()})
