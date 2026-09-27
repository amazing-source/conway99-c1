r"""Finish line (C), C1 27/09: y-pair enumeration reduced by Gamma = Aut(U)/W(R) (full-rank lattices, gamma_fullrank.py).
y1: W-dominant (y_pairs.dominant_y1), then one representative per Gamma-orbit (Gamma preserves the fundamental chamber).
y2: W(R cap y1-perp)-dominant candidates (y2_engine), then one representative per orbit of Stab_Gamma(y1) x {+-1}
(Stab_Gamma(y1) preserves R cap y1-perp and its positive system, hence the candidate set; -y2 is merged when it is a candidate).
Complete up to Aut(U) x {signs}: every frame pair is Aut(U)-equivalent to a listed one (up to the order of y1, y2).
Usage: python y_pairs_gamma.py <envelope.json> <gamma.json> <out.json> [--max-seconds S] [--plan] [--chunk k/n]
--plan: stop after the y1 stage and write its stats (y1_orbits = number of y1 tasks).
--chunk k/n: only the y1 representatives reps1[k::n]; the n chunk files together give exactly the full list
(the y2 reduction is done per y1 representative, so the union of the chunks is the single-run list).
--from-plan plan.json: take the y1 representatives from a --plan file (same envelope and Gamma) instead of recomputing them.
--stream PATH ('-' = stdout): write the pairs as JSON lines {"o": y1 orbit index, "y1": [24], "y2": [24]} (AMBIENT
coordinates, exact fraction strings, grouped by y1 orbit) as they are found, instead of holding them; the last line is
{"end": true, "chunk": [k, n], "pairs": N, "complete": bool, "sha256": sha256 of all the pair lines (each with its '
')}.
out.json then gets the stats only (pairs = [], "streamed": N, "sha256")."""
import hashlib, json, math, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y_pairs import setup, dominant_y1, root_system
from envelope_trap import inverse_exact
from y2_engine import Y2Engine


def orbit_reps(vectors, mats, sign=False):
    """vectors: int array (n x 24) of coefficient rows; mats: list of int matrices (a -> a @ M). Returns (rep indices, orbit sizes)."""
    key = {tuple(v): k for k, v in enumerate(vectors)}
    parent = list(range(len(vectors)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for k, v in enumerate(vectors):
        imgs = [v @ M for M in mats]
        if sign:
            imgs += [-w for w in imgs]
        for w in imgs:
            j = key.get(tuple(int(x) for x in w))
            if j is not None:
                ra, rb = find(k), find(j)
                if ra != rb:
                    parent[ra] = rb
    groups = {}
    for k in range(len(vectors)):
        groups.setdefault(find(k), []).append(k)
    reps = [min(g) for g in groups.values()]
    sizes = [len(g) for g in groups.values()]
    return reps, sizes


def basis_sha(B):
    return hashlib.sha256(json.dumps([[str(x) for x in row] for row in B]).encode()).hexdigest()[:16]


def gamma_in_basis(gam, B, Gi, Bf, R):
    """Gamma matrices in THIS run's LLL basis B (a -> a @ M), each one VERIFIED (27/09 night: the LLL basis of setup() differs
    between the lab PC and this laptop, and a Gamma file made on the other machine is then a set of non-isometries).
    A file that carries its basis ('basis', rows as fraction strings) is converted exactly: with P = B Bg^-1 (unimodular),
    M' = P M P^-1. Every matrix must preserve the Gram matrix and permute the simple roots (= fix the chamber); else abort."""
    mats = [np.array(M, dtype=np.int64) for M in gam['matrices']]
    gens = [np.array(M, dtype=np.int64) for M in gam.get('generator_matrices', [])]
    conv = False
    if 'basis' in gam:
        Bg = [[F(x) for x in row] for row in gam['basis']]
        Bq = [[F(x) for x in row] for row in B]
        if Bg != Bq:
            Bgi, Bqi = inverse_exact(Bg), inverse_exact(Bq)
            mul = lambda X, Y: [[sum(X[i][k] * Y[k][j] for k in range(24)) for j in range(24)] for i in range(24)]
            P, Pi = mul(Bq, Bgi), mul(Bg, Bqi)
            assert all(x.denominator == 1 for row in P + Pi for x in row), 'Gamma basis is not a basis of this lattice'
            P = np.array([[int(x) for x in row] for row in P], dtype=object)
            Pi = np.array([[int(x) for x in row] for row in Pi], dtype=object)
            mats = [np.array((P.dot(M.astype(object))).dot(Pi), dtype=np.int64) for M in mats]
            gens = [np.array((P.dot(M.astype(object))).dot(Pi), dtype=np.int64) for M in gens]
            conv = True
    G = np.array(Gi, dtype=np.int64)
    S = root_system(R)[0]
    Sc = np.rint(S @ np.linalg.inv(Bf)).astype(np.int64)
    simp = {tuple(r) for r in Sc.tolist()}
    for M in mats + gens:
        if not (np.array_equal(M @ G @ M.T, G) and all(tuple((sv @ M).tolist()) in simp for sv in Sc)):
            raise SystemExit('ABORT: a Gamma matrix is not a chamber-preserving isometry in this basis '
                             '(Gamma file from another machine without its basis?)')
    if gens:                                                           # generators must generate exactly the listed group
        keys = {M.tobytes() for M in mats}
        assert all((X @ M).tobytes() in keys for X in mats[:50] for M in gens), 'generators outside the listed Gamma'
    return mats, gens, conv


def main():
    rec_ = json.load(open(sys.argv[1]))
    gam = json.load(open(sys.argv[2]))
    outp = sys.argv[3]
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 3600
    assert gam['id'] == rec_['id']
    gsha = hashlib.sha256(open(sys.argv[2], 'rb').read()).hexdigest()[:16]
    t0 = time.time()
    B, Gi, Bf, R, X3, Snew = setup(rec_['gens'])
    bsha = basis_sha(B)
    mats, gens, converted = gamma_in_basis(gam, B, Gi, Bf, R)
    if '--from-plan' in sys.argv:
        pl = json.load(open(sys.argv[sys.argv.index('--from-plan') + 1]))
        assert pl['id'] == rec_['id'] and pl['plan']['gamma'] == len(mats) and pl['gamma_sha'] == gsha
        assert pl.get('basis_sha') == bsha, 'plan made in another LLL basis'
        Y = np.array(pl['y1_reps'], dtype=np.int64).reshape(-1, 24)
        Yf = Y.astype(float) @ Bf
        info = dict(pl['plan'])
        reps1 = list(range(len(Y)))
    else:
        Y, Yf, info = dominant_y1(B, Gi, Bf, R, X3, Snew)
        reps1, sizes1 = orbit_reps(Y, gens if gens else mats)          # Y is Gamma-invariant: generators suffice
        info.update(id=rec_['id'], roots=rec_['roots'], gamma=len(mats), y1_orbits=len(reps1), gamma_verified=True,
                    gamma_converted=converted)
    print(json.dumps(info), flush=True)
    if '--plan' in sys.argv:
        info['seconds'] = round(time.time() - t0, 1)
        json.dump({'id': rec_['id'], 'plan': info, 'gamma_sha': gsha, 'basis_sha': bsha,
                   'y1_reps': [[int(x) for x in Y[r]] for r in reps1]}, open(outp, 'w'))
        return
    if '--chunk' in sys.argv:
        k, n = map(int, sys.argv[sys.argv.index('--chunk') + 1].split('/'))
        reps1 = reps1[k::n]
        info.update(chunk=[k, n], y1_orbits_chunk=len(reps1))
    eng = Y2Engine(B, Gi, Bf, R, X3, Snew)
    # exact ambient coordinates by integer arithmetic (same strings as str(Fraction)): v = a @ (d B) / d
    dB = 1
    for row in B:
        for x in row:
            dB = dB * F(x).denominator // math.gcd(dB, F(x).denominator)
    BI = np.array([[int(F(x) * dB) for x in row] for row in B], dtype=object)

    def q24(a):
        num = np.array([int(v) for v in a], dtype=object).dot(BI)
        out_ = []
        for v in num:
            v = int(v); g = math.gcd(v, dB); nn, dd = v // g, dB // g
            out_.append(str(nn) if dd == 1 else '%d/%d' % (nn, dd))
        return out_
    stream = sys.argv[sys.argv.index('--stream') + 1] if '--stream' in sys.argv else None
    sfh = (sys.stdout if stream == '-' else open(stream, 'w', newline=chr(10))) if stream else None
    shash = hashlib.sha256()
    nstream = 0
    pairs = []
    tot = {'y2_candidates': 0, 'y2_orbits': 0, 'truncated': 0}
    for r in reps1:
        if time.time() - t0 > ms:
            info['timeout'] = True
            break
        y1c = Y[r]
        stab = [M for M in mats if np.array_equal(y1c @ M, y1c)]
        Y2, st = eng.pairs_for(Yf[r], t0=time.time(), max_seconds=ms)
        tot['truncated'] += int(st.get('truncated', False))
        tot['y2_candidates'] += len(Y2)
        if len(Y2) == 0:
            continue
        reps2, _ = orbit_reps(Y2, stab, sign=True)
        tot['y2_orbits'] += len(reps2)
        if sfh is not None:
            y1s = q24(y1c)
            for k in reps2:
                line = json.dumps({'o': int(r), 'y1': y1s, 'y2': q24(Y2[k])}) + chr(10)
                sfh.write(line); shash.update(line.encode()); nstream += 1
            sfh.flush()
            continue
        for k in reps2:
            pairs.append((y1c, Y2[k]))
    info.update(tot)
    info['pairs'] = len(pairs) if sfh is None else nstream
    info['complete'] = not info.get('timeout') and tot['truncated'] == 0
    info['seconds'] = round(time.time() - t0, 1)
    if sfh is not None:
        info.update(streamed=nstream, sha256=shash.hexdigest())
        sfh.write(json.dumps({'end': True, 'id': rec_['id'], 'chunk': info.get('chunk', [0, 1]), 'pairs': nstream,
                              'complete': info['complete'], 'sha256': shash.hexdigest()}) + chr(10))
        sfh.flush()
        if sfh is not sys.stdout:
            sfh.close()
    print(json.dumps(info), flush=True, file=sys.stderr if stream == '-' else sys.stdout)
    json.dump({'id': rec_['id'], 'pairs': [[q24(a), q24(b)] for a, b in pairs], 'stats': info,
               'note': 'complete up to Aut(U) x signs (Gamma from gamma_fullrank.py, |Gamma| checked against the table)'},
              open(outp, 'w'))


if __name__ == '__main__':
    main()
