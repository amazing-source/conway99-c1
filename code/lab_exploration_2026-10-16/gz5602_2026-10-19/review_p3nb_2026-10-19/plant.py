import gzip, json, runpy, sys
from collections import Counter
pyext, codex, covdir = sys.argv[1:4]; cores = [int(c) for c in sys.argv[4].split(",")]
st = Counter()
for ci in cores:
    cov = "%s/core_%03d.json.gz" % (covdir, ci)
    sys.argv = [pyext, codex, "P3NB", cov, "0", "0", "--sat", "--lean", "--enc=seq", "--plant"]
    ns = runpy.run_path(pyext, run_name="__notmain__")
    rec = json.loads(gzip.decompress(open(cov, "rb").read())); core = rec["core"]
    done = 0
    for bi in range(0, len(rec["boundaries_hex"]), 97):
        bd = tuple(bytes.fromhex(rec["boundaries_hex"][bi]))
        for a, _ in ns["p3nb_attachments"](core, bd):
            r = ns["frontier"](ns["materialize"](core, bd, a), True)
            st[r["status"]] += 1; done += 1
        if done > 30: break
print(json.dumps(dict(st)))
