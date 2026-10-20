"""Rescue of the LAB session scratchpad (session started 30/09/2026) into work/ (LAB 20/10/2026).

The scratchpad is temporary and tied to the session.  This script:
1. copies as-is every small file (<= 2 MB, any type except compiled binaries) and every text-like file <= 10 MB,
   keeping relative paths, into <dest>/files/;
2. puts everything else (big data: CNF, DRAT, run inputs, big outputs) into one .tar.gz per top-level entry under
   <dest>/archives/ (root-level big files go to root_bulk.tar.gz);
3. skips the git clone c1merge/ (everything committed is on GitHub; checked separately), __pycache__ and compiled
   binaries (.exe, .obj, .o, .pyc: rebuilt from the sources, which are copied);
4. writes <dest>/MANIFEST.csv (every file: relative path, size, action, sha256 for copied files).
Read-only on the source.  usage: python rescue.py <scratchpad> <dest>"""
import csv
import hashlib
import os
import sys
import tarfile
import time

SRC, DEST = sys.argv[1], sys.argv[2]
TEXT = {".md", ".txt", ".py", ".cpp", ".c", ".h", ".hpp", ".cc", ".inc", ".sh", ".ps1", ".bat", ".json", ".jsonl",
        ".csv", ".tsv", ".tex", ".bib", ".log", ".out", ".err", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".sage",
        ".g", ".gap", ".m", ".lean", ".patch", ".diff", ".html", ".svg", ".gz"}
BINARY_SKIP = {".exe", ".obj", ".o", ".pyc", ".pdb", ".ilk"}
SKIP_TOP = {"c1merge"}
SMALL, TEXT_MAX = 2 * 1024 * 1024, 10 * 1024 * 1024


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    t0 = time.time()
    files_dir = os.path.join(DEST, "files")
    arch_dir = os.path.join(DEST, "archives")
    os.makedirs(files_dir, exist_ok=True)
    os.makedirs(arch_dir, exist_ok=True)
    rows, bulk = [], {}
    for root, dirs, fnames in os.walk(SRC):
        rel_root = os.path.relpath(root, SRC)
        top = rel_root.split(os.sep)[0] if rel_root != "." else "."
        if top in SKIP_TOP:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d != "__pycache__" and not (rel_root == "." and d in SKIP_TOP)]
        for fn in fnames:
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, SRC)
            try:
                size = os.path.getsize(p)
            except OSError:
                rows.append((rel, -1, "unreadable", ""))
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in BINARY_SKIP:
                rows.append((rel, size, "skipped:compiled-binary", ""))
                continue
            if size <= SMALL or (ext in TEXT and size <= TEXT_MAX):
                q = os.path.join(files_dir, rel)
                os.makedirs(os.path.dirname(q), exist_ok=True)
                try:
                    with open(p, "rb") as fi, open(q, "wb") as fo:
                        while True:
                            b = fi.read(1 << 20)
                            if not b:
                                break
                            fo.write(b)
                    rows.append((rel, size, "copied", sha256(q)))
                except OSError as e:
                    rows.append((rel, size, "copy-failed:%s" % e, ""))
            else:
                key = top if top != "." else "root_bulk"
                bulk.setdefault(key, []).append((p, rel, size))
    for key, items in sorted(bulk.items()):
        name = "%s.tar.gz" % key.replace(os.sep, "_")
        ap = os.path.join(arch_dir, name)
        with tarfile.open(ap, "w:gz", compresslevel=6) as tf:
            for p, rel, size in items:
                try:
                    tf.add(p, arcname=rel)
                    rows.append((rel, size, "archived:" + name, ""))
                except OSError as e:
                    rows.append((rel, size, "archive-failed:%s" % e, ""))
        print("archive %s: %d files, %.1f MB raw -> %.1f MB" % (name, len(items), sum(s for _, _, s in items) / 1e6,
                                                             os.path.getsize(ap) / 1e6), flush=True)
    with open(os.path.join(DEST, "MANIFEST.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["relative_path", "size_bytes", "action", "sha256_of_copy"])
        w.writerows(sorted(rows))
    copied = [r for r in rows if r[2] == "copied"]
    print("files copied: %d (%.1f MB); archived: %d; skipped: %d; failures: %d; %.0f s" % (
        len(copied), sum(r[1] for r in copied) / 1e6, sum(1 for r in rows if r[2].startswith("archived")),
        sum(1 for r in rows if r[2].startswith("skipped")), sum(1 for r in rows if "failed" in r[2] or r[2] == "unreadable"),
        time.time() - t0))


if __name__ == "__main__":
    main()
