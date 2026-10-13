"""Lab session, 2026-10-13. DIMACS file for "the graph has a coclique of size 45 (Hoffman bound)":
x in {0,1}^243, no edge inside, every vertex outside has exactly 5 neighbours inside. Optional unit clause: a given
vertex is inside (enough for a vertex-transitive graph).   python hoffman45_cnf.py <edge file> <out.cnf> [vertex]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hoffman_cocliques import load
n, adj, E = load(sys.argv[1]); cl = []; nv = [n]
def new(): nv[0] += 1; return nv[0]
def counter(lits, kmax):
    prev = None
    for x in lits:
        cur = [new() for _ in range(kmax + 1)]
        if prev is None:
            cl.append([-x, cur[0]]); cl.append([x, -cur[0]])
            for j in range(1, kmax + 1): cl.append([-cur[j]])
        else:
            for j in range(kmax + 1):
                cl.append([-prev[j], cur[j]])
                if j == 0: cl.append([-x, cur[j]]); cl.append([-cur[j], prev[j], x])
                else: cl.append([-x, -prev[j - 1], cur[j]]); cl.append([-cur[j], prev[j], x]); cl.append([-cur[j], prev[j], prev[j - 1]])
        prev = cur
    return prev
for a, b in E: cl.append([-(a + 1), -(b + 1)])
for v in range(n):
    r = counter([w + 1 for w in sorted(adj[v])], 5); cl.append([v + 1, r[4]]); cl.append([v + 1, -r[5]])
if len(sys.argv) > 3: cl.append([int(sys.argv[3]) + 1])
with open(sys.argv[2], "w", newline="\n") as f:
    f.write("p cnf %d %d\n" % (nv[0], len(cl)))
    for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
print("written %s: %d variables, %d clauses" % (sys.argv[2], nv[0], len(cl)))
