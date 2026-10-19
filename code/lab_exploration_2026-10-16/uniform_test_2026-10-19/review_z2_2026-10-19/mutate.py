import json, sys, subprocess, copy, gzip
from fractions import Fraction as Fr
PY, VER, CAT, CF = sys.argv[1:5]
cf = json.load(open(CF)); ce = cf['certificate_explicit']
def run(name, newcf):
    p = 'mut/%s.json' % name
    json.dump(newcf, open(p, 'w'))
    r = subprocess.run([PY, '-I', '-X', 'utf8', VER, CAT, p], capture_output=True, text=True, timeout=250)
    out = r.stdout.strip()
    if out:
        o = json.loads(out); verdict = 'valid=%s neg=%s beta=%s' % (o['valid'], o['negative_coefficients'], o['beta'])
    else:
        verdict = 'CRASH/REJECT: ' + (r.stderr.strip().splitlines() or ['?'])[-1][:150]
    print('%-28s %s' % (name, verdict), flush=True)
def mk(fn):
    n = copy.deepcopy(cf); fn(n['certificate_explicit'], n); return n
big = lambda part, pref: max((k for k in ce[part] if k.startswith(pref)), key=lambda k: abs(Fr(ce[part][k])))
kL3, kL1, kC0, kUp, kE3 = big('y_eq', 'L3'), big('y_eq', 'L1'), big('y_eq', 'C0'), big('y_up', 'm|'), big('y_ub', 'E3n')
def neg(d, k): d[k] = str(-Fr(d[k]))
run('baseline', cf)
run('flip_L3', mk(lambda c, n: neg(c['y_eq'], kL3)))
run('flip_L1', mk(lambda c, n: neg(c['y_eq'], kL1)))
run('drop_C0', mk(lambda c, n: c['y_eq'].pop(kC0)))
run('drop_up_m', mk(lambda c, n: c['y_up'].pop(kUp)))
run('drop_E3n', mk(lambda c, n: c['y_ub'].pop(kE3)))
run('neg_E3n', mk(lambda c, n: neg(c['y_ub'], kE3)))
run('E3n_on_grid', mk(lambda c, n: c['y_ub'].__setitem__('E3n|02', '1')))
kn = next(iter(ce['y_up']))
run('neg_up', mk(lambda c, n: neg(c['y_up'], kn)))
# unsupported m pair: two types of the same grid rectangle 02 whose z(02) = 2 ... build an obviously unsupported one
types = [k.split('|')[1] for k in ce['y_eq'] if k.startswith('L1')]
tz = {}
for t in set(types):
    tz.setdefault(t.split(':')[0], []).append(t)
from itertools import combinations
RECT = list(combinations(range(7), 2))
def z(t): return [int(ch) for ch in t.split(':')[1]]
bad = None
for t1 in sorted(set(types)):
    for t2 in sorted(set(types)):
        q2 = RECT.index(tuple(int(ch) for ch in t2.split(':')[0]))
        if z(t1)[q2] == 0:
            bad = (t1, t2); break
    if bad: break
run('unsupported_m', mk(lambda c, n: c['y_up'].__setitem__('m|%s|%s' % bad, '1')))
run('unknown_type', mk(lambda c, n: c['y_eq'].__setitem__('L3|01:' + '9' * 21 + '|01', '1')))
run('bad_kind', mk(lambda c, n: c['y_eq'].__setitem__('X9|01', '-100')))
run('C0_bogus_rect', mk(lambda c, n: c['y_eq'].__setitem__('C0|77', '-100')))
run('other_template', mk(lambda c, n: n.__setitem__('template_index', n['template_index'] + 1)))
run('scale_x3', mk(lambda c, n: [d.__setitem__(k, str(3 * Fr(v))) for d in c.values() for k, v in list(d.items())]))
run('all_negated', mk(lambda c, n: [d.__setitem__(k, str(-Fr(v))) for d in (c['y_eq'],) for k, v in list(d.items())]))
# reversed order m key (same variable) should be accepted
def rev(c, n):
    k = kUp; v = c['y_up'].pop(k); _, a, b = k.split('|'); c['y_up']['m|%s|%s' % (b, a)] = v
run('reversed_m_key', mk(rev))
# NaN / inf literal
run('nan_value', mk(lambda c, n: c['y_eq'].__setitem__(kC0, float('nan'))))
# drop every multiplier mentioning one type (simulates a certifier that missed that state)
def droptype(c, n):
    t = sorted(set(types))[len(types) // 3 % len(set(types))]
    for d in c.values():
        for k in [k for k in d if t in k.split('|')]:
            d.pop(k)
run('drop_one_type', mk(droptype))
