#!/bin/bash
set -euo pipefail
cd /opt/conway/work
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
PY=/opt/conway/venv/bin/python
mkdir -p results
uname -a > results/host.txt
lscpu >> results/host.txt
free -b >> results/host.txt
/opt/conway/venv/bin/pip freeze > results/packages.txt
systemctl list-timers conway-budget-stop.timer --no-pager > results/auto-stop.txt
$PY code/codex/check_coclique_residual_partition.py data/codex_coclique_defects/partition_v10
$PY code/codex/coclique_partition_campaign.py campaign results/processes32_workers4 --seconds 180 --workers 4 --jobs 32 --seed 1
$PY code/codex/coclique_partition_campaign.py campaign results/processes16_workers8 --seconds 180 --workers 8 --jobs 16 --seed 1
date -u > results/DONE
tar -czf /opt/conway/results.tar.gz results data/codex_coclique_defects/partition_v10
sha256sum /opt/conway/results.tar.gz > /opt/conway/results.tar.gz.sha256
