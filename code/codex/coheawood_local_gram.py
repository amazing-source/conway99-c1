"""Explore the residual Gram on the ten vertices in one S-row."""
from itertools import combinations
import json
from pathlib import Path
import random
import numpy as np


def main():
    rng = random.Random(20261012)
    m = {(4,5),(6,7),(8,9)}
    l = {(5,6),(7,8),(4,9)}
    forbidden = m | l
    edges = set(combinations(range(4),2)) | (set(combinations(range(4,10),2))-forbidden)
    best = 0.0
    examples = []
    for trial in range(2000):
        for step in range(30):
            (a,b),(c,d) = rng.sample(sorted(edges),2)
            if len({a,b,c,d})<4:
                continue
            if rng.randrange(2):
                c,d=d,c
            ac,bd=tuple(sorted((a,c))),tuple(sorted((b,d)))
            if ac in edges or bd in edges or ac in forbidden or bd in forbidden:
                continue
            edges.remove(tuple(sorted((a,b))))
            edges.remove(tuple(sorted((c,d))))
            edges.update((ac,bd))
        g = np.zeros((10,10),dtype=int)
        for a,b in edges:
            g[a,b]=g[b,a]=1
        k = -7*g
        for a in range(10):
            k[a,a]=30 if a<4 else 36
        for a,b in combinations(range(4),2):
            k[a,b]-=3; k[b,a]-=3
        for a,b in combinations(range(4,10),2):
            z = -6 if (a,b) in l else 3
            if (a,b) in m:
                z-=21
            k[a,b]+=z; k[b,a]+=z
        vals,vecs=np.linalg.eigh(k)
        if vals[0] < best-1e-7:
            best=float(vals[0])
            ex=dict(trial=trial, minimum=best, g_edges=sorted(edges),
                    eigenvector=vecs[:,0].tolist(), gram=k.tolist())
            examples.append(ex)
            print(json.dumps({q:v for q,v in ex.items() if q not in ('gram','eigenvector')}),flush=True)
    out=Path(__file__).resolve().parents[2]/'data/codex_coheawood/local_gram_pilot.json'
    out.write_text(json.dumps(dict(samples=2000, minimum=best, negative_examples=examples),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(samples=2000,minimum=best,negative_records=len(examples))),flush=True)


if __name__=='__main__': main()
