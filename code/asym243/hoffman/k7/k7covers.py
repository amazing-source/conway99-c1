# All (Gamma, M): Gamma cubic on 14 vertices, M perfect matching in the complement, Gamma/M = K7 (simple, all 21 pairs once).
# Output: one line per labeled solution as graph6 of the 21-vertex encoding (14 + 7 matching vertices), for canonical dedup.
import sys
def g6dec(s):
    s = s.strip(); n = ord(s[0]) - 63; bits = []
    for ch in s[1:]:
        v = ord(ch) - 63; bits += [(v >> (5 - i)) & 1 for i in range(6)]
    adj = [set() for _ in range(n)]; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: adj[i].add(j); adj[j].add(i)
            k += 1
    return n, adj
def g6enc(n, adj):
    bits = [1 if j in adj[i] else 0 for j in range(1, n) for i in range(j)]
    bits += [0] * (-len(bits) % 6)
    return chr(n + 63) + "".join(chr(63 + int("".join(map(str, bits[i:i + 6])), 2)) for i in range(0, len(bits), 6))
out = open(sys.argv[2], "w"); total = 0
for gi, line in enumerate(open(sys.argv[1])):
    n, adj = g6dec(line)
    part = [-1] * n; pairs = []
    def ok_new(u, v):
        # edges between new super-vertex {u,v} and each existing one must be exactly 1
        for (p, q) in pairs:
            cnt = (p in adj[u]) + (q in adj[u]) + (p in adj[v]) + (q in adj[v])
            if cnt != 1: return False
        return True
    def rec():
        global total
        u = next((i for i in range(n) if part[i] < 0), None)
        if u is None:
            enc = [set(a) for a in adj] + [set() for _ in range(7)]
            for t, (p, q) in enumerate(pairs):
                enc[14 + t] |= {p, q}; enc[p].add(14 + t); enc[q].add(14 + t)
            out.write(g6enc(21, enc) + "\n"); total += 1; return
        for v in range(u + 1, n):
            if part[v] < 0 and v not in adj[u] and ok_new(u, v):
                part[u] = part[v] = len(pairs); pairs.append((u, v)); rec(); pairs.pop(); part[u] = part[v] = -1
    rec()
print("labeled solutions", total)
