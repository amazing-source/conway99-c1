#!/bin/bash
set -eu
systemd-run --unit=conway-budget-stop --on-active=40m --timer-property=AccuracySec=1s /usr/sbin/shutdown -h now
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python3-venv
mkdir -p /opt/conway
python3 -m venv /opt/conway/venv
/opt/conway/venv/bin/pip install --no-cache-dir ortools==9.15.6755 numpy sympy
chown -R ubuntu:ubuntu /opt/conway
touch /opt/conway/READY
