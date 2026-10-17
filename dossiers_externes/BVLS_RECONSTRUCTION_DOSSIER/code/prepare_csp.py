from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];name=sys.argv[1];meta=json.loads((ROOT/'data'/f'{name}.json').read_text());G=np.load(ROOT/'data'/meta['graph']);S=meta['fixed'];F=meta['free'];Y=G[np.ix_(S,F)];Z=Y.T@Y
logs=(ROOT/'reports'/f'{name}.log').read_text().splitlines();assert len(logs)==len(F) and all(s.split()[3]=='EXHAUSTED' for s in logs)
colors={};cs=[]
for j in range(len(F)):
 c=tuple(Y[:,j]);colors.setdefault(c,len(colors));cs.append(colors[c])
with (ROOT/'data'/f'{name}.csp').open('w') as f:
 f.write(str(len(F))+'\n'+' '.join(map(str,cs))+'\n')
 for row in Z:f.write(' '.join(map(str,row))+'\n')
 for i in range(len(F)):
  rows=[list(map(int,s.split())) for s in (ROOT/'data'/f'{name}_{i}.rows').read_text().splitlines()];assert len(rows)==int(logs[i].split()[1]);f.write(str(len(rows))+'\n')
  for row in rows:
   b=sum(1<<j for j in row);f.write(' '.join(str((b>>(64*k))&((1<<64)-1)) for k in range(4))+'\n')
print(name,'vertices',len(F),'initial boundary-profile classes',len(colors))
