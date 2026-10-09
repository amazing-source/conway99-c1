import glob, re, collections, sys, os
os.chdir(sys.argv[1])
n = 0; dup = collections.Counter(); low = []; odd = []; cmin = 10**9; nmin = 10**9; hist = collections.Counter(); seen = {}
for f in glob.glob("sweep_48_part*of12000.log"):
    for l in open(f):
        l = l.rstrip(chr(10))
        if not l.startswith("48 "): odd.append((f, l[:200])); continue
        k = l.split("|")[0].strip(); n += 1
        if k in seen:
            dup[k] += 1
            if seen[k].split("|")[1] != l.split("|")[1]: odd.append(("DIFFERENT DUPLICATE", k))
        seen[k] = l
        if "TORSION" in l: continue
        cs = list(map(int, re.findall(r"cands (\d+)", l))); ns = list(map(int, re.findall(r"nodes (\d+)", l)))
        if len(cs) != 2 or len(ns) != 2 or cs[0] != cs[1]: odd.append((f, l[:300])); continue
        cmin = min(cmin, cs[0]); nmin = min(nmin, min(ns)); hist[cs[0] // 1000] += 1
        if cs[0] < 2000 or min(ns) < 1000: low.append(l[:300])
print("lines %d, distinct balls %d, balls logged more than once %d" % (n, len(seen), len(dup)))
print("torsion-free lines: smallest cands %d, smallest nodes %d" % (cmin, nmin))
print("cands histogram (thousands):", sorted(hist.items()))
print("low lines (cands < 2000 or nodes < 1000): %d" % len(low))
for l in low[:10]: print("   ", l)
print("odd lines: %d" % len(odd))
for o in odd[:10]: print("   ", o)
