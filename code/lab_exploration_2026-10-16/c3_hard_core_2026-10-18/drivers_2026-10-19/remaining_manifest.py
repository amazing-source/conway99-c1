"""At AWS launch time: write manifest_p3prod_remaining.tsv = the jobs of manifest_p3prod.tsv whose output shard does not
exist locally (pkg/data/p3_shards).  Stop the local drivers FIRST (a job running locally has no output yet and would be
duplicated, which is harmless but wasteful)."""
from pathlib import Path

base = Path(__file__).resolve().parent
jobs = [l.rstrip("\n") for l in open(base / "manifest_p3prod.tsv", encoding="utf8") if l.strip()]
rem = [j for j in jobs if not (base / "pkg" / j.split("\t")[3]).exists()]
(base / "manifest_p3prod_remaining.tsv").write_text("\n".join(rem) + "\n")
print("jobs total", len(jobs), "done locally", len(jobs) - len(rem), "remaining", len(rem))
