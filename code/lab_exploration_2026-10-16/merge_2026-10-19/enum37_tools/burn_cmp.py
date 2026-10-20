"""C++ explicit Burnside (plain and adm) vs Python wreath Burnside and vs enumerator fastcount --adm"""
import json, os, subprocess, sys, time
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16\merge_2026-10-19")
from enum37_burnside import partitions, count_lambda, zee, type_of_partition
m = int(sys.argv[1]); exe = sys.argv[2]; budget = float(sys.argv[3]); out = sys.argv[4]; do_enum = sys.argv[5] == "1"; zmax = float(sys.argv[6])
n = 2 * m
done = set()
if os.path.exists(out):
    for l in open(out): done.add(json.loads(l)["lambda"])
t0 = time.time(); ok = True
lams = sorted(partitions(n), key=lambda l: zee(type_of_partition(l, n)))
for lam in lams:
    arg = ",".join(map(str, lam))
    z = zee(type_of_partition(lam, n))
    if arg in done or z > zmax: continue
    if time.time() - t0 > budget: print("budget stop"); break
    if os.path.exists(os.path.join(os.path.dirname(out), "..", "suspended.json")): print("suspended"); break
    b = count_lambda(lam, n)["N"]
    r1 = json.loads(subprocess.run([exe, arg, "--burnside"], capture_output=True, text=True).stdout)
    r2 = json.loads(subprocess.run([exe, arg, "--burnside", "--adm"], capture_output=True, text=True).stdout)
    rec = {"lambda": arg, "z": z, "burnside_py": b, "burnside_cpp": r1["classes"], "adm_burnside": r2["classes"],
           "div": r1["divisible"] and r2["divisible"], "wall": r1["wall_s"] + r2["wall_s"]}
    if do_enum:
        r3 = json.loads(subprocess.run([exe, arg, "--fastcount", "--adm"], capture_output=True, text=True).stdout.strip().splitlines()[-1])
        rec["adm_enum"] = r3["classes"]
    good = rec["burnside_cpp"] == b and rec["div"] and (not do_enum or rec["adm_enum"] == rec["adm_burnside"])
    rec["ok"] = good; ok &= good
    open(out, "a").write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)
print("all_ok so far:", ok, "wall %.1f" % (time.time() - t0))
