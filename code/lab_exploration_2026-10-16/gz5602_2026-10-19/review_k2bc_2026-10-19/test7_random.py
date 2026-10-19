import sys, time, json, random
from collections import Counter
ARGS = list(sys.argv)
sys.path.insert(0, '.')
import indep_model as M
prog = M.load_program(M.COVERS / 'core_000.json.gz')
rnd = random.Random(int(ARGS[1]))
allc = [a for a in json.load(open('cases.json'))['all'] if a[2] and a[2] <= 1200]
t0 = time.time(); res = Counter(); n = 0
while time.time() - t0 < 230:
    ci, bi = rnd.choice(allc)[:2]
    cv = M.cover(ci); core = cv['core']; bd = tuple(bytes.fromhex(cv['boundaries_hex'][bi]))
    leaves = [a for a, _ in prog.gen_attachments(core, bd) if prog.attachment_canon(a) == tuple(a)]
    for a in rnd.sample(leaves, min(4, len(leaves))):
        cert = prog.frontier(prog.materialize(core, bd, a), True)
        st = M.cpsat_frontier(M.known_rows(core['edges'], bd, a), time_limit=120)
        res[(cert['status'], st)] += 1; n += 1
        if st != 'INFEASIBLE' or not cert['status'].startswith('EXCLUDED'):
            print('DISAGREE', ci, bi, a, cert['status'], st, flush=True)
print(n, dict(res), 'secs %.0f' % (time.time() - t0))
