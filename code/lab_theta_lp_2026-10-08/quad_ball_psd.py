"""C1, lab session, 2026-10-09. Is the positivity condition on the neighbourhood of a quadrangle satisfiable at all?
S = N(Q), 44 vertices: four walls of 12 (ten free points in five mate pairs, two ears shared with the next wall).
Edges: mates; the four cross matchings between consecutive walls; between opposite walls every free point has two
neighbours. Necessary: 3I - A_S + J/9 >= 0 and 4I + A_S - (2/11) J >= 0.
Random structures (no prism), then a local search (swaps inside the matchings and 2-switches of the opposite-wall
graphs) minimising the violation.     python quad_ball_psd.py [steps] [seed]      One process, about a minute."""
import sys, random
import numpy as np
STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 20000; random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
walls = "vawb"; pts = []
free = {u: [(u, i) for i in range(10)] for u in walls}                 # free points, mates (u, 2j) - (u, 2j+1)
ears = {("v", "a"): "a'", ("a", "w"): "p", ("w", "b"): "q", ("b", "v"): "b'"}   # ear of the side u-u'
for u in walls: pts += free[u]
pts += list(ears.values()); ix = {p: i for i, p in enumerate(pts)}; n = len(pts); assert n == 44
nxt = {"v": "a", "a": "w", "w": "b", "b": "v"}; prv = {b: a for a, b in nxt.items()}; opp = {"v": "w", "w": "v", "a": "b", "b": "a"}


def build(state):
    A = np.zeros((n, n))
    def e(x, y): A[ix[x], ix[y]] = A[ix[y], ix[x]] = 1
    for u in walls:
        for j in range(5): e((u, 2 * j), (u, 2 * j + 1))
    for u in walls:                                   # matching between wall u and wall nxt[u]
        for x, y in state["pi"][u].items(): e(x, y)
    for key in ("vw", "ab"):
        for x, y in state["D"][key]: e(x, y)
    return A


def random_state():
    st = {"pi": {}, "D": {}}
    for u in walls:
        u2 = nxt[u]
        # domain inside S: free points of u and the ear of the PREVIOUS side at u (the mate of the other Q-neighbour);
        # range inside S: free points of u2 and the ear of the NEXT side at u2. The ear of the side u-u2 itself is fixed.
        src = free[u] + [ears[(prv[u], u)]]; dst = free[u2] + [ears[(u2, nxt[u2])]]
        while True:
            random.shuffle(dst)
            if dst[-1] != ears[(u2, nxt[u2])] or True: break
        st["pi"][u] = dict(zip(src, dst))
    for key, (u, u2) in (("vw", ("v", "w")), ("ab", ("a", "b"))):
        # 2-regular bipartite graph between free points; a free point matched to an ear of the opposite wall by a pi
        # already has one of its two neighbours there
        need1 = {x: 2 for x in free[u]}; need2 = {y: 2 for y in free[u2]}
        for w_ in walls:
            for x, y in st["pi"][w_].items():
                for (a, b) in ((x, y), (y, x)):
                    if isinstance(a, tuple) and not isinstance(b, tuple):
                        # b is an ear; it belongs to two walls; if one of them is opposite to the wall of a, count it
                        for side, name in ears.items():
                            if name == b and opp[a[0]] in side:
                                if a[0] == u: need1[a] -= 1
                                elif a[0] == u2: need2[a] -= 1
        for _ in range(2000):
            L = [x for x, c in need1.items() for _ in range(c)]; R = [y for y, c in need2.items() for _ in range(c)]
            if len(L) != len(R): break
            random.shuffle(R); E = list(zip(L, R))
            if len(set(E)) == len(E): st["D"][key] = E; break
        else: return None
        if key not in st["D"]: return None
    return st


def score(A):
    J = np.ones((n, n)); a = np.linalg.eigvalsh(3 * np.eye(n) - A + J / 9)[0]; b = np.linalg.eigvalsh(4 * np.eye(n) + A - 2 * J / 11)[0]
    return min(a, 0) + min(b, 0), a, b


def mutate(st):
    new = {"pi": {u: dict(d) for u, d in st["pi"].items()}, "D": {k: list(v) for k, v in st["D"].items()}}
    if random.random() < 0.5:
        u = random.choice(walls); d = new["pi"][u]; x, y = random.sample([k for k in d if isinstance(k, tuple) and isinstance(d[k], tuple)], 2)
        d[x], d[y] = d[y], d[x]
    else:
        key = random.choice(("vw", "ab")); E = new["D"][key]; i, j = random.sample(range(len(E)), 2)
        (x1, y1), (x2, y2) = E[i], E[j]
        if (x1, y2) in E or (x2, y1) in E: return None
        E[i], E[j] = (x1, y2), (x2, y1)
    return new


st = None
while st is None: st = random_state()
cur, a, b = score(build(st)); best = cur; t = 0.3
print("start: smallest eigenvalue of 3I - A + J/9: %.3f ; of 4I + A - 2J/11: %.3f" % (a, b))
for step in range(STEPS):
    cand = mutate(st)
    if cand is None: continue
    sc, a2, b2 = score(build(cand))
    if sc >= cur or random.random() < np.exp((sc - cur) / t):
        st, cur, a, b = cand, sc, a2, b2
        if cur > best: best = cur
    t = max(0.01, t * 0.9997)
    if cur == 0: print("step %d: BOTH positivity conditions hold (%.3f, %.3f)" % (step, a, b)); break
print("end: violation %.3f ; smallest eigenvalues %.3f and %.3f ; degrees %s" % (cur, a, b, sorted(set(build(st).sum(1).astype(int).tolist()))))
