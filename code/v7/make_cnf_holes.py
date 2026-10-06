import json, sys
from v7sat import build
cores=json.load(open('cores27.json'))
k=int(sys.argv[1]); holes=[int(v) for v in sys.argv[2].split(',')]
S,h=build(cores[k],fix_holes=holes)
S.cnf.to_file(f'/tmp/solvers/v7_core{k}_h{"_".join(map(str,holes))}.cnf')
print('ok',S.pool.top,len(S.cnf.clauses))
