# Probe which Python sequence operations on OR-Tools 9.15 proto repeated fields are wrong.
from ortools.sat.python import cp_model
import ortools
m = cp_model.CpModel()
x = m.new_int_var(-2, 3, "x")
y = m.new_int_var_from_domain(cp_model.Domain.from_values([2, 4, 6, 8]), "y")
m.add(2 * x + 3 * y <= 7)
print("ortools", ortools.__version__)
for name, f in [("x.domain", m.proto.variables[0].domain), ("y.domain", m.proto.variables[1].domain),
                ("lin.vars", m.proto.constraints[0].linear.vars), ("lin.coeffs", m.proto.constraints[0].linear.coeffs),
                ("lin.domain", m.proto.constraints[0].linear.domain)]:
    L = list(f)
    ops = {"[-1]": lambda s: s[-1], "[-2]": lambda s: s[-2], "[len-1]": lambda s: s[len(s) - 1],
           "[:-1]": lambda s: list(s[:-1]), "[-1:]": lambda s: list(s[-1:]), "[::-1]": lambda s: list(s[::-1]),
           "reversed": lambda s: list(reversed(s)), "max": lambda s: max(s), "min": lambda s: min(s),
           "sorted": lambda s: sorted(s), "tuple": lambda s: tuple(s), "len": lambda s: len(s),
           "in": lambda s: (L[-1] in s), "==list": lambda s: (s == L), "[1:]": lambda s: list(s[1:])}
    bad = []
    for k, op in ops.items():
        try:
            got, want = op(f), op(L)
        except Exception as e:
            got, want = "EXC " + type(e).__name__, op(L)
        if got != want and not (k == "tuple" and list(got) == list(want)):
            bad.append(f"{k}: got {got} want {want}")
    print(name, type(f).__name__, L, "| WRONG:" if bad else "| all ok", "; ".join(bad))
