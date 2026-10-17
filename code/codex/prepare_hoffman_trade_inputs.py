"""Retrieve existing design seeds and the proven row enumerator, without rerunning a census."""
from pathlib import Path
import hashlib
import io
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/codex_hoffman_trades'
OUT.mkdir(parents=True, exist_ok=True)
REF = 'f2b6454'
ARCHIVE = 'dossiers_externes/archives/HOFFMAN_REPONSES_20261011.zip'
blob = subprocess.check_output(['git', 'show', REF + ':' + ARCHIVE], cwd=ROOT)
with zipfile.ZipFile(io.BytesIO(blob)) as archive:
    names = [n for n in archive.namelist() if n.endswith('/cyclic_designs22.json')]
    assert len(names) == 1, names
    raw = archive.read(names[0])
    (OUT / 'cyclic_designs22.json').write_bytes(raw)
    seeds = json.loads(raw)
    print('Recovered archived design seeds:', len(seeds['designs']))
source_path = 'dossiers_externes/HOFFMAN_UPDATE_20261011/code/rows22.cpp'
source = subprocess.check_output(['git', 'show', REF + ':' + source_path], cwd=ROOT)
(OUT / 'lab_rows22.cpp').write_bytes(source)
(OUT / 'provenance.json').write_text(json.dumps({
    'commit': REF, 'archive': ARCHIVE, 'member': names[0],
    'designs_sha256': hashlib.sha256(raw).hexdigest(),
    'row_enumerator': source_path,
    'row_enumerator_sha256': hashlib.sha256(source).hexdigest(),
    'scope': 'Existing seeds retrieved, no repetition of the symmetric-design census'
}, indent=2), encoding='utf-8')
