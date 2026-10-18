"""Apply the new histogram LP bounds to LAB's eight hard c1/c2 catalogues.

The DFS row catalogues are accepted from LAB, not re-enumerated here.
Any reported certificate has its integer combination checked by the
generator; this script does not claim an independent completeness audit.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from root_component_z_design_certificate import linear_system,find_certificate,reduce_diagonal_system


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('--output-directory',type=Path,required=True)
    a=p.parse_args();assert not a.output_directory.exists()
    a.output_directory.mkdir(parents=True)
    resources=limit_research_process(1)
    result={'scope':__doc__,'resources':resources,'records':[],'global_conway_exclusion':False}
    paths=sorted(a.directory.glob('catalogue_c12_*.json'));assert len(paths)==8
    for path in paths:
        started=time.process_time();raw=path.read_bytes();doc=json.loads(raw)
        template,catalogue=doc['template'],doc['catalogue']
        assert catalogue['status']=='ROW_CATALOGUE_COMPLETE'
        cols,eqs,bs=linear_system(template,catalogue,degree_histograms=True,short_columns=True)
        certificate=find_certificate(cols,eqs,bs)
        if certificate['status']=='EXCLUDED_BY_INTEGER_CERTIFICATE':
            eqs,bs=reduce_diagonal_system(cols,eqs,bs,fallback_full=True)
            reduced=find_certificate(cols,eqs,bs)
            if reduced['status']=='EXCLUDED_BY_INTEGER_CERTIFICATE':certificate=reduced
        record={'sample_index':doc['sample_index'],'family':doc['family'],
                'free_dimension':catalogue['free_dimension'],'row_states':len(cols),
                'status':certificate['status'],'cpu_seconds':time.process_time()-started,
                'source':str(path),'source_sha256':hashlib.sha256(raw).hexdigest(),
                'catalogue_completeness_source':'LAB DFS, not independently rerun',
                'uses_Gram_cover':False,'uses_prism_budget':False}
        atomic_json_write(a.output_directory/path.name,{'record':record,'certificate':certificate})
        result['records'].append(record);atomic_json_write(a.output_directory/'summary.json',result)
        print(json.dumps(record),flush=True)


if __name__=='__main__':main()
