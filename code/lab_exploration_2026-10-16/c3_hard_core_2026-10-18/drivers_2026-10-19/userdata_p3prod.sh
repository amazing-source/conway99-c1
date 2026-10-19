#!/bin/bash
# Boot script of the C1 runner instance (Ubuntu 24.04).  Hard cap: the machine powers off after 300 minutes
# whatever happens (InstanceInitiatedShutdownBehavior=terminate), and right after the last job.
exec > /var/log/c1-boot.log 2>&1
set -x
shutdown -h +240 "C1 runner hard cap"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3-venv python3-pip util-linux time g++
python3 -m venv /opt/v
/opt/v/bin/pip install --no-cache-dir ortools==9.15.6755 sympy==1.14.0 numpy scipy boto3 python-sat==1.9.dev15
export PATH=/opt/v/bin:$PATH
mkdir -p /work/repo
cd /work
/opt/v/bin/python - <<'PY'
import boto3
s3 = boto3.client("s3", region_name="eu-north-1")
for key, dst in [("runs/p3prod/pkg/code.tar.gz", "/work/code.tar.gz"), ("runs/p3prod/pkg/manifest.tsv", "/work/manifest.tsv"),
                 ("runs/p3prod/pkg/runner.py", "/work/runner.py")]:
    s3.download_file("conway99-c1-runs-733515672125", key, dst)
PY
tar xzf /work/code.tar.gz -C /work/repo
rm -f /work/repo/data/codex_line_resonance_20261016/cpu_guard.budget.json
bash /work/repo/build.sh > /work/build.log 2>&1 || echo BUILD_FAILED >> /work/build.log
/opt/v/bin/python -c "import boto3; boto3.client('s3', region_name='eu-north-1').upload_file('/work/build.log', 'conway99-c1-runs-733515672125', 'runs/p3prod/build.log')"
/opt/v/bin/python -c "import boto3; boto3.client('s3', region_name='eu-north-1').upload_file('/var/log/c1-boot.log', 'conway99-c1-runs-733515672125', 'runs/p3prod/boot_before_jobs.log')"
/opt/v/bin/python /work/runner.py --bucket conway99-c1-runs-733515672125 --run p3prod --manifest /work/manifest.tsv --workers $(( $(nproc) - 4 ))
/opt/v/bin/python -c "import boto3; boto3.client('s3', region_name='eu-north-1').upload_file('/var/log/c1-boot.log', 'conway99-c1-runs-733515672125', 'runs/p3prod/boot_final.log')"
shutdown -h now
