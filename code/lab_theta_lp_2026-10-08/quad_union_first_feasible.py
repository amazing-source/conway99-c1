"""C1, lab session, 2026-10-09. Decisive form of the union test of NOTE 17.83: for a kernel type with 6 not adjacent to 7,
is there AT LEAST ONE completion of H u H* that passes the mask-multiplicity test of note 222 on the union?
  - yes for a type: the union test does not exclude that type (stop at the first feasible completion);
  - no completion feasible, all completions tested: the type would be excluded (NUMERICAL verdict of a floating LP,
    to be certified exactly before any claim).
The types are taken in the order given on the command line (intended: the types with the fewest partner types).

  python quad_union_first_feasible.py <Codex data folder> <output json> <time limit s> <type> [<type> ...]
One process, below 500 MB. Resumable: a type already decided in the output file is skipped."""
import sys, os, json, time
DATA = sys.argv[1]; OUT = sys.argv[2]; TLIM = float(sys.argv[3]); TYPES = [int(x) for x in sys.argv[4:]]
_argv = sys.argv[:]
sys.argv = [_argv[0], DATA, "run", "unused_none.json", "0"]
import quad_union_mask_lp as u                        # imports quad_partner_kernels as u.q; MODE "run" with no type does nothing
sys.argv = _argv
q = u.q


class Found(Exception):
    pass


class Timeout(Exception):
    pass


class Collector:
    """Stands for the list 'every' of quad_partner_kernels.partners: tests each completion as it is produced."""
    def __init__(self, t0):
        self.t0 = t0; self.tested = 0; self.infeasible = 0; self.other = 0; self.first = None

    def append(self, item):
        if time.time() - self.t0 > TLIM: raise Timeout()
        c, a = item; v, k = u.lp_verdict(a, len(a)); self.tested += 1
        if v == "feasible":
            self.first = {"partner_labelled": c, "partner_type": q.canon(c), "adjacency_bitmasks": list(a), "masks": k}
            raise Found()
        if v == "infeasible": self.infeasible += 1
        else: self.other += 1


res = json.load(open(OUT)) if os.path.exists(OUT) else {}
t0 = time.time()
for b in TYPES:
    if str(b) in res and res[str(b)]["status"] != "TIME LIMIT": continue
    col = Collector(t0); q.PER_TYPE = 10 ** 6
    try:
        q.partners(b, every=col); status = "NO FEASIBLE COMPLETION (numerical)" if col.other == 0 else "UNDECIDED (solver)"
    except Found: status = "feasible completion found"
    except Timeout: status = "TIME LIMIT"
    res[str(b)] = {"status": status, "tested": col.tested, "infeasible_numerical": col.infeasible, "other": col.other, "first_feasible": col.first}
    json.dump(res, open(OUT, "w"))
    print("type %d: %s; completions tested %d (infeasible %d, other %d)%s   [%.0f s]"
          % (b, status, col.tested, col.infeasible, col.other, "" if col.first is None else "; partner type %d" % col.first["partner_type"], time.time() - t0), flush=True)
    if status == "TIME LIMIT": break
done = [b for b in TYPES if str(b) in res and res[str(b)]["status"] != "TIME LIMIT"]
print("decided %d of %d listed types: feasible %d, no feasible completion %d, undecided %d"
      % (len(done), len(TYPES), sum(res[str(b)]["status"].startswith("feasible") for b in done),
         sum(res[str(b)]["status"].startswith("NO") for b in done), sum(res[str(b)]["status"].startswith("UNDECIDED") for b in done)))
