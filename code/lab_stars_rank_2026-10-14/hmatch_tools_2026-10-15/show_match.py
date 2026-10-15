import json, sys, glob
for f in sorted(glob.glob(sys.argv[1]), key=lambda x: int(x.split('_')[-1].split('.')[0])):
    d = json.load(open(f))
    S = [frozenset(l) for l in d['labels']]; idx = {s: i for i, s in enumerate(S)}
    E = {tuple(sorted(e)) for e in d['edges']}
    adj = lambda a, b: tuple(sorted((idx[a], idx[b]))) in E
    L = lambda *x: frozenset(x)
    out = []
    for a in (0, 1, 2, 3):
        others = [y for y in range(14) if y not in (a, a ^ 1)]
        M = sorted({tuple(sorted((y, z))) for y in others for z in others if y < z and adj(L(a, y), L(a, z))})
        out.append("M%d=%s" % (a, [p for p in M if set(p) & {4, 5, 6, 7, 9}]))
    tl = [y for y in range(4, 14) if adj(L(0, y), L(1, y))]
    tm = [y for y in range(4, 14) if adj(L(2, y), L(3, y))]
    print(f.split('/')[-1], "nul", d['nullity_numeric'], "psd", d['psd'], "masym", d['masym'], "| outer t(l) miss", sorted(set(range(4,14)) - set(tl)), "t(m) miss", sorted(set(range(4,14)) - set(tm)), "|", " ".join(out))
