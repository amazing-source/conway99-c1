"""Compile both exact enumerators and independently check the whole archived dossier.
Python >=3.10, a C++17 compiler (g++ by default); no third-party Python packages.
Temporary verification reports do not overwrite the archived evidence.
"""
from pathlib import Path
import os,subprocess,sys,shlex,tempfile,json
R=Path(__file__).resolve().parents[1]
def compile_tools():
 compiler=shlex.split(os.environ.get('CXX','g++'))
 for stem in ('rows22','rows22_independent'):
  subprocess.run(compiler+['-O3','-std=c++17',str(R/'code'/f'{stem}.cpp'),'-o',str(R/stem)],check=True)
def main():
 if not __debug__:raise RuntimeError('Run without -O: assertions are part of the verification.')
 compile_tools()
 with tempfile.TemporaryDirectory(prefix='hoffman_check_') as tmp:
  env=os.environ.copy();env['HOFFMAN_OUTPUT_DIR']=tmp;env.pop('PYTHONOPTIMIZE',None)
  for name in ['verify_catalogues.py','verify_campaign.py','positive_control.py','verify_same_hoffman_boundary.py']:
   subprocess.run([sys.executable,str(R/'code'/name)],env=env,check=True)
  c=json.loads((Path(tmp)/'verification_all.json').read_text())
  assert c['verified_designs']==271 and c['independent_row_search_count']==1283
  assert c['verified_candidate_rows']==432685
  assert c['deletions']==27335
  print('FINAL: 271 designs excluded; two independent row algorithms agree; all deletion traces valid.')
  print('FINAL: asymmetric Paley-family counterexample with the same Hoffman boundary verified.')
if __name__=='__main__':main()
