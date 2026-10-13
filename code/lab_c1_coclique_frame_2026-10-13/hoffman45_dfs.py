"""Lab session, 2026-10-13. Independent exact check (integers only, no solver) of "coclique of size 45 in a
srg(243,22,1,2)": x in {0,1}^243, a vertex in C has no neighbour in C, a vertex outside has exactly 5.
Depth-first search with propagation of these two rules; branching on an outside vertex with the fewest ways left.
python hoffman45_dfs.py <seconds> <edge file> [vertex forced in C]       One process, small memory."""
import sys, time
E = [tuple(map(int, l.split())) for l in open(sys.argv[2]) if l.strip()]; n = 1 + max(max(e) for e in E)
adj = [[] for _ in range(n)]
for a, b in E: adj[a].append(b); adj[b].append(a)
tl = float(sys.argv[1]); t0 = time.time(); nodes = 0; sols = 0; timeout = False
state = [-1] * n; cin = [0] * n; und = [len(adj[v]) for v in range(n)]      # -1 undecided, 0 out, 1 in
def assign(v, val, trail):
    """returns False on contradiction; records changes in trail"""
    stack = [(v, val)]
    while stack:
        v, val = stack.pop()
        if state[v] != -1:
            if state[v] != val: return False
            continue
        state[v] = val; trail.append(v)
        for w in adj[v]:
            und[w] -= 1
            if val: cin[w] += 1
        if val:
            for w in adj[v]:
                if state[w] == 1: return False
                if state[w] == -1: stack.append((w, 0))
        for w in adj[v] + [v]:
            if state[w] == 0:
                if cin[w] > 5 or cin[w] + und[w] < 5: return False
                if cin[w] == 5 and und[w]:
                    for u in adj[w]:
                        if state[u] == -1: stack.append((u, 0))
                elif cin[w] + und[w] == 5 and und[w]:
                    for u in adj[w]:
                        if state[u] == -1: stack.append((u, 1))
            elif state[w] == -1 and cin[w] > 0: stack.append((w, 0))
    return True
def undo(trail):
    for v in reversed(trail):
        val = state[v]; state[v] = -1
        for w in adj[v]:
            und[w] += 1
            if val: cin[w] -= 1
def search():
    global nodes, sols, timeout
    if timeout: return
    nodes += 1
    if nodes % 2000 == 0 and time.time() - t0 > tl: timeout = True; return
    best = None
    for v in range(n):
        if state[v] == 0 and und[v]:
            key = (und[v] - (5 - cin[v]), und[v])
            if best is None or key < best[0]: best = (key, v)
    if best is None:
        v = next((u for u in range(n) if state[u] == -1), None)
        if v is None:
            C = [u for u in range(n) if state[u] == 1]
            assert len(C) == 45 and all(state[w] == 0 for u in C for w in adj[u]); sols += 1; return
        cand = [v]
    else:
        cand = [u for u in adj[best[1]] if state[u] == -1][:1]
    u = cand[0]
    for val in (1, 0):
        trail = []
        if assign(u, val, trail): search()
        undo(trail)
        if timeout or sols: return
trail = []; ok = True
if len(sys.argv) > 3: ok = assign(int(sys.argv[3]), 1, trail)
if ok: search()
name = sys.argv[2].replace("\\", "/").split("/")[-1]
print("%s: %s (%d nodes, %.1f s)" % (name, "TIME OVER, no decision" if timeout else ("coclique of size 45 FOUND" if sols else "NO coclique of size 45%s (exhaustive search)" % (" through the given vertex" if len(sys.argv) > 3 else "")), nodes, time.time() - t0))
