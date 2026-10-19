import sys, time, json
from collections import Counter
ARGS = list(sys.argv)
sys.path.insert(0, '.')
import indep_model as M
prog = M.load_program(M.COVERS / 'core_000.json.gz')
want = ARGS[2].split(',')
cases = [(int(a), int(b)) for a, b in (x.split(':') for x in ARGS[1].split(','))]
t0 = time.time(); res = Counter()
for ci, bi in cases:
    cv = M.cover(ci); core = cv['core']; bd = tuple(bytes.fromhex(cv['boundaries_hex'][bi]))
    for a, _ in prog.gen_attachments(core, bd):
        if prog.attachment_canon(a) != tuple(a):
            continue
        cert = prog.frontier(prog.materialize(core, bd, a), True)
        if cert['status'] not in want:
            continue
        st = M.cpsat_frontier(M.known_rows(core['edges'], bd, a), time_limit=120)
        res[(cert['status'], st)] += 1
        if st != 'INFEASIBLE':
            print('DISAGREE', ci, bi, a, cert['status'], st, flush=True)
    if time.time() - t0 > 240:
        print('time cap reached after', ci, bi); break
print(dict(res), 'secs %.0f' % (time.time() - t0))
