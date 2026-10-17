"""Prepare complementary Schur corner tables for every Gram in a finite cover.

The Gram selector stays variable. No single witness or component is fixed.
Each corner state stores its actual anchor signature, and every allowed
four-corner row is tied to the Gram that generated it.
"""

from root_component_signature_moments import gram_matrix
from root_rectangle_domains import signature_domains
from root_component_corner_tables import enumerate_corner_rows
from root_component_short_vectors import short_directions,filter_domains
from root_component_upper_signatures import data_for,filter_domains as upper_filter,corner_filter
from root_component_propagation import RECTANGLES


def prepare(template, cover, progress=None):
    edges=[tuple(e) for e in template['nongrid_edges']]
    catalogs={q:[] for q in RECTANGLES};indices={q:{} for q in RECTANGLES}
    rows={q:[] for q in RECTANGLES};individual={q:[] for q in RECTANGLES}
    eliminated=[]
    for gi,values in enumerate(cover['gram_anchor_values']):
        matrix=gram_matrix(cover,values)
        domains={tuple(d['rectangle']):d for d in signature_domains(edges,matrix.tolist())}
        filter_domains(domains,short_directions(matrix))
        upper=data_for(edges,matrix);upper_filter(edges,matrix,domains,upper)
        anchors=list(matrix.rref()[1]);small=matrix.extract(anchors,anchors);det=int(small.det())
        adj=[[int(x) for x in row] for row in (small.inv()*det).tolist()]
        tables=enumerate_corner_rows(edges,matrix,domains,anchors,det,adj)
        for table in tables:corner_filter(table,domains,upper)
        if any(not t['rows'] for t in tables):
            eliminated.append(gi)
            if progress:progress(gi,True)
            continue
        for table in tables:
            q=table['rectangle'];hs=domains[q]['signatures']
            used=sorted({i for row in table['rows'] for i in row[:4]});remap={}
            for i in used:
                h=tuple(hs[i][a] for a in cover['anchors'])
                if h not in indices[q]:
                    indices[q][h]=len(catalogs[q]);catalogs[q].append(list(h))
                remap[i]=indices[q][h]
                individual[q].append([gi]+list(h))
            rows[q].extend([gi]+[remap[i] for i in row[:4]]+row[4:] for row in table['rows'])
        if progress:progress(gi,False)
    return dict(cover,
                row_signature_tables=[{'rectangle':list(q),'rows':v} for q,v in individual.items()],
                corner_signature_tables=[{'rectangle':list(q),'catalog':catalogs[q],'rows':v} for q,v in rows.items()],
                coupled_corner_eliminated_indices=eliminated,
                coupled_corner_scope=__doc__)
