"""Audit (15/10/2026): joint distribution of (numerical nullity, min t, min c) over every PSD visit printed in the
walk logs of this folder ('T AND U PSD (c(l)=a, c(m)=b), ..., numerical nullity N, t = (x,y)').  Purpose: is there a
PSD four-star structure of nullity >= 14 with a line carrying <= 7 transversals (bridge G11 / O3), or with c = 1 (O1)?
Logs are biased samples (walks, several families); this measures what was SEEN, not what exists.
usage: python audit_logs_nt.py"""
import glob
import re

pat = re.compile(r'T AND U PSD \(c\(l\)=(\d+), c\(m\)=(\d+)\).*numerical nullity (\d+), t = \((\d+),(\d+)\)')
best_by_t = {}
best_by_c = {}
files_hits = {}
total = 0
for f in sorted(glob.glob('*.log')):
    with open(f, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if 'T AND U PSD' not in line:
                continue
            m = pat.search(line)
            if not m:
                continue
            cl, cm, nul, tl, tm = map(int, m.groups())
            total += 1
            mt, mc = min(tl, tm), min(cl, cm)
            if nul > best_by_t.get(mt, (-1, ''))[0]:
                best_by_t[mt] = (nul, f)
            if nul > best_by_c.get(mc, (-1, ''))[0]:
                best_by_c[mc] = (nul, f)
            if nul >= 14 and (mt <= 7 or mc == 1):
                files_hits[f] = files_hits.get(f, 0) + 1
print("PSD visits parsed:", total)
print("max numerical nullity by min(t(l), t(m)):")
for k in sorted(best_by_t):
    print("   min t = %2d: max nullity %d (first seen in %s)" % (k, best_by_t[k][0], best_by_t[k][1]))
print("max numerical nullity by min(c(l), c(m)):")
for k in sorted(best_by_c):
    print("   min c = %d: max nullity %d (first seen in %s)" % (k, best_by_c[k][0], best_by_c[k][1]))
print("logs with a PSD visit of nullity >= 14 and (min t <= 7 or min c = 1):", files_hits)
