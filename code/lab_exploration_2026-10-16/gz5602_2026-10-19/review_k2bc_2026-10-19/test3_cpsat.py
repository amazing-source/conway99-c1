import sys, time, json, random
from itertools import combinations, product
ARGS = list(sys.argv)
sys.path.insert(0, '.')
import indep_model as M
prog = M.load_program(M.COVERS / 'core_000.json.gz')
mode = ARGS[1]
rnd = random.Random(int(ARGS[3]) if len(ARGS) > 3 else 1)

def my_profiles(q, rows):
    """all known-neighbour sets of outside label q meeting the rectangle counts, own letter quota and C2 with known"""
    core_n = M.base(q, (0, 1)) + M.base(q, (0, 2))
    parts = [list(combinations(range(8), core_n))]
    for F in M.KRECTS[2:]:
        parts.append([(M.kid(F, c),) for c in range(4)] if M.base(q, F) else [()])
    out = []
    for ch in product(*parts):
        s = sorted(set(sum(ch, ())))
        mask = sum(2 ** u for u in s)
        if any(sum(1 for u in s if l in M.KL[u]) > M.quota(q, l) for l in range(14)):
            continue
        if any(M.pc(rows[u] & mask) + M.shared(q, M.KL[u]) + (u in s) > 2 for u in range(20)):
            continue
        out.append(s)
    return out

def plant(rows, with_c2):
    for attempt in range(200):
        chosen = []; ok = True
        for qi, q in enumerate(M.OL):
            dom = my_profiles(q, rows)
            if with_c2:
                dom = [p for p in dom if all(len(set(p) & set(chosen[j])) <= 2 - M.shared(q, M.OL[j]) for j in range(qi))]
            if not dom:
                ok = False; break
            chosen.append(rnd.choice(dom))
        if ok:
            return [[int(u in p) for u in range(20)] for p in chosen]
    return None

cases = [(int(a), int(b)) for a, b in (x.split(':') for x in ARGS[2].split(','))]
t0 = time.time()
for ci, bi in cases:
    cv = M.cover(ci); core = cv['core']; bd = tuple(bytes.fromhex(cv['boundaries_hex'][bi]))
    leaves = M.my_attachments(core['edges'], bd)
    if not leaves:
        print(ci, bi, 'no leaves'); continue
    if mode == 'plant':
        for a in rnd.sample(leaves, min(2, len(leaves))):
            rows = M.known_rows(core['edges'], bd, a)
            for wc in (False, True):
                pl = plant(rows, wc)
                if pl is None:
                    print(ci, bi, 'plant failed', wc); continue
                st = M.cpsat_frontier(rows, plant=pl, drop_outside_c2=not wc, time_limit=60)
                print(ci, bi, 'PLANT with_outside_c2=%s' % wc, st, flush=True)
    else:
        k = int(ARGS[4]) if len(ARGS) > 4 else 3
        for a in rnd.sample(leaves, min(k, len(leaves))):
            rows = M.known_rows(core['edges'], bd, a)
            tp = time.time(); cert = prog.frontier(prog.materialize(core, bd, a), True); tp = time.time() - tp
            tm = time.time(); st = M.cpsat_frontier(rows, time_limit=120); tm = time.time() - tm
            canon = prog.attachment_canon(a) == tuple(a)
            print(ci, bi, 'canonical' if canon else 'image', 'prog', cert['status'], (cert.get('proof_check') or {}).get('empty_clause_verified'),
                  'mine', st, 'times %.1f %.1f' % (tp, tm), flush=True)
print('secs %.0f' % (time.time() - t0))
