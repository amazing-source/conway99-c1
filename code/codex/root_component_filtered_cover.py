"""Remove only Gram branches with an exact INFEASIBLE record from a full cover."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--committed-only",action="store_true",help="Ignore untracked signature reports when freezing a reproducible cover.")
    args=parser.parse_args()
    source=args.directory/"root_component_gram_orbits20.json"
    data=json.loads(source.read_text())
    covers={r["template_index"]:r for r in data["records"]}
    rejected={}
    tracked=None
    if args.committed_only:
        repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
        tracked={(repo/name).resolve() for name in subprocess.check_output(['git','ls-files'],text=True).splitlines()}
    hashes={source.name:hashlib.sha256(source.read_bytes()).hexdigest()}
    for path in sorted(args.directory.glob("root_component_signature_*.json")):
        if tracked is not None and path.resolve() not in tracked:continue
        raw=path.read_bytes()
        report=json.loads(raw)
        used=False
        for record in report.get("records",[]):
            if "cases" not in record:continue
            index=record["template_index"]
            assert record["complete_source_gram_count"]==covers[index]["gram_count"]
            for case in record["cases"]:
                if case["status"]!="INFEASIBLE":continue
                gi=case["gram_index"]
                assert case["gram_anchor_values"]==covers[index]["gram_anchor_values"][gi]
                rejected.setdefault(index,{}).setdefault(gi,path.name)
                used=True
        if used:hashes[path.name]=hashlib.sha256(raw).hexdigest()
    for record in data["records"]:
        assert record["exhaustive"] and record["usable_as_gram_cover"]
        index=record["template_index"]
        omitted=rejected.get(index,{})
        keep=[i for i in range(record["gram_count"]) if i not in omitted]
        record.update(source_gram_count=record["gram_count"],source_gram_indices=keep,
                      excluded_gram_sources=omitted,
                      gram_anchor_values=[record["gram_anchor_values"][i] for i in keep],gram_count=len(keep))
        if "gram_orbit_sizes" in record:
            record["gram_orbit_sizes"]=[record["gram_orbit_sizes"][i] for i in keep]
            record["orbit_size_histogram"]=dict(Counter(record["gram_orbit_sizes"]))
        print(index,len(keep),flush=True)
    data.update(scope="Complete necessary Gram cover after recorded INFEASIBLE signature branches; solver verdicts, no portable proof.",
                input_sha256=hashes)
    args.output.write_text(json.dumps(data,separators=(",",":"))+"\n",encoding="utf-8")


if __name__=="__main__":main()
