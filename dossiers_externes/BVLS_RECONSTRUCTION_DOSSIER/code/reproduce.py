"""Rebuild the principal exact classification in a NEW directory, including the no-quotient cross-check.
Requirements: Python 3, NumPy, a C++17 compiler with Boost headers (for integer weights).
No model API calls, cloud jobs or repository writes.
"""
import argparse,shutil,subprocess,os,json,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--all-cases',action='store_true');a=p.parse_args()
W=Path(a.work).resolve()
if W.exists():raise SystemExit('Work directory must not exist: '+str(W))
W.mkdir(parents=True)
for d in ['code','data','reports','sources']:(W/d).mkdir()
for f in (ROOT/'code').iterdir():
 if f.suffix in ('.cpp','.py'):shutil.copy2(f,W/'code'/f.name)
shutil.copy2(ROOT/'data/gamma3.g6',W/'data/gamma3.g6')
env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1'
def run(cmd,log=None,timeout=900):
 print('+',' '.join(map(str,cmd)),flush=True)
 if log:
  with (W/'reports'/log).open('w') as f:subprocess.run(list(map(str,cmd)),cwd=W,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=timeout)
 else:subprocess.run(list(map(str,cmd)),cwd=W,env=env,check=True,timeout=timeout)
for x in ['rows','cap_aut','complete','complete_noquotient']:
 run(['g++','-std=c++17','-O3','code/'+x+'.cpp','-o','code/'+x])
run([sys.executable,'code/setup_bvls.py'])
sys.path.insert(0,str(W/'code'));from read_graph6 import read_graph6
B=read_graph6(W/'data/gamma3.g6');assert np.array_equal(B@B+B,20*np.eye(243,dtype=int)+2*np.ones((243,243),dtype=int));np.save(W/'data/gamma3.npy',B)
H=np.array(json.loads((W/'data/golay_basis.json').read_text()));np.savetxt(W/'data/cap.txt',H.T,fmt='%d')
run(['code/cap_aut','data/cap.txt','data/linear_aut.txt'],'linear_aut.log')
run([sys.executable,'code/make_instance.py','tri'])
run(['code/rows','data/tri.inst','data/tri','60','1000000'],'tri.log')
run([sys.executable,'code/assemble.py','tri','--seconds','600'],'tri_assembly.log')
C=np.array([[int(c) for c in line.strip()] for line in (W/'data/tri_solutions/000002.adj').read_text().splitlines()],dtype=int);np.save(W/'data/twin.npy',C)
b=''.join(f'{i} {j}\n' for i in range(243) for j in range(i+1,243) if C[i,j]);(W/'data/twin.edges').write_text(b)
import hashlib
bb=b.encode();assert hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()=='f5c2f546c61f0291dcdc709bb1767846c8a3d4fa'
run([sys.executable,'code/make_instance.py','prism2','--release','3,4,5,6,7,8,9,10,11,18,19,20'])
run([sys.executable,'code/orbit_domains.py','prism2'],'prism2_orbit.log')
run([sys.executable,'code/prepare_csp.py','prism2'])
run(['code/complete','data/prism2.csp','data/prism2.sol','600','100000'],'prism2_native.log')
run(['code/complete_noquotient','data/prism2.csp',os.devnull,'600','100000'],'prism2_noquotient.log')
for f in ['prism2_native.log','prism2_noquotient.log']:
 s=(W/'reports'/f).read_text();assert s.startswith('EXHAUSTED') and 'labelled 27648 ' in s,s
run([sys.executable,'code/certify_case.py','prism2'],'prism2_verification.log')
run([sys.executable,'code/coverage.py'],'coverage.log')
run([sys.executable,'code/verify_bundle.py'],'verify_bundle.log')
if a.all_cases:
 for name,graph,release in [('prism','bvls.npy','3,4,5,6,7,8'),('g3prism','gamma3.npy','3,4,5,6,7,8'),('six','bvls.npy','3,6,9,18,27,54')]:
  run([sys.executable,'code/make_instance.py',name,'--graph',graph,'--release',release])
  run(['code/rows','data/'+name+'.inst','data/'+name,'60','2000000'],name+'.log')
  run([sys.executable,'code/assemble.py',name,'--seconds','600'],name+'_assembly.log')
print('REPRODUCTION COMPLETE:',W,flush=True)
