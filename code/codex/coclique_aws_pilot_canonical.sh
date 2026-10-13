#!/bin/bash
set -euo pipefail
while systemctl is-active --quiet conway-followup.service; do sleep 5; done
test -f /opt/conway/next/results/DONE
cd /opt/conway/canonical
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
PY=/opt/conway/venv/bin/python
mkdir -p results
$PY code/codex/coclique_partition_campaign.py campaign results/canonical_processes32_workers4 --seconds 180 --workers 4 --jobs 32 --full-workers 4 --canonical --seed 1
date -u > results/DONE
tar -czf /opt/conway/canonical-results.tar.gz results
sha256sum /opt/conway/canonical-results.tar.gz > /opt/conway/canonical-results.tar.gz.sha256
