"""Transfer an exhaustive Gram cover without choosing a particular witness."""

from itertools import combinations

from root_component_propagation import RECTANGLES


def add_gram_table(model, graph, template, record, matrix=None):
    assert record["exhaustive"] and record["usable_as_gram_cover"]
    assert record["root_prism_budget"] == 51
    edges = [tuple(e) for e in template["nongrid_edges"]]
    anchors = record["anchors"]
    variables = []
    for a, b in record["anchor_pairs"]:
        i, j = anchors[a], anchors[b]
        if matrix is not None:
            variables.append(matrix[i][j])
            continue
        e, f = edges[i], edges[j]
        if i == j:
            expression = 8 - 2 * sum(graph[u][v] for u, v in combinations(RECTANGLES[e], 2))
        else:
            expression = (0 if set(e) & set(f) else 4) - sum(
                graph[u][v] for u in RECTANGLES[e] for v in RECTANGLES[f])
        variable = model.new_int_var(-8, 8, f"gram_anchor_{i}_{j}")
        model.add(variable == expression)
        variables.append(variable)
    signature_tables = record.get("row_signature_tables")
    signature_count = 0
    if record["gram_anchor_values"] and signature_tables is not None:
        selector = model.new_int_var(0, record["gram_count"] - 1, "gram_selector")
        model.add_allowed_assignments([selector] + variables,
                                      [[i] + values for i, values in enumerate(record["gram_anchor_values"])])
        assert len(signature_tables) == 21
        for table in signature_tables:
            rectangle = tuple(table["rectangle"])
            for w in RECTANGLES[rectangle]:
                signatures = []
                for anchor in anchors:
                    target = edges[anchor]
                    base = 2 if rectangle == target else (0 if set(rectangle) & set(target) else 1)
                    h = model.new_int_var(-3, 2, f"h_{w}_{anchor}")
                    model.add(h == base - sum(graph[w][q] for q in RECTANGLES[target]))
                    signatures.append(h)
                model.add_allowed_assignments([selector] + signatures, table["rows"])
                signature_count += 1
    elif record["gram_anchor_values"]:
        model.add_allowed_assignments(variables, record["gram_anchor_values"])
    else:
        model.add(False)
    return {"gram_count": record["gram_count"], "anchors": anchors,
            "exhaustive": True, "fixed_single_gram": False,
            "normalizes_template_preserving_root_relabelings": record.get("coverage_up_to_template_relabeling", False),
            "individual_vertex_Schur_tables": signature_count,
            "separate_corner_realizations_filtered": record["requires_separate_corner_realization"]}
