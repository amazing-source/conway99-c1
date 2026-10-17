"""All four-corner Schur realizations of a fixed rectangle Gram."""

from itertools import combinations,product

from root_component_gram_enumeration import integer_psd
from root_rectangle_domains import corner_graphs
from root_component_propagation import RECTANGLES


def enumerate_corner_rows(edges,matrix,domains,anchors,det,adj):
    result=[]
    for rectangle,corners in RECTANGLES.items():
        item=domains[rectangle]
        signatures=[tuple(h) for h in item["signatures"]]
        coordinate=edges.index(rectangle) if rectangle in edges else None
        energy=int(matrix[coordinate,coordinate]) if coordinate is not None else 0
        patterns=corner_graphs(4-energy//2)
        reduced=[tuple(h[i] for i in anchors) for h in signatures]
        gram=[[sum(a[i]*adj[i][j]*b[j] for i in range(len(anchors)) for j in range(len(anchors)))
               for b in reduced] for a in reduced]
        rows=[]
        target=tuple(item["target"])
        for adjacency,t4,degrees in patterns:
            choices=[[i for i,h in enumerate(signatures) if coordinate is None or h[coordinate]==value] for value in degrees]
            sums={}
            for k,l in product(choices[2],choices[3]):
                key=tuple(a+b for a,b in zip(signatures[k],signatures[l]))
                sums.setdefault(key,[]).append((k,l))
            for i,j in product(choices[0],choices[1]):
                needed=tuple(t-a-b for t,a,b in zip(target,signatures[i],signatures[j]))
                for k,l in sums.get(needed,[]):
                    indices=(i,j,k,l)
                    residual=[[det*t4[a][b]-4*gram[indices[a]][indices[b]] for b in range(4)] for a in range(4)]
                    if integer_psd(residual):
                        rows.append(list(indices)+[adjacency[a][b] for a,b in combinations(range(4),2)])
        result.append({"rectangle":rectangle,"rows":rows})
    return result


def add_corner_tables(model,graph,selectors,edges,matrix,domains,anchors,det,adj):
    tables=enumerate_corner_rows(edges,matrix,domains,anchors,det,adj)
    for table in tables:
        corners=RECTANGLES[table["rectangle"]]
        columns=[selectors[w] for w in corners]+[graph[u][v] for u,v in combinations(corners,2)]
        model.add_allowed_assignments(columns,table["rows"])
    return {"tables":21,"rows":sum(len(t["rows"]) for t in tables),
            "test":"Exact four-corner conditional PSD and four-signature sums."}
