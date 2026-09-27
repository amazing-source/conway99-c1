"""Two-block rational filter (C1, 27/09).  A partial graph around the fixed point x0 of the involution, in which two blocks
c, d are 'described' (every pair with a vertex in x0, the interior or a c-/d-root is known), and the far-far pairs are
unknown.  srg(v, k, 1, 2) with k = deg(x0).
  (a) every lambda/mu count whose terms are all known is checked (1 common neighbour if adjacent, 2 if not), and degrees;
  (b) for every vertex y with unknown entries, each fully known row w gives the exact linear equation
          sum_{z in Unk(y)} adj(w,z) a(y,z) = [2 - adj(w,y)] - #{z known : adj(w,z) = adj(y,z) = 1}.
      Rank, and the exact solution when unique (it must be integral, in {0,1}); at m = 7 there are 59 equations
      (x0, 14 interior, 44 described roots) for 38 unknowns per y, so the far-far graph is overdetermined by U_c, U_d;
  (c) if every unknown is determined: symmetry, sigma-invariance, degrees and every lambda/mu count (then it IS an srg).
Input JSON: {"n", "x0", "blocks": [[a, a'], ...], "adj": n x n with 1 / 0 / -1 = unknown} (structures' two-block model).
Usage: python q7_twoblock_filter.py model.json   |   python q7_twoblock_filter.py --selftest-bvls [reps]"""
import sys, json, random
import numpy as np


def sigma_map(M, x0, blocks):
    """sigma: x0 fixed, swaps the two vertices of each block, root {a, b} -> root {sigma a, sigma b} (roots are read
    through their two interior neighbours, whose rows are known)."""
    n = len(M)
    sig = list(range(n))
    inner = {}
    for a, b in blocks:
        sig[a], sig[b] = b, a
        inner[a] = inner[b] = True
    key = {}
    for r in range(n):
        if r == x0 or r in inner:
            continue
        I = tuple(sorted(a for a in inner if M[r][a] == 1))
        key[I] = r
    for I, r in key.items():
        sig[r] = key[tuple(sorted(sig[a] for a in I))]
    return sig


def check_counts(M, k):
    """(a): lambda/mu on every pair whose products are all known, and degrees.  Returns the list of violations."""
    n = len(M)
    A = np.asarray(M)
    kn = A >= 0
    one = (A == 1).astype(np.int32)
    unk = (A < 0).astype(np.int32)
    nz = (A != 0).astype(np.int32)                     # 1 or unknown
    cnt = one @ one.T                                  # known common neighbours
    amb = unk @ nz.T + nz @ unk.T                      # > 0 if some product is undetermined
    bad = []
    for u in range(n):
        for w in range(u + 1, n):
            if not kn[u, w] or amb[u, w] > 0:
                continue
            want = 1 if A[u, w] == 1 else 2
            if cnt[u, w] != want:
                bad.append(('pair', u, w, int(cnt[u, w]), want))
    for u in range(n):
        d1 = int(one[u].sum())
        if (kn[u].all() and d1 != k) or d1 > k:
            bad.append(('degree', u, d1, k))
    return bad


def solve_rows(M, truth=None):
    """(b): per vertex y with unknowns, the exact linear system from the fully known rows."""
    n = len(M)
    A = np.asarray(M)
    full = [w for w in range(n) if (A[w] >= 0).all()]
    out = {}
    for y in range(n):
        U = [z for z in range(n) if A[y, z] < 0]
        if not U:
            continue
        rows, rhs = [], []
        for w in full:
            if w == y:
                continue
            known_common = sum(1 for z in range(n) if A[y, z] == 1 and A[w, z] == 1)
            rows.append([int(A[w, z]) for z in U])
            rhs.append((1 if A[w, y] == 1 else 2) - known_common)
        C = np.array(rows, dtype=float)
        b = np.array(rhs, dtype=float)
        r = np.linalg.matrix_rank(C) if len(rows) else 0
        rab = np.linalg.matrix_rank(np.column_stack([C, b])) if len(rows) else 0
        rec = {'unknowns': len(U), 'equations': len(rows), 'rank': int(r), 'consistent': bool(rab == r)}
        if r == len(U) and rab == r:
            x = np.linalg.lstsq(C, b, rcond=None)[0]
            xi = np.rint(x).astype(int)
            exact = bool((np.array(rows, dtype=np.int64) @ xi == np.array(rhs, dtype=np.int64)).all())
            rec.update(unique=True, integral=bool(np.abs(x - xi).max() < 1e-7) and exact,
                       zero_one=bool(set(xi.tolist()) <= {0, 1}), solution=dict(zip(U, xi.tolist())))
        else:
            rec['unique'] = False
        if truth is not None:
            t = np.array([truth[y][z] for z in U], dtype=np.int64)
            rec['truth_ok'] = bool((np.array(rows, dtype=np.int64) @ t == np.array(rhs, dtype=np.int64)).all()) if rows else True
        out[y] = rec
    return out


def complete(M, sol, sig, k):
    """(c): assemble the determined far-far graph and check it fully."""
    n = len(M)
    A = np.array(M, dtype=np.int64)
    for y, rec in sol.items():
        for z, v in rec['solution'].items():
            A[y, z] = v
    msgs = []
    if (A < 0).any():
        msgs.append('undetermined entries remain')
    if not (A == A.T).all():
        msgs.append('asymmetric: %d entries' % int((A != A.T).sum()))
    P = np.eye(n, dtype=np.int64)[sig]
    if not (P @ A @ P.T == A).all():
        msgs.append('not sigma-invariant')
    bad = check_counts(A.tolist(), k)
    if bad:
        msgs.append('%d lambda/mu or degree violations, e.g. %s' % (len(bad), bad[:3]))
    return msgs


def run(M, x0, blocks, truth=None, verbose=True):
    k = sum(1 for v in M[x0] if v == 1)
    sig = sigma_map(M, x0, blocks)
    bad = check_counts(M, k)
    sol = solve_rows(M, truth)
    rep = {'k': k, 'violations_a': len(bad), 'rows_with_unknowns': len(sol),
           'all_unique': all(r['unique'] for r in sol.values()),
           'inconsistent_rows': sum(1 for r in sol.values() if not r['consistent']),
           'nonbinary_rows': sum(1 for r in sol.values() if r.get('unique') and not (r['integral'] and r['zero_one'])),
           'rank_profile': sorted({(r['unknowns'], r['equations'], r['rank']) for r in sol.values()})[:6]}
    if truth is not None:
        rep['truth_satisfies_b'] = all(r['truth_ok'] for r in sol.values())
    if sol and rep['all_unique'] and not rep['inconsistent_rows'] and not rep['nonbinary_rows']:
        rep['complete_checks'] = complete(M, sol, sig, k) or ['srg(%d, %d, 1, 2) with sigma: OK' % (len(M), k)]
    if verbose:
        print({kk: v for kk, v in rep.items()})
        if bad:
            print('  (a) first violations:', bad[:5])
    return rep


def partial_from_graph(A, x0, blocks, c, d):
    """Hide every pair of roots that avoid blocks c and d (the far-far pairs), except {y, sigma y} (known 0)."""
    n = len(A)
    inner = [v for bl in blocks for v in bl]
    desc = set(blocks[c]) | set(blocks[d])
    far = [r for r in range(n) if r != x0 and r not in inner and not any(A[r][a] for a in desc)]
    M = [row[:] for row in A]
    sig = sigma_map(A, x0, blocks)
    for i in far:
        for j in far:
            if i != j and j != sig[i]:
                M[i][j] = -1
    return M, far


def selftest_bvls(reps=2, seed=1):
    sys.path.insert(0, r'C:/home/researcher/Desktop/c99_structures_lab/famille')
    from family_graphs import bvls_243
    V, adjl = bvls_243()
    V = [tuple(v) for v in V]
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    A = [[0] * n for _ in range(n)]
    for i, nb in enumerate(adjl):
        for j in nb:
            A[i][j] = 1
    x0 = idx[tuple([0] * len(V[0]))]
    N0 = [j for j in range(n) if A[x0][j]]
    blocks, seen = [], set()
    for a in N0:
        if a in seen:
            continue
        b = idx[tuple((-x) % 3 for x in V[a])]
        blocks.append([a, b]); seen |= {a, b}
    rng = random.Random(seed)
    ok = True
    for rep in range(reps):
        c, d = rng.sample(range(len(blocks)), 2)
        M, far = partial_from_graph(A, x0, blocks, c, d)
        print('BvLS rep %d: blocks c=%d d=%d, far-far vertices %d' % (rep, c, d, len(far)))
        r = run(M, x0, blocks, truth=A)
        ok &= r['violations_a'] == 0 and r['truth_satisfies_b'] and r['inconsistent_rows'] == 0
        # negative control: flip one known edge between a described root and a far-far root
        Mb = [row[:] for row in M]
        inner = {v for bl in blocks for v in bl}
        y = far[0]
        w = next(u for u in range(n) if u != x0 and u not in inner and u not in far and Mb[u][y] >= 0)
        Mb[w][y] = Mb[y][w] = 1 - Mb[w][y]
        rb = run(Mb, x0, blocks, verbose=False)
        caught = rb['violations_a'] > 0 or rb['inconsistent_rows'] > 0
        print('  negative control (flipped known edge %d-%d): %s' % (w, y, 'caught' if caught else 'MISSED'))
        ok &= caught
    print('SELFTEST', 'OK' if ok else 'FAILED')
    return ok


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest-bvls':
        selftest_bvls(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
    else:
        D = json.load(open(sys.argv[1]))
        run(D['adj'], D['x0'], D['blocks'])
