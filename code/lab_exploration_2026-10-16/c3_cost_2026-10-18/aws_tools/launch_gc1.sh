#!/bin/bash
# Launch run gc1a (LAB 18/10/2026): Gram covers in the exact all-in-one model, one on-demand c7a.16xlarge (64 vCPU).
# usage: bash launch_gc1.sh [upload]
set -u
P="$(cd "$(dirname "$0")" && pwd)"; cd "$P"; export MSYS_NO_PATHCONV=1
A="aws --profile frere --region eu-north-1"
B=conway99-c1-runs-733515672125
if [ "${1:-}" = upload ]; then
  $A s3 cp code_gc1.tar.gz s3://$B/runs/gc1a/pkg/code.tar.gz --only-show-errors
  $A s3 cp manifest_gc1a.tsv s3://$B/runs/gc1a/pkg/manifest.tsv --only-show-errors
  $A s3 cp runner_v2.py s3://$B/runs/gc1a/pkg/runner.py --only-show-errors
  echo uploaded
fi
for spec in "c7a.16xlarge subnet-0ea35b14265e0812c" "c7a.16xlarge subnet-0c965bd273a9c5134" "c7a.16xlarge subnet-0e1603ed9b6044789"; do
  set -- $spec
  r=$($A ec2 run-instances --image-id ami-0fd9576cca965bd19 --instance-type "$1" --subnet-id "$2" --iam-instance-profile Name=conway99-c1-runner \
      --instance-initiated-shutdown-behavior terminate --user-data "file://userdata_gc1a.sh" \
      --block-device-mappings 'DeviceName=/dev/sda1,Ebs={VolumeSize=60,VolumeType=gp3,DeleteOnTermination=true}' --metadata-options HttpTokens=required \
      --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=c1-gc1-a},{Key=project,Value=conway99-c1}]" \
      --query 'Instances[0].InstanceId' --output text 2>&1 | tail -1)
  case "$r" in i-*) echo "gc1a $r $1 $2"; exit 0;; *) echo "  $1 $2: $r";; esac
done
echo "gc1a NO_CAPACITY"
