"""Exact rank-over-F_p constraint by unrestricted U V factorization.

This uses two independent rectangular factors, not U U^t: a fixed symmetric
factorization would silently assume a quadratic-form type. No pivot set,
principal basis, or unproved lower-rank conjecture is selected.
"""


def add_modular_rank_bound(model, matrix, bound, prime=7, name="rank7"):
    rows=len(matrix)
    columns=len(matrix[0]) if rows else 0
    assert rows and columns and 0<=bound<=min(rows,columns)
    assert prime==7, "This first use is specifically over the field F_7."
    if bound==0:
        for i in range(rows):
            for j in range(columns):
                residue,edge=matrix[i][j]
                model.add(residue-edge==0)
        return {"prime":prime,"bound":0,"rows":rows,"columns":columns,"factor_variables":0,"product_variables":0}
    left=[[model.new_int_var(0,prime-1,f"{name}_u_{i}_{a}") for a in range(bound)] for i in range(rows)]
    right=[[model.new_int_var(0,prime-1,f"{name}_v_{a}_{j}") for j in range(columns)] for a in range(bound)]
    maximum_product=(prime-1)**2
    for i in range(rows):
        for j in range(columns):
            products=[]
            for a in range(bound):
                value=model.new_int_var(0,maximum_product,f"{name}_p_{i}_{j}_{a}")
                model.add_multiplication_equality(value,[left[i][a],right[a][j]])
                products.append(value)
            residue,edge=matrix[i][j]
            # Each target is residue-edge, with 0<=residue<=6 and edge binary.
            # It lies in [-1,6]; hence the quotient is nonnegative when the
            # nonnegative product sum has that residue modulo seven.
            quotient=model.new_int_var(0,(bound*maximum_product+1)//prime+1,f"{name}_q_{i}_{j}")
            model.add(sum(products)==residue-edge+prime*quotient)
    return {"prime":prime,"bound":bound,"rows":rows,"columns":columns,
            "factor_variables":bound*(rows+columns),
            "product_variables":rows*columns*bound,"quotient_variables":rows*columns,
            "encoding":"Unrestricted U*V over F_7, equivalent to rank<=bound."}


def add_four_star_rank7(model,labels,graph,root_lines,bound=28):
    letters={a for i in root_lines for a in (2*i,2*i+1)}
    selected=[i for i,p in enumerate(labels) if letters.intersection(p)]
    assert len(selected)==44
    matrix=[]
    for i in selected:
        row=[]
        for j in selected:
            p,q=labels[i],labels[j]
            baseline=24*int(i==j)-3*len(set(p)&set(q))-sum((a^1) in q for a in p)+2
            # 8 T_ij = baseline-8 Gamma_ij == baseline-Gamma_ij (mod 7).
            row.append((baseline%7,graph[i][j]))
        matrix.append(row)
    info=add_modular_rank_bound(model,matrix,bound,7,"fourstar_rank7")
    info.update(root_lines=list(root_lines),selected_label_indices=selected,
                target="8*T on the complete four-star principal block",
                necessary_bound_source="Accepted global r7<=43 and local rank r7-15 (LAB941/L22).",
                performance_improvement_established=False)
    return info
