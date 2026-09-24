"""Explain a refutation by unit propagation: run UP with reason tracking on the rooted model of a prescribed tau
(rooted_model.py), find the conflict, walk the implication graph back and report which ORIGINAL constraints
(SRG equation of a vertex pair, degree of an X-vertex, or grid tightness) are involved.
Usage: python explain_up.py g19AA
"""
import sys, itertools, collections
import rooted_model as rm
from pysat.formula import IDPool, CNF


def build_tagged(tau):
    """same model as rooted_model.build but records, for each clause, the constraint it comes from."""
    tags = []
    orig_extend = CNF.extend
    orig_append = CNF.append
    current = ['init']

    class TCNF(CNF):
        def append(self, cl, **kw):
            orig_append(self, cl)
            tags.append(current[0])

        def extend(self, cls, **kw):
            for cl in cls:
                self.append(cl)
    # monkeypatch CNF inside rooted_model and wrap the constraint loops by re-implementing build with tags
    Xv = [frozenset((a, b)) for a, b in itertools.combinations(rm.LABELS, 2) if a[0] != b[0]]
    V = ['x'] + rm.LABELS + Xv
    pool = IDPool()
    cnf = TCNF()
    D = {}
    mate = rm.mate
    from pysat.card import CardEnc, EncType

    def dvar(u, w):
        key = tuple(sorted([tuple(sorted(u)), tuple(sorted(w))]))
        if key not in D:
            D[key] = pool.id(('d',) + key)
        return D[key]

    def adj(u, v):
        if u == v:
            return ('c', 0)
        if u == 'x' or v == 'x':
            o = v if u == 'x' else u
            return ('c', 1 if isinstance(o, tuple) else 0)
        ul, vl = isinstance(u, tuple), isinstance(v, tuple)
        if ul and vl:
            return ('c', 1 if mate(u) == v else 0)
        if ul:
            return ('c', 1 if u in v else 0)
        if vl:
            return ('c', 1 if v in u else 0)
        com = u & v
        if com:
            (a,) = com
            (b,) = u - com
            (c,) = v - com
            return ('c', 1 if tau[a][b] == c else 0)
        return ('v', dvar(u, v))
    for u in Xv:
        current[0] = ('deg', u)
        lits = [adj(u, w)[1] for w in Xv if w != u and adj(u, w)[0] == 'v']
        cnf.extend(CardEnc.equals(lits, 10, vpool=pool, encoding=EncType.seqcounter).clauses)
    for p in range(len(V)):
        for q in range(p + 1, len(V)):
            u, v = V[p], V[q]
            current[0] = ('pair', u, v)
            auv = adj(u, v)
            const, lits = 0, []
            for w in V:
                if w in (u, v):
                    continue
                a1, a2 = adj(u, w), adj(v, w)
                if a1 == ('c', 0) or a2 == ('c', 0):
                    continue
                if a1[0] == 'c' and a2[0] == 'c':
                    const += 1
                elif a1[0] == 'c':
                    lits.append(a2[1])
                elif a2[0] == 'c':
                    lits.append(a1[1])
                else:
                    c = pool.id(('and', p, q, str(w)))
                    cnf.extend([[-c, a1[1]], [-c, a2[1]], [c, -a1[1], -a2[1]]])
                    lits.append(c)
            if auv[0] == 'c':
                want = (1 if auv[1] else 2) - const
                if want < 0 or want > len(lits):
                    cnf.append([])
                elif lits:
                    cnf.extend(CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses)
                elif want != 0:
                    cnf.append([])
            else:
                e = auv[1]
                for want, cond in ((1 - const, e), (2 - const, -e)):
                    if want < 0 or want > len(lits):
                        cnf.append([-cond]); continue
                    for cl in CardEnc.equals(lits, want, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cnf.append([-cond] + cl)
    return cnf, pool, tags, D


def unit_propagate(clauses):
    """naive-but-OK UP with watched literals and reasons. returns (conflict_clause_index or None, assign, reason)."""
    assign = {}
    reason = {}
    watches = collections.defaultdict(list)
    queue = []
    for i, cl in enumerate(clauses):
        if len(cl) == 0:
            return i, assign, reason
        if len(cl) == 1:
            l = cl[0]
            if assign.get(abs(l)) is None:
                assign[abs(l)] = l > 0; reason[abs(l)] = i; queue.append(l)
            elif assign[abs(l)] != (l > 0):
                return i, assign, reason
        else:
            watches[cl[0]].append(i); watches[cl[1]].append(i)
    val = lambda l: None if assign.get(abs(l)) is None else (assign[abs(l)] == (l > 0))
    qi = 0
    while qi < len(queue):
        l = queue[qi]; qi += 1
        fl = -l
        wl = watches[fl]
        watches[fl] = []
        for k, ci in enumerate(wl):
            cl = clauses[ci]
            # ensure fl is at position 1
            if cl[0] == fl:
                cl[0], cl[1] = cl[1], cl[0]
            if val(cl[0]) is True:
                watches[fl].append(ci); continue
            found = False
            for j in range(2, len(cl)):
                if val(cl[j]) is not False:
                    cl[1], cl[j] = cl[j], cl[1]
                    watches[cl[1]].append(ci); found = True; break
            if found:
                continue
            watches[fl].append(ci)
            if val(cl[0]) is False:
                watches[fl].extend(wl[k + 1:])
                return ci, assign, reason
            if val(cl[0]) is None:
                assign[abs(cl[0])] = cl[0] > 0; reason[abs(cl[0])] = ci; queue.append(cl[0])
    return None, assign, reason


def main():
    case = sys.argv[1]
    tau = rm.tau_case(case)
    cnf, pool, tags, D = build_tagged(tau)
    clauses = [list(c) for c in cnf.clauses]
    conf, assign, reason = unit_propagate(clauses)
    if conf is None:
        print('UP does not refute'); return
    # walk back
    seen_cl, stack, used = set(), [conf], set()
    while stack:
        ci = stack.pop()
        if ci in seen_cl:
            continue
        seen_cl.add(ci); used.add(tags[ci])
        for l in clauses[ci]:
            v = abs(l)
            if v in reason and reason[v] != ci:
                stack.append(reason[v])
    print(f'conflict found; {len(seen_cl)} clauses in the implication cone, from {len(used)} original constraints:')
    fmt = lambda z: z if isinstance(z, str) else (str(z) if isinstance(z, tuple) else '{' + ','.join(f'{c}{s}' for c, s in sorted(z)) + '}')
    for t in sorted(used, key=str):
        if t[0] == 'pair':
            print('   pair', fmt(t[1]), fmt(t[2]))
        else:
            print('  ', t[0], fmt(t[1]) if len(t) > 1 else '')


if __name__ == '__main__':
    main()
