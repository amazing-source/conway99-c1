"""Validate all packaged file digests. Does not perform mathematical verification."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1]
count=0
for line in (root/'SHA256SUMS').read_text().splitlines():
    expected,name=line.split('  ',1)
    path=(root/name).resolve()
    if not path.is_relative_to(root):raise SystemExit('Unsafe manifest path')
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected:raise SystemExit('Digest mismatch: '+name)
    count+=1
print(f'OK: {count} packaged file digests')
