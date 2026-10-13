"""Lab session, 2026-10-13. For a graph with a small automorphism group: all elements of Aut, the elements of 3-power
order, whether they form a group (normal Sylow 3-subgroup), its order, element orders, abelian or not, and the
elements acting without fixed point (semiregular elements); also the numbers of fixed points of the involutions.
python -I sylow_info.py <edge files ...>"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aut_tools as T, regular_subgroups as RS
for path in sys.argv[1:]:
    A = T.load(path); n = len(A); ident = tuple(range(n)); o, gens, base, sizes = T.aut_group(A)
    if o > 20000: print("%s: |Aut| = %d, too large for this listing" % (os.path.basename(path), o)); continue
    G = RS.generate([tuple(g) for g in gens], ident); ords = {g: RS.order(g, ident) for g in G}
    P = [g for g in G if ords[g] in (1, 3, 9, 27, 81, 243)]; isgroup = RS.generate(P, ident) == set(P)
    fix = lambda g: sum(1 for x in range(n) if g[x] == x)
    semi = collections.Counter(ords[g] for g in P if g != ident and fix(g) == 0)
    fixed3 = collections.Counter(fix(g) for g in P if g != ident and fix(g) > 0)
    inv = collections.Counter(fix(g) for g in G if ords[g] == 2)
    ab = all(RS.mul(a, b) == RS.mul(b, a) for a in P[:60] for b in P)
    print("%s: |Aut| = %d; element orders %s" % (os.path.basename(path), o, sorted(collections.Counter(ords.values()).items())))
    print("    3-elements: %d, form a subgroup: %s, abelian (test): %s, orders %s" % (len(P), isgroup, ab, sorted(collections.Counter(ords[g] for g in P).items())))
    print("    fixed-point-free 3-elements by order: %s; 3-elements with fixed points (number of fixed points: count): %s" % (sorted(semi.items()), sorted(fixed3.items())))
    print("    involutions by number of fixed points: %s" % sorted(inv.items()))
