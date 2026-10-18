"""Transport frozen Gram invariants without choosing a root relabelling.

The21 rectangle vectors are permuted when the seven lines are relabelled.
For their Gram R, sort the21 integers 2048*R_ii+sum_j R_ij^2. All entries
have absolute value<=8, so each row-square sum is<=1344 and this encoding
is injective on (diagonal,row-square sum). The sorted profile is a necessary
invariant of any of the still-open Grams in the frozen complete cover.

Apply this table only at another root whose own prism sum is<=51. The
profile is weaker than a full Gram isomorphism test; no omitted labels or
specific completion are fixed, and roots above51 remain unrestricted.
"""
import argparse
from collections import defaultdict
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def freeze(source,output,frontier):
    import sympy as sp
    assert not output.exists(), 'Frozen Gram invariants are immutable.'
    raw=source.read_bytes();data=json.loads(raw);profiles=defaultdict(list)
    frontier_raw=frontier.read_bytes();frontier_data=json.loads(frontier_raw)
    assert frontier_data['allowed_template_indices']==[7,9,19]
    for record in data['records']:
        ti=record['template_index']
        if ti not in (7,9,19):continue
        assert record['exhaustive'] and record['usable_as_gram_cover']
        lift=sp.Matrix([[sp.Rational(*x) for x in row] for row in record['lift_matrix']])
        for gi,values in zip(record['source_gram_indices'],record['gram_anchor_values']):
            small=sp.zeros(lift.cols)
            for (a,b),v in zip(record['anchor_pairs'],values):small[a,b]=small[b,a]=v
            r=lift*small*lift.T;assert all(v.q==1 and abs(v)<=8 for v in r)
            assert all(r[i,i] in (4,6,8) for i in range(r.rows))
            profile=[0]*(21-r.rows)+[2048*int(r[i,i])+sum(int(r[i,j])**2 for j in range(r.cols)) for i in range(r.rows)]
            profiles[tuple(sorted(profile))].append([ti,gi])
    result={'scope':__doc__,'source':source.as_posix(),
        'source_sha256_lf':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),
        'template_frontier':frontier.as_posix(),
        'template_frontier_sha256_lf':hashlib.sha256(frontier_raw.replace(b'\r\n',b'\n')).hexdigest(),
        'allowed_template_indices':frontier_data['allowed_template_indices'],
        'budget_threshold':51,'diagonal_radix':2048,
        'source_gram_count':sum(map(len,profiles.values())),
        'records':[{'profile':list(k),'source_grams':v} for k,v in sorted(profiles.items())]}
    atomic_json_write(output,result);return result


def add_profile_cuts(model,rectangles,profiles):
    assert profiles['diagonal_radix']==2048 and profiles['budget_threshold']==51
    groups={}
    for item in rectangles:groups.setdefault(item['root'],[]).append(item)
    records=[];allowed=[r['profile'] for r in profiles['records']]
    for root,items in sorted(groups.items()):
        first=items[0]
        assert len(items)==15 and 'low_budget_flag' in first and 'residual_gram_entries' in first
        lines=sorted(tuple(line) for line in first['all_lines']);diagonals={}
        for item in items:
            a,b=sorted((lines.index(tuple(item['base_vertices'][:2])),lines.index(tuple(item['base_vertices'][2:]))))
            diagonals[a+1,b+1]=8-2*sum(item['edges'])
        for item in first['old_root_rectangles']:
            diagonals[0,lines.index(tuple(item['line']))+1]=8-2*item['edge_count']
        pairs=sorted(diagonals);assert len(pairs)==21
        entries=first['residual_gram_entries'];assert len(entries)==210
        squares={}
        for (a,b),value in entries.items():
            s=model.new_int_var(0,64,f'rotated_profile_offsquare_{root}_{a}_{b}')
            model.add_allowed_assignments([value,s],[(v,v*v) for v in range(-8,5)])
            squares[a,b]=s
        encoded=[]
        for i,pair in enumerate(pairs):
            d=model.new_int_var(0,8,f'rotated_profile_diagonal_{root}_{i}')
            model.add(d==diagonals[pair])
            ds=model.new_int_var(0,64,f'rotated_profile_diagonal_square_{root}_{i}')
            model.add_allowed_assignments([d,ds],[(v,v*v) for v in (0,4,6,8)])
            row_norm=ds+sum(s for (a,b),s in squares.items() if pair in (a,b))
            key=model.new_int_var(0,17728,f'rotated_profile_key_{root}_{i}')
            model.add(key==2048*d+row_norm);encoded.append(key)
        # An insertion sorting network; no ordering restriction on the graph.
        ordered=[];comparators=0
        for value in encoded:
            ordered.append(value)
            for j in range(len(ordered)-1,0,-1):
                lo=model.new_int_var(0,17728,f'rotated_profile_min_{root}_{comparators}')
                hi=model.new_int_var(0,17728,f'rotated_profile_max_{root}_{comparators}')
                model.add_min_equality(lo,ordered[j-1:j+1]);model.add_max_equality(hi,ordered[j-1:j+1])
                ordered[j-1],ordered[j]=lo,hi;comparators+=1
        model.add_allowed_assignments(ordered,allowed).only_enforce_if(first['low_budget_flag'])
        records.append({'root':root,'allowed_profiles':len(allowed),'source_grams':profiles['source_gram_count'],
                        'sorting_comparators':comparators,'unconditional_new_root_budget':None})
    return {'roots':records,'scope':__doc__}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('--freeze',type=Path,required=True)
    p.add_argument('--frontier',type=Path,required=True)
    args=p.parse_args();limit_research_process(1);result=freeze(args.source,args.freeze,args.frontier)
    print(json.dumps({'source_grams':result['source_gram_count'],'invariant_profiles':len(result['records'])}))


if __name__=='__main__':main()
