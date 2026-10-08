"""C1, lab session, 2026-10-08. Reproduce the September random generic balls (structures-lab
scripts/random_balls_star_calibration.py, seed 2609, same filters: K >= 0, rank_7(3I - B) = 35, tau non-square mod 7)
and keep the TRIANGLE-FREE ones (P = 0 locally), with c4 at the edge (0, 12) at most 2; write each as {"adjacency": 36x36}.
  python make_random_balls.py <path to structures-lab scripts dir> <out dir> [how many] [seed]"""
import random, sys, json, os
sys.path.insert(0, sys.argv[1])
from star_shadows import build, ball_data, N, part
out = sys.argv[2]; want = int(sys.argv[3]) if len(sys.argv) > 3 else 3; rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 2609)
def rand_inv(rng):
    xs = list(range(12)); rng.shuffle(xs); f = [None] * 12
    for i in range(0, 12, 2): f[xs[i]], f[xs[i + 1]] = xs[i + 1], xs[i]
    return f
kept = 0; got = 0; tried = 0
while got < want and tried < 5000:
    a, b, c = rand_inv(rng), rand_inv(rng), rand_inv(rng); hol = list(range(12)); rng.shuffle(hol)
    adj = build(a, b, c, hol); tried += 1
    Bm, H, tau, rk = ball_data(adj)
    if rk != 35 or tau % 7 in (0, 1, 2, 4): continue
    B2 = [[sum(Bm[p][r] * Bm[r][q] for r in range(N)) for q in range(N)] for p in range(N)]
    if any(12 * (p == q) - Bm[p][q] + 2 - B2[p][q] - (part(p) == part(q)) < 0 for p in range(N) for q in range(N)): continue
    kept += 1
    tri = sum(1 for p in range(N) for q in adj[p] for r in adj[q] if p < q < r and r in adj[p])
    B3 = sum(B2[0][r] * Bm[r][12] for r in range(N)); c4 = B3 - 5
    print("calibration ball %d: tau mod 7 = %d, triangles %d, c4(0,12) = %d" % (kept, tau % 7, tri, c4), flush=True)
    if tri == 0 and 0 <= c4 <= 2 and 12 in adj[0]:
        got += 1; json.dump({"adjacency": Bm, "source": "seed 2609, calibration ball %d" % kept}, open(os.path.join(out, "random_ball_%d.json" % kept), "w"))
print("written %d triangle-free balls after %d tries" % (got, tried))
