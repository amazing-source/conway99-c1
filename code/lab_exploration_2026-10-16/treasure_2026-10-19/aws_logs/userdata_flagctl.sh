#!/bin/bash
# Flag-algebra campaign (LAB 19/10/2026, user: "utilise aws s'il faut ... mets le paquet").  Hard cap 180 minutes.
exec > /var/log/c1-boot.log 2>&1
set -x
shutdown -h +150 "C1 flag control hard cap"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3-venv python3-pip
python3 -m venv /opt/v
/opt/v/bin/pip install --no-cache-dir numpy scipy boto3 highspy
mkdir -p /work/repo
cd /work
/opt/v/bin/python -c "import boto3; boto3.client('s3', region_name='eu-north-1').download_file('conway99-c1-runs-733515672125', 'runs/flagctl/pkg/code.tar.gz', '/work/code.tar.gz')"
tar xzf /work/code.tar.gz -C /work/repo
/opt/v/bin/python -c "import boto3; boto3.client('s3', region_name='eu-north-1').upload_file('/var/log/c1-boot.log', 'conway99-c1-runs-733515672125', 'runs/flagctl/boot_before_jobs.log')"
cd /work/repo && /opt/v/bin/python aws_control_runner.py > /work/runner.log 2>&1
/opt/v/bin/python -c "import boto3; c = boto3.client('s3', region_name='eu-north-1'); c.upload_file('/work/runner.log', 'conway99-c1-runs-733515672125', 'runs/flagctl/runner.log'); c.upload_file('/var/log/c1-boot.log', 'conway99-c1-runs-733515672125', 'runs/flagctl/boot_final.log')"
shutdown -h now
