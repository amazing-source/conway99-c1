import sys, json, random
ARGS = list(sys.argv)
sys.path.insert(0, '.')
import indep_model as M
prog = M.load_program(M.COVERS / 'core_000.json.gz')
rnd = random.Random(5)
allc = [a for a in json.load(open('cases.json'))['all'] if a[2] and a[2] <= 600]
checked = bad = 0
for _ in range(25):
    ci, bi = rnd.choice(allc)[:2]
    cv = M.cover(ci); core = cv['core']; bd = tuple(bytes.fromhex(cv['boundaries_hex'][bi]))
    leaves = [tuple(a) for a, _ in prog.gen_attachments(core, bd)]
    ls = set(leaves)
    for a in rnd.sample(leaves, min(5, len(leaves))):
        R = M.known_rows(core['edges'], bd, a)
        for f3 in (0, 1):
            for f6 in (0, 1):
                def fl(lab):
                    return tuple(sorted(x ^ 1 if (x // 2 == 3 and f3) or (x // 2 == 6 and f6) else x for x in lab))
                pi = [M.KIDX[fl(M.KL[u])] for u in range(20)]
                # image attachment by my own rule: relabel every edge of every block
                img = []
                for bi_, (A, B) in enumerate(M.BLOCKS):
                    p = [None] * 4
                    for c in range(4):
                        u, v = M.kid(A, c), M.kid(B, a[bi_][c])
                        cu = M.rect_labels(*A).index(M.KL[pi[u]]); cv_ = M.rect_labels(*B).index(M.KL[pi[v]])
                        p[cu] = cv_
                    img.append(tuple(p))
                img = tuple(img)
                R2 = M.known_rows(core['edges'], bd, img)
                iso = all(sum(2 ** pi[w] for w in range(20) if R[u] >> w & 1) == R2[pi[u]] for u in range(20))
                in_orbit = img in ls
                canon_ok = prog.attachment_canon(a) == min(prog.attachment_canon(a), img)
                checked += 1; bad += (not iso) or (not in_orbit) or (not canon_ok)
print('checked', checked, 'bad', bad)
