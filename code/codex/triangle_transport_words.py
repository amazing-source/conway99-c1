"""An explicit transition-system description of rooted lambda=1,mu=2 SRGs.

For a root x, put S=N(x), with its perfect matching P. Each far vertex is
uniquely labelled by a nonmatched pair {a,b} of S: a,b have exactly two
common neighbors, x and this vertex. Thus far vertices are the edges of
H=K_|S| minus P. Triangles through a in S pair the H-edges incident with a.
The transport cycles are precisely the circuits of this transition system.

Label each transport edge yz by the common star neighbor a completing its
triangle. Consecutive letters of a circuit word give the labels of its far
vertices. Rooted skeleton automorphisms are EXACTLY the permutations of S
preserving P and this unoriented collection of circuit words. This is a
description of the new skeleton, not a recomputation of full SRG groups.

If one circuit has a unique length L and uses every letter of S, any rooted
skeleton automorphism is determined by one of its 2L dihedral alignments.
Checking consistency of repeated letters, then P, then all circuit words
gives a finite certificate with at most 2L candidates, without a group solver.
The same certificate also applies to the explicitly partial local examples.
"""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/codex_asymmetry_mechanisms_20261014'
spec=importlib.util.spec_from_file_location('transport',Path(__file__).with_name('asymmetry_triangle_transport.py'))
tr=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tr)


def circuit_words(adj,third,x):
    h=tr.transport(adj,third,x,2)
    remaining=set(h); words=[]
    while remaining:
        start=min(remaining); u=start; previous=None; word=[]; vertices=[]
        while True:
            vertices.append(u); remaining.remove(u)
            choices=h[u]-({previous} if previous is not None else set())
            v=min(choices)
            word.append(third[u,v])
            previous,u=u,v
            if u==start:break
        assert len(word)>=4 and len(word)==len(vertices)
        words.append(tuple(word))
    # Consecutive letters encode every edge of K_|S| minus P once.
    pairs=Counter(tuple(sorted((w[i-1],w[i]))) for w in words for i in range(len(w)))
    S=adj[x]
    expected={(a,b) for a in S for b in S if a<b and b not in adj[a]}
    assert set(pairs)==expected and set(pairs.values())=={1}
    return sorted(words,key=lambda w:(len(w),w))


def unoriented(word):
    word=tuple(word); reverse=word[::-1]
    return min(v[i:]+v[:i] for v in (word,reverse) for i in range(len(v)))


def cycle_incidence_colors(S,mate,words):
    lengths=sorted({len(w) for w in words})
    counts={L:Counter(a for w in words if len(w)==L for a in w) for L in lengths}
    signatures={a:tuple(counts[L][a] for L in lengths) for a in S}
    def compress(d):
        ids={s:i for i,s in enumerate(sorted(set(d.values())))}
        return {a:ids[s] for a,s in d.items()}
    colors=compress(signatures); rounds=[len(set(colors.values()))]
    # Matched partners are intrinsic to the rooted star.
    while True:
        new=compress({a:(colors[a],colors[mate[a]]) for a in S})
        if len(set(new.values()))==len(set(colors.values())):break
        colors=new;rounds.append(len(set(colors.values())))
    return {'lengths':lengths,'signatures':{str(a):signatures[a] for a in sorted(S)},
            'color_class_counts':rounds,'class_sizes':sorted(Counter(colors.values()).values()),
            'all_star_vertices_distinguished':len(set(colors.values()))==len(S)}


def study(name,path,x=0,partial=False):
    start=time.monotonic(); adj=tr.read_graph(path);third=tr.triangle_table(adj)
    S=adj[x]; mate={a:next(iter(adj[a]&S)) for a in S}
    words=circuit_words(adj,third,x)
    size_counts=Counter(map(len,words))
    anchors=[w for w in words if size_counts[len(w)]==1 and set(w)==S]
    result={'name':name,'source':str(path.relative_to(ROOT)),'root':x,
            'partial_graph_only':partial,'n':len(adj),'k':len(S),
            'star_matching':sorted((a,b) for a,b in mate.items() if a<b),
            'cycle_lengths':list(map(len,words)),
            'cycle_words':words,
            'cycle_incidence_colors':cycle_incidence_colors(S,mate,words),
            'unique_length_spanning_cycles':list(map(len,anchors)),
            'full_graph_group_not_recomputed':True}
    if anchors:
        anchor=min(anchors,key=len); L=len(anchor)
        canonical=sorted(unoriented(w) for w in words)
        stages=Counter(); accepted=[]; rejection_counts=Counter(); witnesses=[]
        for direction in [1,-1]:
            for shift in range(L):
                stages['dihedral_alignments']+=1
                perm={}; first_occurrence={}; consistent=True
                for i,a in enumerate(anchor):
                    b=anchor[(shift+direction*i)%L]
                    if a in perm and perm[a]!=b:
                        j=first_occurrence[a]
                        witnesses.append({'direction':direction,'shift':shift,
                                          'equal_letter_positions':[j,i],
                                          'unequal_image_positions':[(shift+direction*j)%L,(shift+direction*i)%L]})
                        consistent=False;break
                    perm[a]=b
                    first_occurrence.setdefault(a,i)
                if not consistent or len(set(perm.values()))!=len(S):
                    rejection_counts['repeated_letters']+=1;continue
                stages['letter_permutations']+=1
                if any(perm[mate[a]]!=mate[perm[a]] for a in S):
                    rejection_counts['star_matching']+=1;continue
                stages['preserve_star_matching']+=1
                if sorted(unoriented(tuple(perm[a] for a in w)) for w in words)!=canonical:
                    rejection_counts['other_circuits']+=1;continue
                stages['preserve_all_circuits']+=1
                accepted.append({'direction':direction,'shift':shift,
                                 'permutation':{str(a):perm[a] for a in sorted(S)}})
        # Each pair of consecutive colors occurs only once, so different
        # alignments cannot yield the same permutation.
        assert len({tuple(item['permutation'].values()) for item in accepted})==len(accepted)
        result['dihedral_certificate']={'anchor_length':L,'anchor_word':anchor,
                'stage_counts':dict(stages),'rejection_counts':dict(rejection_counts),
                'rooted_skeleton_order':len(accepted),'automorphisms':accepted,
                'repeated_letter_rejection_witnesses':witnesses,
                'single_circuit_and_matching_rigid':stages['preserve_star_matching']==1}
    result['seconds']=time.monotonic()-start
    (OUT/(name+'_words.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['name','root','cycle_lengths','unique_length_spanning_cycles','seconds']}),flush=True)
    cert=result.get('dihedral_certificate',{})
    print(json.dumps({'name':name,'incidence_class_sizes':result['cycle_incidence_colors']['class_sizes'],
                     'certificate':{k:cert[k] for k in ['anchor_length','stage_counts','rejection_counts','rooted_skeleton_order'] if k in cert}}),flush=True)
    return result


def main():
    lab=ROOT/'data/codex_asymmetry_synthesis_20261014/lab_sources'
    cases=[('gamma6',lab/'new243_trade_aut108.edges',0,False),
           ('gamma8',lab/'new243_trade_aut108_b.edges',0,False),
           ('local99_odd',OUT/'local_t7_s1401_5.edges',0,True)]
    for args in cases:study(*args)


if __name__=='__main__':main()
