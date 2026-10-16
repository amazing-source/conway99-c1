"""Run one SAT solver on a CNF with a wall-clock limit (LAB 16/10/2026).
  cadical: the win64 binary with extra options (e.g. --unsat), stdout to <cnf>.<tag>.out
  kissat:  python-sat's kissat404 (no proof), via solve() in a child process killed at the limit
usage: python run_solver.py <cnf> <tag> <seconds> cadical <exe> [options...]
       python run_solver.py <cnf> <tag> <seconds> kissat"""
import multiprocessing as mp
import subprocess
import sys
import time


def kissat_child(path, q):
    from pysat.formula import CNF
    from pysat.solvers import Solver
    f = CNF(from_file=path)
    with Solver(name="kissat404", bootstrap_with=f.clauses) as s:
        q.put(s.solve())


if __name__ == "__main__":
    cnf, tag, secs, kind = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    t0 = time.time()
    if kind == "cadical":
        exe, extra = sys.argv[5], sys.argv[6:]
        with open(cnf + "." + tag + ".out", "w") as fo:
            p = subprocess.Popen([exe, "-q"] + extra + [cnf], stdout=fo, stderr=subprocess.DEVNULL)
            try:
                p.wait(timeout=secs)
                st = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "UNKNOWN(%d)" % p.returncode)
            except subprocess.TimeoutExpired:
                p.kill()
                p.wait()
                st = "TIMEOUT"
    else:
        q = mp.Queue()
        p = mp.Process(target=kissat_child, args=(cnf, q))
        p.start()
        p.join(secs)
        if p.is_alive():
            p.kill()
            p.join()
            st = "TIMEOUT"
        else:
            r = q.get() if not q.empty() else None
            st = {True: "SAT", False: "UNSAT", None: "UNKNOWN"}[r]
    print("%s %s: %s in %.1f s" % (tag, cnf, st, time.time() - t0), flush=True)
