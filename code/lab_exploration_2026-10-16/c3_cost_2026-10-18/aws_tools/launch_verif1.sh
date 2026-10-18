#!/bin/bash
# Launch run verif1 (LAB 18/10/2026): uploads the package, manifests, runner, then one Spot machine per part.
#   a: E1/E2 censuses (two enumerators) + V3 (CP-SAT and HiGHS on every c >= 3 template), 128 workers
#   b: P3 pilot of the corrected complete-star (100 tasks x 2 variants), 100 workers (memory)
# usage: bash launch_verif1.sh <a|b|both> [upload]
set -u
P="$(cd "$(dirname "$0")" && pwd)"; cd "$P"; export MSYS_NO_PATHCONV=1
A="aws --profile frere --region eu-north-1"
B=conway99-c1-runs-733515672125
parts="$1"; [ "$parts" = both ] && parts="a b"
if [ "${2:-}" = upload ]; then
  for m in a b; do
    $A s3 cp code_verif1.tar.gz s3://$B/runs/verif1$m/pkg/code.tar.gz --only-show-errors
    $A s3 cp manifest_verif1$m.tsv s3://$B/runs/verif1$m/pkg/manifest.tsv --only-show-errors
    $A s3 cp runner.py s3://$B/runs/verif1$m/pkg/runner.py --only-show-errors
  done
  echo uploaded
fi
for m in $parts; do
  done_id=""
  for spec in "m7a.32xlarge subnet-0ea35b14265e0812c" "m7a.32xlarge subnet-0c965bd273a9c5134" "m7a.32xlarge subnet-0e1603ed9b6044789" \
              "c7a.32xlarge subnet-0ea35b14265e0812c" "c7a.32xlarge subnet-0e1603ed9b6044789" "c7a.32xlarge subnet-0c965bd273a9c5134"; do
    set -- $spec
    if [ "$m" = b ] && [ "$1" = c7a.32xlarge ]; then continue; fi        # part b needs the 512 GiB of m7a
    r=$($A ec2 run-instances --image-id ami-0fd9576cca965bd19 --instance-type "$1" --subnet-id "$2" --iam-instance-profile Name=conway99-c1-runner \
        --instance-market-options 'MarketType=spot,SpotOptions={SpotInstanceType=one-time,InstanceInterruptionBehavior=terminate,MaxPrice=2.00}' \
        --instance-initiated-shutdown-behavior terminate --user-data "file://userdata_verif1$m.sh" \
        --block-device-mappings 'DeviceName=/dev/sda1,Ebs={VolumeSize=100,VolumeType=gp3,DeleteOnTermination=true}' --metadata-options HttpTokens=required \
        --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=c1-verif1-$m},{Key=project,Value=conway99-c1}]" \
        --query 'Instances[0].InstanceId' --output text 2>&1 | tail -1)
    case "$r" in i-*) echo "verif1$m $r $1 $2"; done_id="$r"; break;; *) echo "  $1 $2: $r";; esac
  done
  [ -n "$done_id" ] || echo "verif1$m NO_CAPACITY"
done
