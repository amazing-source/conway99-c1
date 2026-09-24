"""Minimal UNSAT core for the 'confined twisting' family of rooted_family.py (twists only inside classes K).
tau constraints (perfect matchings, at least one twist) are hard; degree and SRG (lambda/mu) equations get selectors.
Usage: core_family.py 012
"""
import sys, itertools, time
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
from rooted_family import LABELS, mate
from core_extract import fmt

def main():
    K = set(int(ch) for ch in sys.argv[1])
    t0 = time.time()
    Xv = [frozenset((a, b)) for a, b in itertools.combinations(LABELS, 2) if a[0] != b[0]]
    V = ['x'] + LABELS + Xv
    pool = IDPool(); hard = []; groups = {}; T = {}
    def tvar(a, b, c):
        key = (a, tuple(sorted((b, c))))
        if key not in T:
            T[key] = pool.id(('t',) + key)
        return T[key]
    free = {}
    for a in LABELS:
        if a[0] in K:
            dom = [b for b in LABELS if b[0] in K and b[0] != a[0]]
            free[a] = dom
            for b in dom:
                hard.extend(CardEnc.equals([tvar(a, b, c) for c in dom if c != b], 1, vpool=pool, encoding=EncType.pairwise).clauses)
    hard.append([tvar(a, b, c) for a in free for b, c in itertools.combinations(free[a], 2) if c != mate(b)])
    def dvar(u, w):
        return pool.id(('d',) + tuple(sorted([tuple(sorted(u)), tuple(sorted(w))])))
    def adj(u, v):
        if u == v: return ('c', 0)
        if u == 'x' or v == 'x':
            o = v if u == 'x' else u
            return ('c', 1 if isinstance(o, tuple) else 0)
        ul, vl = isinstance(u, tuple), isinstance(v, tuple)
        if ul and vl: return ('c', 1 if mate(u) == v else 0)
        if ul: return ('c', 1 if u in v else 0)
        if vl: return ('c', 1 if v in u else 0)
        com = u & v
        if com:
            (a,) = com; (b,) = u - com; (c,) = v - com
            if a in free and b in free[a] and c in free[a]:
                return ('v', tvar(a, b, c))
            return ('c', 1 if mate(b) == c else 0)
        return ('v', dvar(u, v))
    def add(name, cls):
        s = pool.id(('sel', name)); groups[s] = (name, [[-s] + c for c in cls])
    for u in Xv:
        lits, const = [], 0
        for w in Xv:
            if w == u: continue
            a_ = adj(u, w)
            if a_[0] == 'v': lits.append(a_[1])
            else: const += a_[1]
        add(('deg', u), CardEnc.equals(lits, 12 - const, vpool=pool, encoding=EncType.seqcounter).clauses)
    for p in range(len(V)):
        for q in range(p + 1, len(V)):
            u, v = V[p], V[q]
            auv = adj(u, v); const, lits, ands = 0, [], []
            for w in V:
                if w in (u, v): continue
                a1, a2 = adj(u, w), adj(v, w)
                if a1 == ('c', 0) or a2 == ('c', 0): continue
                if a1[0] == 'c' and a2[0] == 'c': const += 1
                elif a1[0] == 'c': lits.append(a2[1])
                elif a2[0] == 'c': lits.append(a1[1])
                else:
                    c = pool.id(('and', p, q, str(w)))
                    ands.extend([[-c, a1[1]], [-c, a2[1]], [c, -a1[1], -a2[1]]]); lits.append(c)
            cls = list(ands)
            if auv[0] == 'c':
                want = (1 if auv[1] else 2) - const
                if want < 0 or want > len(lits) or (not lits and want != 0): cls.append([])
                elif lits: cls.extend(CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses)
            else:
                e = auv[1]
                for want, cond in ((1 - const, e), (2 - const, -e)):
                    if want < 0 or want > len(lits): cls.append([-cond]); continue
                    for cl in CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cls.append([-cond] + cl)
            add(('srg', u, v), cls)
    s = Cadical153()
    for c in hard: s.add_clause(c)
    for g in groups.values():
        for c in g[1]: s.add_clause(c)
    sels = list(groups)
    r = s.solve(assumptions=sels)
    print(f'K={sorted(K)}: {len(sels)} groups -> {"SAT" if r else "UNSAT"} ({time.time()-t0:.1f}s)', flush=True)
    if r: return
    core = list(s.get_core()); print('initial core', len(core), flush=True)
    i = 0
    while i < len(core):
        trial = core[:i] + core[i + 1:]
        if not s.solve(assumptions=trial):
            c2 = list(s.get_core()); core = c2 if len(c2) < len(trial) else trial
        else:
            i += 1
    print(f'minimal core ({len(core)}, {time.time()-t0:.1f}s):')
    for sel in sorted(core, key=lambda z: str(groups[z][0])):
        n = groups[sel][0]
        print('  ', n[0], ' '.join(fmt(p) for p in n[1:]))

main()
