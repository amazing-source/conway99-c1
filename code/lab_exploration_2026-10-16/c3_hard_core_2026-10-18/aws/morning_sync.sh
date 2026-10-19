#!/bin/bash
# Morning sync after the AWS re-login (LAB 19/10/2026): pull every run of the night from S3, list the instances still
# alive, recompute the c3 ledger (P1/P2/ZC/.../PALL/PORB/ZJ/C4C3) and print a short summary.
# usage: bash morning_sync.sh
set -u
cd "$(dirname "$0")"
B=conway99-c1-runs-733515672125
A="aws --profile frere --region eu-north-1"
for run in c3l2 c3p5 c3p4e c3p4eb c3eig2 glob1 gj5602; do
  echo "== sync $run"; timeout 600 $A s3 sync s3://$B/runs/$run/ collect_$run/ --only-show-errors
  $A s3 cp s3://$B/runs/$run/status.json - 2>/dev/null | tr -d '\n' | head -c 300; echo
done
for r in eu-north-1 eu-west-2 us-east-2; do
  echo "== instances $r"; aws --profile frere --region $r ec2 describe-instances --filters Name=instance-state-name,Values=pending,running \
    --query "Reservations[].Instances[].[InstanceId,InstanceType,Tags[?Key=='Name']|[0].Value,LaunchTime]" --output text
done
py -3 c3_ledger.py | head -40
py -3 - <<'EOF'
import glob, json
from collections import Counter
for pre, d in [("l2_", "collect_c3l2"), ("p5_", "collect_c3p5"), ("pe_", "collect_c3p4e"), ("pe_", "collect_c3p4eb")]:
    c = Counter()
    for f in glob.glob("%s/files/out/%s*.json" % (d, pre)):
        try:
            for cs in json.load(open(f)).get("cases", []): c[cs.get("status")] += 1
        except Exception: pass
    print(d, pre, dict(c))
c = Counter()
for f in glob.glob("collect_c3eig2/files/out/zj_*.jsonl"):
    for line in open(f):
        if line.startswith("{"): c[json.loads(line)["status"]] += 1
print("zj (Gram-free whole templates)", dict(c))
EOF
