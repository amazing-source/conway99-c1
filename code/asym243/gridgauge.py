"""Valid gauge for grid covers.  Each cell carries the standard K3xK3 labelling (r,s) -> 3r+s, so a cell may only be
relabelled by an automorphism of the grid (order 72).  Aut(grid) is transitive on points and the stabiliser of point 0
is transitive on its 4 neighbours and on its 4 non-neighbours.  Hence, for a chosen reference matching sigma_{R,j}
(one per cell j), WLOG sigma_{R,j}(0) = 0 and sigma_{R,j}(1) in {1, 4}   (1 ~ 0, 4 not ~ 0 in the grid)."""
def add_gauge(m, var, cells, ref):
    """ref: dict cell j -> reference cell R (distinct cells j get independent normalisations)."""
    for j, R in ref.items():
        a0, a1 = cells[R][0], cells[R][1]
        m.Add(var[(a0, cells[j][0])] == 1)
        m.AddBoolOr([var[(a1, cells[j][1])], var[(a1, cells[j][4])]])
