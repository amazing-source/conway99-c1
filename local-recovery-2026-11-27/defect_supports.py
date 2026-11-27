import sys,json,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'research-deps'))
import networkx as nx

def rank(g):
    # Rank over R of the unsigned vertex-edge incidence matrix.
    return sum(len(c)-int(nx.is_bipartite(g.subgraph(c))) for c in nx.connected_components(g))

counts=collections.Counter(); survivors=[]
for g in nx.graph_atlas_g():
    if len(g)!=7:continue
    counts['all_unlabelled_seven_vertex_graphs']+=1
    if not g.number_of_edges():continue
    if any(d==1 for _,d in g.degree()):continue
    counts['nonempty_no_degree_one']+=1
    r=rank(g)
    if any(rank(nx.restricted_view(g,[],[(u,v)]))!=r for u,v in g.edges()):continue
    counts['every_column_can_be_nonzero_in_incidence_kernel']+=1
    if list(nx.bridges(g)):
        counts['excluded_by_norm_bridge_argument']+=1
        continue
    counts['bridgeless_incidence_admissible']+=1
    survivors.append(dict(graph6=nx.to_graph6_bytes(g,header=False).decode().strip(),edges=g.number_of_edges(),kernel_dimension=g.number_of_edges()-r))
out=dict(counts=counts,survivors=survivors,scope='Necessary support conditions only; no SRG completion or exclusion of surviving supports.')
(Path(__file__).parent/'defect_supports.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(dict(counts))
print('Survivors by edge count:',dict(sorted(collections.Counter(x['edges'] for x in survivors).items())))
