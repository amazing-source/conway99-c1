"""Ablation of the rank-37 line obligation (LAB 20/10/2026, step 2 of the plan agreed with the user).
For c = 1 generic lines with (tau | 7) = -1 (seeds 1, 2, 4, 5; the only ones possible at rank 37 by Codex's L23),
re-run oblr2 with one family of exact constraints switched off (OBLR_ABL letters: m = margins L1, l = L3, a = lambda
for adjacent far vertices, d = far degree 8, e = near-far counts, c = far-far common neighbours), and with all of them
off (only the forced 7-adic values in {0,1} and the bijections remain).  Runs at IDLE priority (one process at a
time; the children inherit the priority class).  usage: python abl_batch.py <scratch dir> <seconds> <out.jsonl>"""
import ctypes
import json
import os
import subprocess
import sys

if sys.platform == "win32":
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)   # IDLE_PRIORITY_CLASS
HERE = os.path.dirname(os.path.abspath(__file__))
S, SEC, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
PY = sys.executable
configs = ["", "m", "l", "a", "d", "e", "c", "mladec"]
for seed in (1, 2, 4, 5):
    f = os.path.join(S, "abl_s%d.bin" % seed)
    subprocess.run([PY, os.path.join(HERE, "oblr_prep.py"), "c1", str(seed), "0", "0", "1", f], capture_output=True)
    for cfg in configs:
        env = dict(os.environ, OBLR_ABL=cfg)
        r = subprocess.run([os.path.join(HERE, "oblr2.exe"), f, SEC], capture_output=True, text=True, env=env)
        line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '{"error": "%s"}' % r.stderr[-200:]
        rec = {"seed": seed, "ablated": cfg or "none", "res": json.loads(line)}
        with open(OUT, "a") as g:
            g.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)
    os.remove(f)
print("DONE", flush=True)
