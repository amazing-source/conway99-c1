"""Inventory of every research note on the PC and in every git branch (LAB, chantier of 20/10/2026).

Sources:
  - git repositories (every local and remote-tracking branch, read through git plumbing, no checkout);
  - folders on disk (walked; the folder claude-codex-bridge and the files mdp.txt / auth.json are never opened).
"Notes" are files with a note-like extension (NOTE_EXT).  Every note is identified by its git blob hash (sha1 of
"blob <size>\\0" + content), so identical copies in different repos, branches and folders collapse into one record.
Output (in <out>):
  notes.jsonl     one record per distinct content: blob, size, ext, title, first date, locations
                  (kind git/fs, repo or root, branch, path, date)
  summary.json    counts per source, extension and month; duplicates
  other_files.csv per source and extension, the count and total size of non-note files (code, data)
usage: python inventory.py <config.json> <out dir>
config: {"git": [repo paths], "fs": [folder paths], "fs_exclude_dirs": [names]}"""
import collections
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import time

NOTE_EXT = {".md", ".txt", ".tex", ".rst", ".org", ".pdf", ".ipynb"}
SKIP_DIRS = {"claude-codex-bridge", ".git", "__pycache__", "node_modules"}
SKIP_FILES = {"mdp.txt", "auth.json"}
DATE_RE = re.compile(r"(20\d\d)[-_]?(\d\d)[-_]?(\d\d)")
DMY_RE = re.compile(r"(\d\d)[-_/](\d\d)[-_/](20\d\d)")


def path_date(p):
    m = DATE_RE.search(p)
    if m and 1 <= int(m.group(2)) <= 12 and 1 <= int(m.group(3)) <= 31:
        return "%s-%s-%s" % m.groups()
    m = DMY_RE.search(p)
    if m and 1 <= int(m.group(2)) <= 12:
        return "%s-%s-%s" % (m.group(3), m.group(2), m.group(1))
    return None


def title_of(data, ext):
    if ext == ".pdf":
        return "(pdf)"
    try:
        text = data[:4000].decode("utf-8", "replace")
    except Exception:
        return ""
    for line in text.splitlines():
        s = line.strip().lstrip("#").strip()
        if s:
            return s[:160]
    return ""


def blob_hash(data):
    h = hashlib.sha1(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, "-c", "core.quotepath=false"] + list(args), capture_output=True)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else ""


def scan_git(repo, notes, other):
    name = os.path.basename(os.path.normpath(repo))
    refs = []
    for line in git(repo, "for-each-ref", "--format=%(refname)\t%(committerdate:short)", "refs/heads",
                    "refs/remotes").splitlines():
        ref, date = line.split("\t")
        if ref.endswith("/HEAD"):
            continue
        refs.append((ref, date))
    added = {}
    cur = None
    for line in git(repo, "log", "--all", "--diff-filter=A", "--format=COMMIT %cs", "--name-only").splitlines():
        if line.startswith("COMMIT "):
            cur = line[7:]
        elif line.strip() and cur:
            p = line.strip()
            if p not in added or cur < added[p]:
                added[p] = cur
    want = {}
    for ref, rdate in refs:
        for line in git(repo, "ls-tree", "-r", "--long", ref).splitlines():
            try:
                meta, path = line.split("\t", 1)
                mode, typ, blob, size = meta.split()
            except ValueError:
                continue
            if typ != "blob":
                continue
            ext = os.path.splitext(path)[1].lower()
            size = int(size) if size.isdigit() else 0
            if ext in NOTE_EXT:
                date = added.get(path) or path_date(path) or rdate
                loc = {"kind": "git", "repo": name, "branch": ref.replace("refs/remotes/", "").replace("refs/heads/", ""),
                       "path": path, "date": date}
                rec = notes.get(blob)
                if rec is None:
                    want[blob] = (ext, size)
                    notes[blob] = {"blob": blob, "size": size, "ext": ext, "title": None, "locations": [loc]}
                else:
                    rec["locations"].append(loc)
            else:
                k = ("git:" + name, ext)
                c = other.setdefault(k, [0, 0, set()])
                if blob not in c[2]:
                    c[2].add(blob)
                    c[0] += 1
                    c[1] += size
    if want:
        p = subprocess.Popen(["git", "-C", repo, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        for blob, (ext, size) in want.items():
            p.stdin.write((blob + "\n").encode())
            p.stdin.flush()
            header = p.stdout.readline().split()
            if len(header) < 3:
                continue
            n = int(header[2])
            data = p.stdout.read(n)
            p.stdout.read(1)
            notes[blob]["title"] = title_of(data, ext)
        p.stdin.close()
        p.wait()
    return len(refs)


def scan_fs(root, notes, other, exclude):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and d not in exclude]
        for fn in files:
            if fn in SKIP_FILES:
                continue
            p = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1].lower()
            try:
                st = os.stat(p)
            except OSError:
                continue
            if ext in NOTE_EXT and st.st_size <= 50 * 1024 * 1024:
                try:
                    data = open(p, "rb").read()
                except OSError:
                    continue
                blob = blob_hash(data)
                date = path_date(p) or time.strftime("%Y-%m-%d", time.localtime(st.st_mtime))
                loc = {"kind": "fs", "repo": root, "branch": "", "path": os.path.relpath(p, root), "date": date,
                       "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))}
                rec = notes.get(blob)
                if rec is None:
                    notes[blob] = {"blob": blob, "size": st.st_size, "ext": ext, "title": title_of(data, ext),
                                   "locations": [loc]}
                else:
                    rec["locations"].append(loc)
                    if rec["title"] is None:
                        rec["title"] = title_of(data, ext)
            else:
                k = ("fs:" + root, ext)
                c = other.setdefault(k, [0, 0, None])
                c[0] += 1
                c[1] += st.st_size


def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    notes, other, nrefs = {}, {}, {}
    t = time.time()
    for repo in cfg.get("git", []):
        nrefs[repo] = scan_git(repo, notes, other)
        print("git %-70s refs %4d  distinct notes so far %6d  (%.0f s)" % (repo, nrefs[repo], len(notes),
                                                                            time.time() - t), flush=True)
    for root in cfg.get("fs", []):
        scan_fs(root, notes, other, set(cfg.get("fs_exclude_dirs", [])))
        print("fs  %-70s distinct notes so far %6d  (%.0f s)" % (root, len(notes), time.time() - t), flush=True)
    for rec in notes.values():
        rec["first_date"] = min((l["date"] for l in rec["locations"] if l.get("date")), default=None)
    recs = sorted(notes.values(), key=lambda r: (r["first_date"] or "9999", r["locations"][0]["path"]))
    with open(os.path.join(out, "notes.jsonl"), "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    by_src = collections.Counter()
    for r in recs:
        for src in {(l["kind"] + ":" + os.path.basename(l["repo"].rstrip("/\\"))) for l in r["locations"]}:
            by_src[src] += 1
    summary = {"distinct_notes": len(recs),
               "total_locations": sum(len(r["locations"]) for r in recs),
               "by_extension": collections.Counter(r["ext"] for r in recs),
               "by_month": collections.Counter((r["first_date"] or "?")[:7] for r in recs),
               "by_source": by_src, "git_refs": nrefs,
               "total_bytes": sum(r["size"] for r in recs), "elapsed_s": round(time.time() - t)}
    json.dump(summary, open(os.path.join(out, "summary.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(os.path.join(out, "other_files.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "extension", "count", "bytes"])
        for (src, ext), (n, b, _) in sorted(other.items(), key=lambda kv: -kv[1][1]):
            w.writerow([src, ext, n, b])
    print(json.dumps({k: v for k, v in summary.items() if k in ("distinct_notes", "total_locations", "total_bytes",
                                                                "elapsed_s")}))


if __name__ == "__main__":
    main()
