"""Equal disjoint pair H_P = H_Q = h, ternary case (LAB 19/10/2026), on top of Codex's encoder
root_component_equal_pair_profiles.py (his working tree, 19/10 09:40 local; instance() and encode() reused unchanged).
Exact facts added (all proved in the notes; h = H_P = base(., P) - Z_P, extended by 0 on the root and the letters, is an
eigenvector of the Conway adjacency for -4, a consequence of lambda = 1, mu = 2 and the letter quotas):
  (T0) no value -2 (m = 0): the m = 1 case is excluded by Codex's certified runs (diagonal/diagonal at the three
       rectangles of D) and is impossible for a lateral matching (Codex's note, section 2);
  (T1) exactly 14 values +1 (the 8 core vertices and exactly 6 outside, all in D) and 14 values -1 (Codex, section 3);
  (T2) eigen-equation at a core vertex u: its internal partner has h = 1 and no outside vertex with h = 1 touches the
       core, so u has exactly 5 outside neighbours with h = -1;
  (T3) eigen-equation at a letter l: the sum of h over the 12 labels containing l is 0, i.e. the outside labels
       containing l sum to minus the number of core labels containing l.
Every case is one labelled pair of internal matchings (9 per template); an exclusion of the template needs all 9.
usage: python lab_equal_pair_m0.py <codex code dir> <catalogue.json.gz> <template> <m1> <m2> <cpu seconds> <out.json>
       [--extend-all]   (adds Codex's --all-known-pair-rows extension: every outside row completed)
       [--hubs=03,04]   (complete only the rows of the labels of these rectangles; T4 on those rows)
       [--dump=FILE.cnf] (write the DIMACS CNF and stop; for an external solver whose proof is then checked by drat-trim)"""
import json
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path

CODEX, CAT, TPL, M1, M2, CPU, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), \
    float(sys.argv[6]), Path(sys.argv[7])
EXTEND = '--extend-all' in sys.argv
HUB_RECTS = [tuple(sorted((int(r[0]), int(r[1])))) for r in next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--hubs=')), '').split(',') if r]
if sys.flags.optimize:
    raise SystemExit('assertions required')
sys.path.insert(0, CODEX)
import gzip                                                               # noqa: E402
import root_component_equal_pair_profiles as ep                          # noqa: E402
from pysat.card import CardEnc, EncType                                  # noqa: E402

assert not OUT.exists()
template = json.loads(gzip.decompress(Path(CAT).read_bytes()))['open'][TPL]['template']
pair = ep.TARGETS[TPL]
relation = ep.equal_pair_relation(template, pair)                        # exact certificate of H_P = H_Q
data = ep.instance(template, pair, (M1, M2), bounded_defect=True)
P0 = pair[0]


def hval(y, prof):
    return ep.base(tuple(l // 2 for l in data['outside_labels'][y]), P0) - sum(u < 4 for u in prof)


# (T0) remove every profile with h = -2 (bounded_defect already removed h < -2)
before = sum(map(len, data['domains']))
data['domains'] = [[p for p in d if hval(y, p) >= -1] for y, d in enumerate(data['domains'])]
removed = before - sum(map(len, data['domains']))
assert all(data['domains']), 'an outside label lost every profile'
hubs = list(range(len(data['domains']))) if EXTEND else [y for y, q in enumerate(data['outside_labels']) if tuple(l // 2 for l in q) in HUB_RECTS]
t0 = time.process_time()
clauses, literals, info = ep.encode(data, template, hubs, all_known_pair_rows=EXTEND)
top = info['variables']


class P:
    pass


pool = P(); pool.top = top
extra = defaultdict(int)


def card(lits, k, kind, mode='eq'):
    f = {'eq': CardEnc.equals, 'le': CardEnc.atmost, 'ge': CardEnc.atleast}[mode]
    if mode == 'eq' and not 0 <= k <= len(lits):
        clauses.append([]); extra[kind] += 1; return
    cnf = f(lits, bound=k, top_id=pool.top, encoding=EncType.seqcounter)
    pool.top = max(pool.top, cnf.nv); clauses.extend(cnf.clauses); extra[kind] += len(cnf.clauses)


plus = [lit for y, d in enumerate(data['domains']) for i, p in enumerate(d) if hval(y, p) == 1 for lit in [literals[y][i]]]
minus = [lit for y, d in enumerate(data['domains']) for i, p in enumerate(d) if hval(y, p) == -1 for lit in [literals[y][i]]]
assert all(not p for y, d in enumerate(data['domains']) for p in d if hval(y, p) == 1), 'h = 1 outside must have no core neighbour'
card(plus, 6, 'T1_plus')                                                  # (T1)
card(minus, 14, 'T1_minus')
for u in range(8):                                                        # (T2)
    lits = [literals[y][i] for y, d in enumerate(data['domains']) for i, p in enumerate(d) if u in p and hval(y, p) == -1]
    card(lits, 5, 'T2_core_minus_neighbours')
known = data['known_labels']
for l in range(14):                                                       # (T3) sum of h over labels with letter l is 0
    rhs = -sum(l in q for q in known)
    pos = [literals[y][i] for y, d in enumerate(data['domains']) if l in data['outside_labels'][y]
           for i, p in enumerate(d) if hval(y, p) == 1]
    neg = [literals[y][i] for y, d in enumerate(data['domains']) if l in data['outside_labels'][y]
           for i, p in enumerate(d) if hval(y, p) == -1]
    # #pos - #neg = rhs  <=>  #pos + #(not neg) = rhs + len(neg)
    card(pos + [-x for x in neg], rhs + len(neg), 'T3_letter_sums')
if hubs:
    # (T4) eigen-equation at every completed outside row w (all rows with --extend-all, else the --hubs rows) (all rows are complete in this mode):
    #   |N(w) cap C| + #(outside neighbours with h = 1) - #(outside neighbours with h = -1) = -4 h(w),
    # where h(w) and |N(w) cap C| = |profile| are fixed by w's profile; guarded by the profile class of w.
    physical = {(x, y): v for x, y, v in info['row_extension']['edge_variables']}
    n_out = len(data['outside_labels'])

    def new():
        pool.top += 1
        return pool.top
    hflag = {}

    def flag(z, val):
        if (z, val) not in hflag:
            lits = [literals[z][i] for i, p in enumerate(data['domains'][z]) if hval(z, p) == val]
            if not lits:
                hflag[z, val] = None
            else:
                v = new(); hflag[z, val] = v
                clauses.append([-v] + lits); clauses.extend([[-x, v] for x in lits])
        return hflag[z, val]
    prod = {}

    def both(e, f):
        key = (e, f)
        if key not in prod:
            v = new(); prod[key] = v
            clauses.extend([[-v, e], [-v, f], [-e, -f, v]])
        return prod[key]
    for w in hubs:
        plus_t, minus_t = [], []
        for z in range(n_out):
            if z == w:
                continue
            e = physical[tuple(sorted((w, z)))]
            fp, fm = flag(z, 1), flag(z, -1)
            if fp is not None:
                plus_t.append(both(e, fp))
            if fm is not None:
                minus_t.append(both(e, fm))
        targets = defaultdict(list)
        for i, p in enumerate(data['domains'][w]):
            targets[-4 * hval(w, p) - len(p)].append(literals[w][i])
        for t, guards in targets.items():
            g = new()
            clauses.append([-g] + guards); clauses.extend([[-x, g] for x in guards])
            k = t + len(minus_t)
            lits = plus_t + [-x for x in minus_t]
            if not 0 <= k <= len(lits):
                clauses.append([-g]); extra['T4_impossible_guard'] += 1; continue
            cnf = CardEnc.equals(lits, bound=k, top_id=pool.top, encoding=EncType.seqcounter)
            pool.top = max(pool.top, cnf.nv)
            clauses.extend([[-g] + c for c in cnf.clauses]); extra['T4_eigen_rows'] += len(cnf.clauses)
enc_cpu = time.process_time() - t0
DUMP = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--dump=')), None)
if DUMP:
    with open(DUMP, 'w', newline='\n') as f:
        f.write('p cnf %d %d\n' % (pool.top, len(clauses)))
        for c in clauses:
            f.write(' '.join(map(str, c)) + ' 0\n')
    print(json.dumps({'dumped': DUMP, 'variables': pool.top, 'clauses': len(clauses)}))
    sys.exit(0)
from pysat.solvers import Solver                                          # noqa: E402
sys.path.insert(0, CODEX)
from root_component_shared_k3_profile_sat import flush_native_proof, finished_proof  # noqa: E402
from root_component_native_rup import check_native_rup                    # noqa: E402
res = {'scope': __doc__.split('\n')[0], 'template': TPL, 'pair': pair, 'matching_indices': [M1, M2],
       'extend_all_rows': EXTEND, 'hub_rectangles': HUB_RECTS, 'relation': relation, 'removed_minus_two_profiles': removed,
       'domain_total': sum(map(len, data['domains'])), 'codex_encoding': {k: info[k] for k in ('clauses', 'variables', 'clause_kinds')},
       'lab_extra_clauses': dict(extra), 'clauses': len(clauses), 'variables': pool.top, 'cpu_encoding_seconds': enc_cpu}
with Solver(name='g3', bootstrap_with=clauses, with_proof=True) as s:
    done = threading.Event(); st = time.process_time()

    def timer():
        while not done.wait(0.05):
            if time.process_time() - st >= CPU:
                s.interrupt(); return
    th = threading.Thread(target=timer, daemon=True); th.start()
    try:
        ans = s.solve_limited(expect_interrupt=True)
    finally:
        done.set(); th.join(); s.clear_interrupt()
    flush_native_proof()
    res['status'] = 'UNKNOWN' if ans is None else ('SAT_RELAXATION' if ans else 'UNSAT')
    res['cpu_search_seconds'] = time.process_time() - st
    res['solver_stats'] = s.accum_stats()
    if ans is False:
        res['proof'] = check_native_rup(clauses, finished_proof(s), OUT.with_suffix(''))
OUT.write_text(json.dumps(res, indent=1, default=str))
print(json.dumps({k: res[k] for k in ('template', 'matching_indices', 'status', 'cpu_search_seconds', 'domain_total', 'clauses')}))
