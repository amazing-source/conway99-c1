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
    corner_table_count,corner_row_count=0,0
    pair_table_count,pair_row_count=0,0
    if record["gram_anchor_values"] and signature_tables is not None:
        selector = model.new_int_var(0, record["gram_count"] - 1, "gram_selector")
        model.add_allowed_assignments([selector] + variables,
                                      [[i] + values for i, values in enumerate(record["gram_anchor_values"])])
        assert len(signature_tables) == 21
        corner_tables={tuple(t['rectangle']):t for t in record.get('corner_signature_tables',[])}
        corner_selectors={}
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
                if rectangle in corner_tables:
                    catalog=corner_tables[rectangle]['catalog']
                    state=model.new_int_var(0,max(0,len(catalog)-1),f'corner_signature_{w}')
                    model.add_allowed_assignments([state]+signatures,[[i]+h for i,h in enumerate(catalog)])
                    corner_selectors[w]=state
                signature_count += 1
        for rectangle,table in corner_tables.items():
            corners=RECTANGLES[rectangle]
            if table.get('encoding')=='existential_square_orientations_v1':
                from root_component_corner_orbits import add_factored_table
                add_factored_table(model,selector,corner_selectors,corners,graph,table)
            else:
                assert 'encoding' not in table
                columns=[selector]+[corner_selectors[w] for w in corners]+[graph[u][v] for u,v in combinations(corners,2)]
                model.add_allowed_assignments(columns,table['rows'])
            corner_table_count+=1;corner_row_count+=len(table['rows'])
        if record.get('pair_signature_forbidden_tables'):
            from root_component_pair_schur_cover import pair_types
            pairs=pair_types()
            for table in record['pair_signature_forbidden_tables']:
                q,r=map(tuple,table['rectangles'])
                key=(q,r,table['common_labels'],table['mate_common_labels'])
                for u,v in pairs[key]:
                    edge=graph[u][v]
                    if isinstance(edge,int):
                        rows=[row[:3] for row in table['rows'] if row[3]==edge]
                        columns=[selector,corner_selectors[u],corner_selectors[v]]
                    else:
                        rows=table['rows']
                        columns=[selector,corner_selectors[u],corner_selectors[v],edge]
                    if rows:
                        model.add_forbidden_assignments(columns,rows)
                        pair_table_count+=1;pair_row_count+=len(rows)
    elif record["gram_anchor_values"]:
        model.add_allowed_assignments(variables, record["gram_anchor_values"])
    else:
        model.add(False)
    return {"gram_count": record["gram_count"], "anchors": anchors,
            "exhaustive": True, "fixed_single_gram": False,
            "normalizes_template_preserving_root_relabelings": record.get("coverage_up_to_template_relabeling", False),
            "individual_vertex_Schur_tables": signature_count,
            "coupled_corner_tables":corner_table_count,"coupled_corner_rows":corner_row_count,
            "pair_signature_tables":pair_table_count,"pair_signature_forbidden_rows":pair_row_count,
            "separate_corner_realizations_filtered": record["requires_separate_corner_realization"]}
