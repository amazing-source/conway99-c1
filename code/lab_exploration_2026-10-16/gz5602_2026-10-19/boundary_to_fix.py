"""Convert one 20-vertex boundary of Codex's 5602 cover (gz5602_boundary20_cover.json, main 36e48a62) into the --fix
format of full5602.py (LAB 19/10/2026), for an independent solver check of its exclusion.
Codex's indexing: rectangles = CORE + GRIDS = [03, 12, 01, 02, 13, 23, 45, 46, 56]; label u = 4 r + 2 s_a + s_b
(letters 2*line + s).  Fixed: the core adjacency (labels 0..7), and for the 12 C3-grid labels (24..35) their core
neighbours (bit masks over 0..7).  Everything else is left to full5602.py.
usage: python boundary_to_fix.py <cover.json> <orbit> <boundary index> <out.json>"""
import json
import sys

d = json.load(open(sys.argv[1]))
orbit, bi = int(sys.argv[2]), int(sys.argv[3])
case = d["orbit_reduction"]["orbits"][orbit]["boundaries"]["cases"][bi]
RECTS = [(0, 3), (1, 2), (0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 6)]


def lab(u):
    r, rest = divmod(u, 4)
    return [list(RECTS[r]), rest // 2, rest % 2]


pairs = []
K = case["core_adjacency"]
for i in range(8):
    for j in range(i + 1, 8):
        pairs.append([lab(i), lab(j), K[i][j]])
for k, mask in enumerate(case["core_neighbours_of_grid_vertices"]):
    g = 24 + k
    for v in range(8):
        pairs.append([lab(g), lab(v), (mask >> v) & 1])
json.dump({"source": "Codex 36e48a62 gz5602_boundary20_cover.json", "orbit": orbit, "boundary_index": bi, "pairs": pairs},
          open(sys.argv[4], "w"))
print(len(pairs), "fixed pairs")
