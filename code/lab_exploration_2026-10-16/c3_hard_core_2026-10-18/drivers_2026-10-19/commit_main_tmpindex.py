"""Commit files on top of origin/main of amazing-source/conway99-c1 WITHOUT touching any working index:
a temporary index (GIT_INDEX_FILE) seeded from origin/main, blobs added with hash-object, write-tree, commit-tree,
then a plain (non-force) push of the new commit to main.  Run inside the scratchpad clone c1merge.
usage: python commit_main_tmpindex.py <pairs file local=remote> <message file> [--dry-run]"""
import os
import subprocess
import sys
import time

pairs = [l.strip().split("=", 1) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
msg = sys.argv[2]
DRY = "--dry-run" in sys.argv
here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.join(here, "c1merge")
idx = os.path.join(here, "tmp_index_%d" % int(time.time()))
ENV = dict(os.environ, GIT_AUTHOR_NAME="amazing-source", GIT_AUTHOR_EMAIL="206353265+amazing-source@users.noreply.github.com",
           GIT_COMMITTER_NAME="amazing-source", GIT_COMMITTER_EMAIL="206353265+amazing-source@users.noreply.github.com", GIT_INDEX_FILE=idx)


def git(*a, env=ENV):
    r = subprocess.run(["git", "-c", "core.longpaths=true"] + list(a), cwd=repo, capture_output=True, text=True, env=env)
    if r.returncode:
        raise SystemExit("git %s failed: %s" % (" ".join(a[:3]), r.stderr[-600:]))
    return r.stdout.strip()


git("fetch", "origin", "main")
base = git("rev-parse", "origin/main")
git("read-tree", base)
for local, remote in pairs:
    blob = git("hash-object", "-w", local)
    git("update-index", "--add", "--cacheinfo", "100644,%s,%s" % (blob, remote))
tree = git("write-tree")
commit = git("commit-tree", tree, "-p", base, "-F", msg)
changed = git("diff-tree", "--no-commit-id", "--name-status", "-r", base, commit)
print("base", base[:8], "commit", commit[:8], "files changed:", len(changed.splitlines()))
print("\n".join(changed.splitlines()[:8]))
if not DRY:
    print(git("push", "origin", "%s:refs/heads/main" % commit))
    print("pushed", commit)
os.remove(idx)
