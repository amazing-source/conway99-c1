"""V10: exact residual block and an exhaustive invariant partition of (0,2).

Branching uses the unordered residual degrees of e,f and the class of their
unique common neighbour. Both label orientations are retained. This is a
necessary model until the remaining mixed equations / exact completion pass.
"""
from itertools import combinations

from coclique_column_coexistence import build as base_build


def branches():
    answer = []
    for a in range(1, 7):
        for b in range(a, 7):
            if a+b > 11:
                continue
            for location in ('C8', 'C13', 'ZH', 'Z0'):
                if location in ('C8', 'Z0') and a == 1:
                    continue
                if location == 'C13' and b == 6:
                    continue
                if a+b == 11 and location != 'C8':
                    continue
                answer.append(dict(id=f'r{a}_{b}_{location}', degrees=[a, b],
                                   common_neighbour_class=location))
    assert len(answer) == 61
    return answer


class Products:
    def __init__(self, model):
        self.model, self.cache = model, {}

    def __call__(self, a, b):
        if isinstance(a, int):
            return b if a else 0
        if isinstance(b, int):
            return a if b else 0
        if a.index == b.index:
            return a
        key = tuple(sorted((a.index, b.index)))
        if key not in self.cache:
            x = self.model.new_bool_var(f'v10_product{len(self.cache)}')
            self.model.add(x <= a)
            self.model.add(x <= b)
            self.model.add(x >= a+b-1)
            self.cache[key] = x
        return self.cache[key]


def add_residual_block(model, M, edge, mu=2, caps_only=False):
    """Complete M-M equations, reusing the existing B-overlap variables.

With A regular and B-B exact, all off-diagonal caps <=mu already imply
these equalities by conservation. The explicit equalities propagate better
in principle; the actual performance must be measured.
"""
    indices = {v.name: i for i, v in enumerate(model.proto.variables)
               if v.name.startswith('overlap')}
    mul = Products(model)
    for u, v in combinations(M, 2):
        overlap = model.get_int_var_from_proto_index(indices[f'overlap{u}_{v}'])
        expression = overlap+edge(u, v)+sum(
            mul(edge(u, w), edge(v, w)) for w in M if w not in (u, v))
        model.add(expression <= mu if caps_only else expression == mu)
    return mul


def build(branch_id=None, residual=True):
    model, B, M, edge, meta = base_build(
        mixed='coclique', saturated=True, triangles=True,
        rook_cut=True, center_kind='conditional')
    initial = (len(model.proto.variables), len(model.proto.constraints))
    mul = add_residual_block(model, M, edge) if residual else Products(model)
    residual_products = len(mul.cache)
    degree = {}
    for u in M:
        degree[u] = model.new_int_var(1 if u in (37, 38) else 2,
                                     6 if u in (37, 38) else 8, f'v10_degree{u}')
        model.add(degree[u] == sum(edge(u, v) for v in M if u != v))
        c8 = sum(edge(u, c) for c in range(8))
        model.add(degree[u] == 1+c8 if u in (37, 38) else
                  degree[u] == 2+c8+sum(edge(u, x) for x in range(25, 29)))
    # Consequences of the complete H stars and the unique triangle on ef.
    model.add(degree[37]+degree[38] <= 11)
    common = {}
    groups = dict(C8=range(8), C13=range(8, 21), ZH=range(39, 63), Z0=range(63, 99))
    for name, group in groups.items():
        common[name] = model.new_bool_var(f'v10_common_{name}')
        model.add(common[name] == sum(mul(edge(37, v), edge(38, v)) for v in group))
    model.add(sum(common.values()) == 1)
    for location in ('C8', 'Z0'):
        for u in (37, 38):
            model.add(degree[u] >= 2).only_enforce_if(common[location])
    for u in (37, 38):
        model.add(degree[u] <= 5).only_enforce_if(common['C13'])
    model.add(degree[37]+degree[38] <= 10).only_enforce_if(common['C8'].Not())
    # A four-X center is the unique common neighbour of the negative edge.
    # In a branch with the triangle outside its class it therefore cannot exist.
    for i, variable in enumerate(model.proto.variables):
        if variable.name.startswith('four_X_center'):
            v = int(variable.name.removeprefix('four_X_center'))
            model.add(model.get_bool_var_from_proto_index(i) <= common['C13' if v < 21 else 'Z0'])
    chosen = None
    if branch_id is not None:
        chosen = next((item for item in branches() if item['id'] == branch_id), None)
        if chosen is None:
            raise ValueError(f'Unknown branch {branch_id}')
        a, b = chosen['degrees']
        model.add_allowed_assignments([degree[37], degree[38]],
                                      [(a, b)] if a == b else [(a, b), (b, a)])
        model.add(common[chosen['common_neighbour_class']] == 1)
    meta.update(version='V10', branch=chosen, residual_equations=703 if residual else 0,
                residual_product_variables=residual_products,
                extra_variables=len(model.proto.variables)-initial[0],
                extra_constraints=len(model.proto.constraints)-initial[1],
                invariant_partition_size=61, mixed_block_complete=False)
    return model, B, M, edge, meta
