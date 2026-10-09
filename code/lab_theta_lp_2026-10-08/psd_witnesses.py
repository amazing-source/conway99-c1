"""C1, lab session, 2026-10-09. Exact witnesses for the "NOT PSD" verdicts of the surveys: for every single extra edge
or identification of the five-centre window, and of the closed cycles of length 6, 7, 8, whose block
Q- = 27I - 9A + J or Q+ = 44I + 11A - 2J is not positive semidefinite, an INTEGER vector v with v^T Q v < 0.
  python psd_witnesses.py        One process, seconds."""
import itertools, json, collections
import numpy as np
import support_masks as S


def witness(n, edges):
    A = np.zeros((n, n), dtype=np.int64)
    for x, y in edges: A[x, y] = A[y, x] = 1
    for name, Q in (("Q-", 27 * np.eye(n, dtype=np.int64) - 9 * A + 1), ("Q+", 44 * np.eye(n, dtype=np.int64) + 11 * A - 2)):
        w, V = np.linalg.eigh(Q.astype(float))
        if w[0] < -1e-7:
            for scale in (100, 1000, 10000, 100000):
                v = np.round(V[:, 0] * scale).astype(np.int64); val = int(v @ Q @ v)
                if val < 0: return name, [int(t) for t in v], val, float(w[0])
            raise SystemExit("no integer witness found (eigenvalue %g)" % w[0])
    return None


def local_ok(n, edges):
    adj = [set() for _ in range(n)]
    for x, y in edges: adj[x].add(y); adj[y].add(x)
    return all(len(adj[i] & adj[j]) <= (1 if j in adj[i] else 2) for i in range(n) for j in range(i + 1, n))


def cases(names, E0):
    ix = {s: i for i, s in enumerate(names)}; base = set(tuple(sorted(e)) for e in E0); n = len(names)
    for x, y in itertools.combinations(names, 2):
        if tuple(sorted((ix[x], ix[y]))) in base: continue
        yield "%s-%s" % (x, y), n, E0 + [(ix[x], ix[y])]
        keep = [s for s in names if s != y]; jx = {s: i for i, s in enumerate(keep)}; jx[y] = jx[x]; E = set(); bad = False
        for p, q in E0:
            u, v = jx[names[p]], jx[names[q]]
            if u == v: bad = True; break
            E.add((min(u, v), max(u, v)))
        if not bad: yield "%s=%s" % (x, y), len(keep), sorted(E)


out = {}; summary = collections.Counter(); worst = 0.0
names, ix, E0 = S.window(5)
fam = [("window5", names, E0)]
for m in (6, 7, 8):
    for MO in (False, True):
        nm = ["a%d" % i for i in range(m)] + ["b%d" % i for i in range(m)] + ["c%d" % i for i in range(m)]; jx = {s: i for i, s in enumerate(nm)}; E = []
        for i in range(m):
            if i < m - 1 or not MO: an, bn = "a%d" % ((i + 1) % m), "b%d" % ((i + 1) % m)
            else: an, bn = "b0", "a0"
            for x, y in (("c%d" % i, "a%d" % i), ("c%d" % i, an), ("a%d" % i, an), ("c%d" % i, "b%d" % i), ("c%d" % i, bn), ("b%d" % i, bn)): E.append((jx[x], jx[y]))
        fam.append(("closed%d %s" % (m, "moebius" if MO else "cylinder"), nm, E))
for tag, nm, E in fam:
    wz = witness(len(nm), E); summary[(tag, "clean: " + ("not PSD" if wz else "PSD"))] += 1
    if wz: out[tag + " clean"] = {"block": wz[0], "v": wz[1], "value": wz[2]}; worst = min(worst, wz[3]) if worst else wz[3]
    for label, n, edges in cases(nm, E):
        if not local_ok(n, edges): summary[(tag, "local")] += 1; continue
        wz = witness(n, edges)
        if wz is None: summary[(tag, "PSD (float): goes to the mask system")] += 1; continue
        out["%s %s" % (tag, label)] = {"block": wz[0], "v": wz[1], "value": wz[2]}; summary[(tag, "not PSD, integer witness")] += 1
        worst = max(worst, wz[3])
json.dump(out, open("psd_witnesses.json", "w"))
for k, v in sorted(summary.items()): print("%-18s %-40s %d" % (k[0], k[1], v))
print("integer witnesses written: %d; least negative eigenvalue among them (float, of the integer block): %.4f" % (len(out), worst))
