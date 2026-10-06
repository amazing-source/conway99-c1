import json, sys, itertools, time
from v7sat import build, P13
from coset_cvp import run
cores=json.load(open('cores27.json'))
k=int(sys.argv[1])
core=cores[k]
S,h=build(core)
# exclude hole sets killed by core-supported class elements (level-0 norm < 40)
cols=core['columns']; killed=0
for H in itertools.combinations(range(13),4):
    holes=[14+i for i in H]
    res=run(core,holes,bound=34)
    if any(l==0 for (l,v) in res):
        S.clause([-h[v] for v in holes]); killed+=1
S.cnf.to_file(f'/tmp/solvers/v7_core{k}.cnf')
print('core',k,'vars',S.pool.top,'clauses',len(S.cnf.clauses),'hole sets killed by CVP',killed)
