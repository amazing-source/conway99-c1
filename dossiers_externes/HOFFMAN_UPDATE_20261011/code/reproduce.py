"""Regenerate the campaign from source in a NEW empty working directory.
Does not copy any recorded design, row domain or exclusion certificate.
Usage: python code/reproduce.py --work /path/to/new_directory
"""
from pathlib import Path
import argparse,shutil,subprocess,sys,time,json,os
R=Path(__file__).resolve().parents[1]
def main():
 if not __debug__:raise RuntimeError('Run without -O.')
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);args=ap.parse_args()
 target=args.work.expanduser().resolve()
 if target.exists():raise FileExistsError(f'Use a NEW directory: {target}')
 target.mkdir(parents=True)
 shutil.copytree(R/'code',target/'code',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for d in ['data','reports','sources']: (target/d).mkdir()
 for name in ['paley25.adj','paley_asymmetric25.adj','paley25_complement.adj','paley_asymmetric25_complement.adj']:
  shutil.copy2(R/'data'/name,target/'data'/name)
 shutil.copy2(R/'reports/paley_original_transformation.json',target/'reports/paley_original_transformation.json')
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env.pop('HOFFMAN_OUTPUT_DIR',None)
 t0=time.time()
 subprocess.run([sys.executable,'-c','from check_all import compile_tools; compile_tools()'],cwd=target/'code',env=env,check=True)
 scripts=['cyclic_designs.py','one_rotational_designs.py','run_designs.py','run_one_rotational.py',
          'verify_catalogues.py','verify_campaign.py','positive_control.py','verify_same_hoffman_boundary.py']
 for script in scripts:
  print('RUN',script,flush=True)
  with open(target/'reports'/f'replay_{Path(script).stem}.log','w') as f:
   subprocess.run([sys.executable,str(target/'code'/script)],stdout=f,stderr=subprocess.STDOUT,env=env,check=True)
 v=json.loads((target/'reports/verification_all.json').read_text())
 assert v['verified_designs']==271 and v['verified_candidate_rows']==432685 and v['deletions']==27335
 report={'completed':True,'verified_designs':271,'verified_candidate_rows':432685,'verified_deletions':27335,
         'seconds':time.time()-t0,'no_original_domains_or_design_catalogues_copied':True}
 (target/'reports/reproduction.json').write_text(json.dumps(report,indent=2));print(report,flush=True)
if __name__=='__main__':main()
