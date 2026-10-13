"""Verify saved V10 campaign artifacts and the unchanged V7 model prefix."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import sys
from ortools.sat import cp_model_pb2


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(folder):
    aws = folder/'aws_pilot'
    archives = {}
    for name in ('results.tar.gz','next-results.tar.gz','canonical-results.tar.gz'):
        p = aws/name
        assert digest(p) == (aws/(name+'.sha256')).read_text().split()[0]
        archives[name] = dict(bytes=p.stat().st_size,sha256=digest(p))
    campaigns = []
    for plan_file in sorted((aws/'results').glob('*/protocol.json')):
        p = plan_file.parent
        plan = json.loads(plan_file.read_text())
        report = json.loads((p/'report.json').read_text())
        for name,expected in plan['source_hashes'].items():
            assert digest(p/'sources'/name) == expected,(p,name)
        selected = [b['id'] for b in plan['selected_branches']]
        assert set(selected) == set(report['results'])
        for name in selected:
            config = json.loads((p/name/'config.json').read_text())
            for source,expected in config['source_hashes'].items():
                assert digest(p/'sources'/source) == expected,(name,source)
            assert report['results'][name]['returncode'] == 0
            assert (p/name/'diagnostics.json').exists()
        campaigns.append(dict(name=p.name,jobs=len(selected),
            statuses=dict(Counter(x['status'] for x in report['results'].values()))))
    assert len(campaigns) == 5 and sum(c['jobs'] for c in campaigns) == 255
    old_path = folder.parent/'calibration_v9/models/5a29aa8518171c4eb2cb5f3fbe7e869f377a705436c5e640581dcde00bf801cc.pb'
    old,new = cp_model_pb2.CpModelProto(),cp_model_pb2.CpModelProto()
    old.ParseFromString(old_path.read_bytes())
    new_path = folder/'local_global_8w/model.pb'
    new.ParseFromString(new_path.read_bytes())
    assert list(new.variables[:len(old.variables)]) == list(old.variables)
    assert list(new.constraints[:len(old.constraints)]) == list(old.constraints)
    result = dict(check='PASS',archives=archives,campaigns=campaigns,
                  prefix=dict(old_variables=len(old.variables),old_constraints=len(old.constraints),
                              added_variables=len(new.variables)-len(old.variables),
                              added_constraints=len(new.constraints)-len(old.constraints),
                              strengthened_model_sha256=digest(new_path)),
                  scope='Artifact integrity, not a mathematical nonexistence certificate')
    (folder/'artifact_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    verify(Path(sys.argv[1]))
