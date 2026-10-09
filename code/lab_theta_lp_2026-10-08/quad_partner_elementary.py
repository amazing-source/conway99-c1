"""C1, lab session, 2026-10-09 (NOTE 17.83). Is the computed partner relation between kernel types explained by elementary
identities alone? Predicted relation for a type (6 not adjacent to 7) and a labelled survivor c read as H*:
 (i)  c agrees with H on every pair of members of D* that are vertices of H;
 (ii) a member of D* that is a NEW vertex has its forced neighbours in S: d(1,6), d(4,6), d(0,7), d(3,7) are not adjacent
      to 2 or 5; a new common neighbour of 6 and 7 is not adjacent to both 2 and 5;
 (iii) each of the pairs (2,6), (2,7), (5,6), (5,7) has at most one common neighbour besides 0, 1, 3, 4 respectively.
Compared with the relation computed by quad_partner_kernels.py (all completions, positivity on the union).
  python quad_partner_elementary.py <Codex data folder> <json of quad_partner_kernels.py>"""
import sys, json
_argv = sys.argv[:]; sys.argv = [_argv[0], _argv[1], "unused.json", "0", "0", "0", "100000"]
import quad_partner_kernels as q
done = json.load(open(_argv[2]))["types"]
same = diff = 0; more = less = 0
for bs, r in done.items():
    if r["prism_partner"]: continue
    bits = int(bs); b = lambda u, v: bits >> q.OPTI[(u, v)] & 1
    adj0 = q.base_adj(bits); i611, i69, i710, i78, both = q.interface(bits)
    star = dict(q.STAR_S); star[6] = 2; star[7] = 5
    for lab, ident, old in ((8, i611, 11), (9, i69, 9), (10, i710, 10), (11, i78, 8)):
        if ident: star[lab] = old
    labs = [12, 13]
    for k in both: star[labs.pop(0)] = k
    new12 = labs
    pred = set()
    for c in q.LABELLED:
        cb = lambda p, s: c >> q.OPTI[(p, s)] & 1
        if any((c >> q.OPTI[(p, s)] & 1) != (adj0[star[p]] >> star[s] & 1) for p, s in q.OPT if p in star and s in star): continue
        if any(lab not in star and cb(*e) for lab, e in ((9, (6, 9)), (11, (6, 11)), (8, (7, 8)), (10, (7, 10)))): continue
        if any(cb(6, k) and cb(7, k) for k in new12): continue
        n6 = sum(cb(6, k) for k in new12); n7 = sum(cb(7, k) for k in new12)      # new common neighbours of 6,7 adjacent to 2 / to 5
        if b(6, 9) + b(6, 12) + b(6, 13) + n6 > 1: continue                         # pair (2,6)
        if b(7, 8) + b(7, 12) + b(7, 13) + n6 > 1: continue                         # pair (2,7)
        if b(6, 11) + b(6, 12) + b(6, 13) + n7 > 1: continue                        # pair (5,6)
        if b(7, 10) + b(7, 12) + b(7, 13) + n7 > 1: continue                        # pair (5,7)
        pred.add(q.canon(c))
    comp = set(r["partners"])
    if pred == comp: same += 1
    else: diff += 1; more += len(pred - comp); less += len(comp - pred)
print("types compared %d: predicted relation equal to the computed one for %d; different for %d (predicted but not computed %d, computed but not predicted %d)" % (same + diff, same, diff, more, less))
