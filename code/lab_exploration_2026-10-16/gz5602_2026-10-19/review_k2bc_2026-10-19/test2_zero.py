import sys, time, json
ARGS = list(sys.argv)
sys.path.insert(0, '.')
import indep_model as M
cases = json.load(open('cases.json'))['zero']
lo, hi = int(ARGS[1]), int(ARGS[2])
t0 = time.time(); nonzero = []
for ci, bi in cases[lo:hi]:
    cv = M.cover(ci); bd = tuple(bytes.fromhex(cv['boundaries_hex'][bi]))
    ma = M.my_attachments(cv['core']['edges'], bd)
    if ma:
        nonzero.append((ci, bi, len(ma)))
print('checked', hi - lo if hi <= len(cases) else len(cases) - lo, 'nonzero', nonzero, 'secs %.0f' % (time.time() - t0))
