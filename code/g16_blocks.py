"""notes/112: second-order block check for the 4-cycle patterns (0,2,0,2), (0,2,2,2), (2,2,2,2) on the cycle 0-1-2-3.
Hand facts (notes/112): the generic common neighbours of the Kneser-opposite quadrangles Q01 x Q23 (block 1) and
Q03 x Q12 (block 2) all lie in Q45, Q46, Q56, whose vertices z have n01 = n23 = q_z and n03 = n12 = 2 - q_z with
q_z in {0, 2} for these three patterns; a vertex with q = 2 covers one 'deficit pair' of Q01 and one of Q23 (a
non-adjacent pair short of mu, or an adjacent pair whose line has its third point there), and the two q = 2 vertices of
a quadrangle cover complementary pairs.  Then D1(y, w) = 2 - #(decided common neighbours) must equal
sum_z N01(z) x N23(z); same for block 2 with q = 0.  Shadow maps are those forced by lemmas A and B."""
import itertools, sys
from collections import Counter
from slot_calculus import Config, build, propagate, LAB, CL
from slot_tests import base, matchings_no_mate

CYC = [0, 1, 2, 3]
NB = {v: [CYC[(v - 1) % 4], CYC[(v + 1) % 4]] for v in CYC}
V = [frozenset(p) for p in itertools.combinations(LAB, 2) if list(p)[0][0] != list(p)[1][0]]

def oracle(cfg):
    tau, rho = cfg.tau, cfg.rho
    def adj(y, w):
        s = y & w
        if len(s) == 1:
            (l,) = s; (u,) = y - s; (v,) = w - s
            return tau[l][u] == v
        for u in y:
            for v in w:
                if u[0] == v[0] and u != v:
                    (yo,) = y - {u}; (wo,) = w - {v}
                    return wo == rho[u[0]][yo] if u[1] == 0 else yo == rho[u[0]][wo]
        return None
    return adj

def commons(adj, y, w):
    n = len(y & w)
    return n + sum(1 for z in V if z not in (y, w) and adj(y, z) and adj(w, z))

def Q(a, b):
    return [frozenset({(a, s), (b, t)}) for s in (0, 1) for t in (0, 1)]

def deficits(adj, q):
    out = []
    for p, r in itertools.combinations(q, 2):
        need = (1 if adj(p, r) else 2) - commons(adj, p, r)
        out += [frozenset((p, r))] * need
    return out

def block_ok(MA, MB, D, QA, QB):
    if len(MA) != 6 or len(MB) != 6:
        return False
    comp = lambda a, b, q: (a | b) == frozenset(q) and not (a & b)
    for perm in set(itertools.permutations(range(6))):
        S = Counter()
        for i, j in enumerate(perm):
            for y in MA[i]:
                for w in MB[j]:
                    S[(y, w)] += 1
        if any(S[k] != D[k] for k in D):
            continue
        for m in itertools.permutations(range(6)):
            if all(comp(MA[a], MA[b], QA) and comp(MB[perm[a]], MB[perm[b]], QB)
                   for a, b in ((m[0], m[1]), (m[2], m[3]), (m[4], m[5]))):
                return True
    return False

def forced_rhos(sizes):
    """shadow maps allowed by lemmas A and B for T_v = first sizes[v] labels of class v (twisting both neighbours)."""
    T = {v: [(v, s) for s in range(sizes[v])] for v in CYC}
    per_class = []
    for v in CYC:
        Z = [l for u in NB[v] for l in T[u]]
        opts = []
        for p in itertools.permutations(Z):
            r = dict(zip(Z, p))
            if any(r[z] == z for z in Z):
                continue
            ok = True
            for u in NB[v]:
                w = [x for x in NB[v] if x != u][0]
                if T[u] and T[v]:                    # lemma A: rho_v swaps the labels of u
                    ok &= all(r[l] == (u, 1 - l[1]) for l in T[u])
                elif T[u] and not T[v]:              # lemma B (v silent): rho_v sends u-labels to the other neighbour
                    ok &= all(r[l][0] == w for l in T[u])
            if ok:
                opts.append(r)
        per_class.append((v, opts))
    return T, per_class

def run(sizes):
    T, per_class = forced_rhos(sizes)
    tw = [l for v in CYC for l in T[v]]
    tchoices = [list(matchings_no_mate([(c, s) for c in sorted(NB[l[0]]) for s in (0, 1)])) for l in tw]
    stats = Counter()
    for ms in itertools.product(*tchoices):
        for rs in itertools.product(*[opts for v, opts in per_class]):
            tau, rho = base()
            for l, m in zip(tw, ms):
                for a, b in m:
                    tau[l][a] = b; tau[l][b] = a
            for (v, _), r in zip(per_class, rs):
                rho[v].update(r)
            cfg = Config(tau, rho)
            var, lo, hi, eqs, inc = build(cfg)
            good, *_ = propagate(lo, hi, eqs)
            if not good:
                stats['first order refuted'] += 1
                continue
            adj = oracle(cfg)
            res = []
            for (A, B), (C, Dq) in (((0, 1), (2, 3)), ((0, 3), (1, 2))):
                QA, QB = Q(A, B), Q(C, Dq)
                MA, MB = deficits(adj, QA), deficits(adj, QB)
                D = {(y, w): 2 - commons(adj, y, w) for y in QA for w in QB}
                res.append(block_ok(MA, MB, D, QA, QB))
            stats[('block1 ok' if res[0] else 'block1 dead') + ', ' + ('block2 ok' if res[1] else 'block2 dead')] += 1
    return stats

if __name__ == '__main__':
    for sizes in [(0, 2, 0, 2), (0, 2, 2, 2), (2, 2, 2, 2)]:
        print(sizes, dict(run(sizes)), flush=True)
