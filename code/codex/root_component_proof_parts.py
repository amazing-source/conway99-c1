"""Transport a large checked compressed proof in byte-exact Git-sized parts.

The source file is retained locally. Restoring concatenates the parts and
requires their sizes/hashes AND the original compressed-file hash to match.
No proof or CNF content is edited.
"""

import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def pack(paths, manifest, part_bytes=32*1024*1024):
    assert part_bytes>0
    manifest=Path(manifest);artifacts={}
    for path in map(Path,paths):
        assert path.resolve().parent==manifest.resolve().parent
        assert path.is_file()
        parts=[];full=hashlib.sha256();size=0
        with path.open('rb') as f:
            while True:
                raw=f.read(part_bytes)
                if not raw:break
                name=path.name+'.part%03d'%(len(parts)+1);target=path.with_name(name)
                expected=hashlib.sha256(raw).hexdigest()
                if target.exists():assert digest(target)==expected
                else:target.write_bytes(raw)
                full.update(raw);size+=len(raw)
                parts.append({'name':name,'bytes':len(raw),'sha256':expected})
        artifacts[path.name]={'compressed_bytes':size,'compressed_sha256':full.hexdigest(),'parts':parts}
    result={'format':'byte-concatenation-v1','artifacts':artifacts}
    manifest.write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8')
    return result


def restore(manifest):
    manifest=Path(manifest);data=json.loads(manifest.read_text(encoding='utf-8'))
    assert data['format']=='byte-concatenation-v1'
    for name,artifact in data['artifacts'].items():
        target=manifest.parent/name
        assert target.resolve().parent==manifest.resolve().parent
        if target.exists():
            assert target.stat().st_size==artifact['compressed_bytes'] and digest(target)==artifact['compressed_sha256']
            continue
        temporary=target.with_name(target.name+'.restore.tmp');assert not temporary.exists()
        full=hashlib.sha256();total=0
        try:
            with temporary.open('xb') as output:
                for part in artifact['parts']:
                    source=manifest.parent/part['name']
                    assert source.resolve().parent==manifest.resolve().parent
                    h=hashlib.sha256();count=0
                    with source.open('rb') as stream:
                        for chunk in iter(lambda:stream.read(1024*1024),b''):
                            output.write(chunk);full.update(chunk);h.update(chunk);count+=len(chunk)
                    assert count==part['bytes'] and h.hexdigest()==part['sha256']
                    total+=count
            assert total==artifact['compressed_bytes'] and full.hexdigest()==artifact['compressed_sha256']
            temporary.rename(target)
        finally:
            if temporary.exists():temporary.unlink()
    return data


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('pack');s.add_argument('manifest',type=Path);s.add_argument('files',type=Path,nargs='+')
    s=sub.add_parser('restore');s.add_argument('manifest',type=Path)
    a=p.parse_args()
    r=pack(a.files,a.manifest) if a.command=='pack' else restore(a.manifest)
    print(json.dumps({'artifacts':len(r['artifacts']),'manifest':str(a.manifest)}))
