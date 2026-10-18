#!/bin/bash
# Boot script of the C1 runner instance (Ubuntu 24.04).  Hard cap: the machine powers off after __MAXMIN__ minutes
# whatever happens (InstanceInitiatedShutdownBehavior=terminate), and right after the last job.
exec > /var/log/c1-boot.log 2>&1
set -x
shutdown -h +__MAXMIN__ "C1 runner hard cap"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3-venv python3-pip util-linux time
python3 -m venv /opt/v
/opt/v/bin/pip install --no-cache-dir __PIPSPEC__ boto3
export PATH=/opt/v/bin:$PATH
mkdir -p /work/repo
cd /work
/opt/v/bin/python - <<'PY'
import boto3
s3 = boto3.client("s3", region_name="eu-north-1")
for key, dst in [("runs/__RUN__/pkg/code.tar.gz", "/work/code.tar.gz"), ("runs/__RUN__/pkg/manifest.tsv", "/work/manifest.tsv"),
                 ("runs/__RUN__/pkg/runner.py", "/work/runner.py")]:
    s3.download_file("__BUCKET__", key, dst)
PY
tar xzf /work/code.tar.gz -C /work/repo
rm -f /work/repo/data/codex_line_resonance_20261016/cpu_guard.budget.json
/opt/v/bin/python -c "import boto3; boto3.client('s3', region_name='eu-north-1').upload_file('/var/log/c1-boot.log', '__BUCKET__', 'runs/__RUN__/boot_before_jobs.log')"
/opt/v/bin/python /work/runner.py --bucket __BUCKET__ --run __RUN__ --manifest /work/manifest.tsv --workers $(nproc)
/opt/v/bin/python -c "import boto3; boto3.client('s3', region_name='eu-north-1').upload_file('/var/log/c1-boot.log', '__BUCKET__', 'runs/__RUN__/boot_final.log')"
shutdown -h now
