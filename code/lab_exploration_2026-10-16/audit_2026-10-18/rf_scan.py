"""AST scan: flag negative subscripts, negative slices and ==/!= comparisons on values that come from
OR-Tools proto repeated fields (directly, or through a local name assigned from such an expression)."""
import ast, sys, pathlib
FIELDS = {"domain", "vars", "coeffs", "literals", "exprs", "enforcement_literal", "variables", "constraints",
          "solution", "values", "intervals", "demands", "x_intervals", "y_intervals", "tails", "heads"}
def touches_proto(node):
    for n in ast.walk(node):
        if isinstance(n, ast.Attribute) and n.attr in ("proto", "Proto"):
            return True
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "Proto":
            return True
    return False
def wrapped_in_list(node):
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("list", "tuple", "sorted")
def neg(sl):
    if isinstance(sl, ast.UnaryOp) and isinstance(sl.op, ast.USub):
        return True
    if isinstance(sl, ast.Slice):
        return any(neg(x) for x in (sl.lower, sl.upper, sl.step) if x is not None) or True
    return False
hits = []
for path in sys.argv[1:]:
    for f in sorted(pathlib.Path(path).glob("*.py")):
        try:
            tree = ast.parse(f.read_text(encoding="utf-8-sig", errors="replace"))
        except SyntaxError as e:
            hits.append((str(f), 0, "SYNTAX " + str(e))); continue
        tainted = set()
        for n in ast.walk(tree):                         # names assigned from a proto field without list()
            if isinstance(n, ast.Assign) and touches_proto(n.value) and not wrapped_in_list(n.value):
                for t in n.targets:
                    for x in ast.walk(t):
                        if isinstance(x, ast.Name):
                            tainted.add(x.id)
        def is_field(e):
            if isinstance(e, ast.Name) and e.id in tainted:
                return True
            return isinstance(e, ast.Attribute) and e.attr in FIELDS and touches_proto(e)
        for n in ast.walk(tree):
            if isinstance(n, ast.Subscript) and is_field(n.value) and neg(n.slice):
                hits.append((f.name, n.lineno, "negative index/slice: " + ast.unparse(n)[:90]))
            if isinstance(n, ast.Compare) and any(isinstance(o, (ast.Eq, ast.NotEq)) for o in n.ops):
                if any(is_field(x) for x in [n.left] + n.comparators):
                    hits.append((f.name, n.lineno, "==/!= on field: " + ast.unparse(n)[:90]))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "reversed" and n.args and is_field(n.args[0]):
                hits.append((f.name, n.lineno, "reversed(field): " + ast.unparse(n)[:90]))
        if tainted:
            hits.append((f.name, -1, "names assigned from proto (inspect by hand): " + ",".join(sorted(tainted))))
for h in hits:
    print(*h, sep=" | ")
print("files scanned:", sum(len(list(pathlib.Path(p).glob('*.py'))) for p in sys.argv[1:]))
