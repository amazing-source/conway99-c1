"""Negative self-test of srg_sat: an edge with two common neighbours must make the 9-vertex instance UNSAT."""
import sys
import srg_sat as S
n, k, l, m, _ = S.instance_selftest()
f = {(0, 1): True, (0, 2): True, (1, 2): True, (0, 3): True, (1, 3): True}
enc, e = S.encode(n, k, l, m, f)
S.write_dimacs(enc, sys.argv[1])
