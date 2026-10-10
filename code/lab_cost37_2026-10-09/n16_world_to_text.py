"""C1, lab session, 2026-10-10. Convert one of Codex's typed worlds of norm 16 (JSON: base_adjacency, domains with
cell = [p, q], multiplicity, neighbour_masks) into the text input of n16cell.c.
python n16_world_to_text.py <typed world json> <output txt>"""
import sys, json
D = json.load(open(sys.argv[1])); A = D["base_adjacency"]; n = len(A)
out = ["%d %d" % (n, len(D["domains"]))] + ["".join(str(int(x)) for x in row) for row in A]
for d in D["domains"]:
    out.append("%d %d %d %d" % (d["cell"][0], d["cell"][1], d["multiplicity"], len(d["neighbour_masks"])))
    out.append(" ".join(str(m) for m in d["neighbour_masks"]))
open(sys.argv[2], "w", newline="\n").write("\n".join(out) + "\n")
print("written %s: %d base vertices, %d domains, %d masks" % (sys.argv[2], n, len(D["domains"]), sum(len(d["neighbour_masks"]) for d in D["domains"])))
