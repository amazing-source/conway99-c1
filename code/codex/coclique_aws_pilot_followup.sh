#!/bin/bash
set -euo pipefail
# Wait for the two frozen base comparisons; no concurrent benchmark load.
while systemctl is-active --quiet conway-pilot.service; do sleep 5; done
test -f /opt/conway/work/results/DONE
cd /opt/conway/next
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
PY=/opt/conway/venv/bin/python
mkdir -p results
$PY code/codex/coclique_partition_campaign.py campaign results/processes32_workers4_full4 --seconds 180 --workers 4 --jobs 32 --full-workers 4 --seed 1
$PY code/codex/coclique_partition_campaign.py campaign results/leaf_columns_workers8 --seconds 180 --workers 8 --jobs 11 --leaf-columns --seed 1 --select r1_1_C13 r1_1_ZH r1_2_C13 r1_2_ZH r1_3_C13 r1_3_ZH r1_4_C13 r1_4_ZH r1_5_C13 r1_5_ZH r1_6_ZH
date -u > results/DONE
tar -czf /opt/conway/next-results.tar.gz results
sha256sum /opt/conway/next-results.tar.gz > /opt/conway/next-results.tar.gz.sha256
