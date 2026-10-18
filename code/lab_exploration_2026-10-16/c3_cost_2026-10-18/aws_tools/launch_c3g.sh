#!/bin/bash
# Launch the second c3 pass with Gram covers (LAB 18/10/2026): one Spot machine (m7a.32xlarge, else c7a.32xlarge) per part.
# usage: bash launch_c3g.sh <a|b> [upload]
set -u
P="$(cd "$(dirname "$0")" && pwd)"; cd "$P"; export MSYS_NO_PATHCONV=1
A="aws --profile frere --region eu-north-1"
B=conway99-c1-runs-733515672125
m="$1"
if [ "${2:-}" = upload ]; then
  $A s3 cp code_c3g.tar.gz s3://$B/runs/c3g$m/pkg/code.tar.gz --only-show-errors
  $A s3 cp manifest_c3g$m.tsv s3://$B/runs/c3g$m/pkg/manifest.tsv --only-show-errors
  $A s3 cp runner_v2.py s3://$B/runs/c3g$m/pkg/runner.py --only-show-errors
  echo uploaded
fi
for spec in "m7a.32xlarge subnet-0ea35b14265e0812c" "m7a.32xlarge subnet-0c965bd273a9c5134" "m7a.32xlarge subnet-0e1603ed9b6044789" \
            "c7a.32xlarge subnet-0ea35b14265e0812c" "c7a.32xlarge subnet-0e1603ed9b6044789" "c7a.32xlarge subnet-0c965bd273a9c5134"; do
  set -- $spec
  r=$($A ec2 run-instances --image-id ami-0fd9576cca965bd19 --instance-type "$1" --subnet-id "$2" --iam-instance-profile Name=conway99-c1-runner \
      --instance-market-options 'MarketType=spot,SpotOptions={SpotInstanceType=one-time,InstanceInterruptionBehavior=terminate,MaxPrice=2.00}' \
      --instance-initiated-shutdown-behavior terminate --user-data "file://userdata_c3g$m.sh" \
      --block-device-mappings 'DeviceName=/dev/sda1,Ebs={VolumeSize=100,VolumeType=gp3,DeleteOnTermination=true}' --metadata-options HttpTokens=required \
      --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=c1-c3g-$m},{Key=project,Value=conway99-c1}]" \
      --query 'Instances[0].InstanceId' --output text 2>&1 | tail -1)
  case "$r" in i-*) echo "c3g$m $r $1 $2"; exit 0;; *) echo "  $1 $2: $r";; esac
done
echo "c3g$m NO_CAPACITY"
