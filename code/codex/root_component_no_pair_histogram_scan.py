"""Pilot the new Gram-free histogram cuts on the 27 c3 templates without a two-block.

This is a new necessary-condition pass, not a rerun of LAB's Gram campaigns.
Each exact certificate is checked immediately by the integer reader.
"""

import argparse
import gzip
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from root_component_z_pipeline import run


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('--output-directory',type=Path,required=True)
    a=p.parse_args();assert not a.output_directory.exists()
    a.output_directory.mkdir(parents=True)
    resources=limit_research_process(1)
    source=json.loads(gzip.decompress(a.source.read_bytes()))
    entries=source.get('open',source.get('survivors'))
    indices=[i for i,entry in enumerate(entries)
             if not any(len(part)==2 for groups in entry['template']['nontrivial_component_groups'] for part in groups)]
    assert len(indices)==27,(len(indices),indices)
    result={'scope':__doc__,'indices':indices,'records':[],'resources':resources,
            'uses_Gram_cover':False,'global_conway_exclusion':False}
    for i in indices:
        item=run(a.source,i,a.output_directory/f'gz{i:05}',design_seconds=0,
                 reduce=True,short_columns=True,max_free=7)
        result['records'].append({k:v for k,v in item.items() if k!='resources'})
        atomic_json_write(a.output_directory/'summary.json',result)


if __name__=='__main__':main()
