"""Exact, standard-library proof of six-ribbon star restrictions (note 239).

The saturated 3-eigenvectors are from the proof supplied by the user.
This extends its one-chord argument to arbitrary chord stars. No LP or
floating-point eigensolver is used. Run to rebuild the finite certificate.
"""
from itertools import combinations
import json
from pathlib import Path


def ribbon(twist):
    a = [[0]*18 for _ in range(18)]
    for i in range(6):
        for off in (0, 6):
            nxt = off+i+1 if i < 5 else (6-off if twist else off)
            for u, v in combinations((off+i, nxt, 12+i), 2):
                a[u][v] = a[v][u] = 1
    return a


F = [3, 0, -3, -3, 0, 3]*2 + [2, -2, -4, -2, 2, 4]
G = [0, -3, -3, 0, 3, 3]*2 + [-2, -4, -2, 2, 4, 2]


def deficit(a):
    return [[2-a[u][v]-sum(a[u][w]*a[v][w] for w in range(18))
             for v in range(18)] for u in range(18)]


def local_ok(a):
    d = deficit(a)
    return all(d[u][v] >= 0 for u, v in combinations(range(18), 2))


def pair_obstruction(a, h):
    d = deficit(a)
    for u, v in combinations(range(18), 2):
        if a[u][v] or d[u][v] <= 0:
            continue
        allowed = [w for w in range(18) if w not in (u, v)
                   and d[u][w] > 0 and d[v][w] > 0
                   and all(a[t][u]+a[t][v]+a[t][w] <= 2-int(t in (u, v, w))
                           for t in range(18))]
        sums = {0}
        for w in allowed:
            sums |= {s+h[w] for s in sums}
        if -h[u]-h[v] not in sums:
            return {"pair": [u, v], "allowed": allowed,
                    "initial": h[u]+h[v], "other_sums": sorted(sums)}
    return None


def main():
    records = []
    for twist in (0, 1):
        base = ribbon(twist)
        for hub in (0, 12):
            candidates = []
            for v in range(18):
                if v == hub or base[hub][v]:
                    continue
                a = [r[:] for r in base]
                a[hub][v] = a[v][hub] = 1
                if local_ok(a):
                    candidates.append(v)
            h = G if hub == 0 else [(F[v]+G[v])//3 for v in range(18)]
            counts = {"local": 0, "plane": 0, "arithmetic": 0}
            left = []
            ruled = []
            local_survivors = []
            for bits in range(1, 1 << len(candidates)):
                targets = [v for k, v in enumerate(candidates) if bits >> k & 1]
                a = [r[:] for r in base]
                for v in targets:
                    a[hub][v] = a[v][hub] = 1
                if not local_ok(a):
                    counts["local"] += 1
                    continue
                local_survivors.append(targets)
                p = 2*F[hub]*sum(F[v] for v in targets)
                q = F[hub]*sum(G[v] for v in targets)+G[hub]*sum(F[v] for v in targets)
                r = 2*G[hub]*sum(G[v] for v in targets)
                if p > 0 or r > 0 or p*r-q*q < 0:
                    counts["plane"] += 1
                    continue
                assert all(sum(a[u][v]*h[v] for v in range(18)) == 3*h[u]
                           for u in range(18))
                obs = pair_obstruction(a, h)
                if obs:
                    counts["arithmetic"] += 1
                    ruled.append({"targets": targets, "obstruction": obs})
                else:
                    left.append(targets)
            expected = [] if hub == 0 else [[4, 9], [3, 10], [14, 16]]
            assert left == expected
            records.append({"twist": twist, "hub": hub, "candidates": candidates,
                            "counts": counts, "local_survivors": local_survivors,
                            "left": left, "harmonic_vector": h, "ruled": ruled})
    path = Path(__file__).resolve().parents[2]/"data/codex_ribbon_six_star.json"
    path.write_text(json.dumps(records, indent=2)+"\n", encoding="utf-8")
    for row in records:
        print({k: row[k] for k in ("twist", "hub", "counts", "left")})
    print("All cases covered by exact local budgets, 2x2 forms, and subset sums.")


if __name__ == "__main__":
    main()
