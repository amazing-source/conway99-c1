"""Exclude every three-edge rectangle based at ANY point of the root line.

For a same-colour matching edge u-v in a coloured component of N(L),
take its four neighbours in the other two colours. They are the four
rectangle corners at that point of L, between L and the line through u-v.
Exactly three induced edges violate the universal no-P4 rectangle theorem.
This is a necessary local filter, independent of the Gram and prism budget.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process,atomic_json_write


def matching_maps(record):
    n=len(record['cross_permutations'][0])
    maps=[]
    for matching in record['internal_matchings']:
        row=[None]*n
        for a,b in matching:row[a]=b;row[b]=a
        assert all(v is not None for v in row)
        maps.append(row)
    return maps


def obstruction(record,code,maps=None):
    maps=maps if maps is not None else matching_maps(record)
    pi,ai,bi=code;p=record['cross_permutations'][pi];n=len(p)
    a,b=maps[ai],maps[bi];inverse=[None]*n
    for i,j in enumerate(p):inverse[j]=i
    # Colour0--colour1 and colour0--colour2 are identity matchings;
    # colour1--colour2 is p. Internal colour0 mates are i^1.
    for i in range(0,n,2):
        j=i^1
        e=int(a[i]==j)+int(b[i]==j)+int(p[i] in (i,j))+int(p[j] in (i,j))
        if e==3:return {'colour':0,'matching_edge':[i,j],'corners':[n+i,n+j,2*n+i,2*n+j],'edges':e}
    for i,j in enumerate(a):
        if i>=j:continue
        x,y=p[i],p[j]
        e=int(j==(i^1))+int(b[x]==y)+int(x in (i,j))+int(y in (i,j))
        if e==3:return {'colour':1,'matching_edge':[n+i,n+j],'corners':[i,j,2*n+x,2*n+y],'edges':e}
    for i,j in enumerate(b):
        if i>=j:continue
        x,y=inverse[i],inverse[j]
        e=int(j==(i^1))+int(a[x]==y)+int(x in (i,j))+int(y in (i,j))
        if e==3:return {'colour':2,'matching_edge':[2*n+i,2*n+j],'corners':[i,j,n+x,n+y],'edges':e}
    return None


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--certificate',type=Path,required=True)
    args=parser.parse_args();resources=limit_research_process(1)
    raw=args.source.read_bytes();data=json.loads(raw);certificates=[]
    for record in data['records']:
        maps=matching_maps(record);kept=[];rejected=[];patterns=set();hist=Counter()
        for code in record['component_code_triples']:
            witness=obstruction(record,code,maps)
            if witness is not None:rejected.append({'code':code,**witness});continue
            kept.append(code);pi,ai,bi=code;p=record['cross_permutations'][pi];a,b=maps[ai],maps[bi]
            hist[sum(i==j for i,j in enumerate(p))]+=1
            row=[]
            for i in range(0,len(p),2):
                j=i^1
                bits=[int(a[i]==j),int(p[i]==i),int(p[i]==j),int(p[j]==i),int(p[j]==j),int(b[i]==j)]
                row.append(sum(bit<<k for k,bit in enumerate(bits)))
            patterns.add(tuple(row))
        record['all_colour_E3_filter']={'before':len(record['component_code_triples']),'after':len(kept),
                                        'removed':len(rejected),'scope':__doc__}
        record['component_code_triples']=kept
        record['internal_rectangle_patterns']=[list(row) for row in sorted(patterns)]
        record['projected_pattern_count']=len(patterns)
        record['triangle_histogram']={str(k):v for k,v in sorted(hist.items())}
        record.pop('witnesses',None)
        certificates.append({'vertices':record['vertices'],'rejected_codes':rejected,
                             'kept_codes':len(kept),'colour_histogram':dict(Counter(r['colour'] for r in rejected))})
        print(json.dumps({'vertices':record['vertices'],'before':len(kept)+len(rejected),'after':len(kept),'removed':len(rejected)}),flush=True)
    provenance={'source':args.source.as_posix(),'source_sha256_lf':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),
                'scope':__doc__}
    data['all_colour_E3_filter_source']=provenance
    atomic_json_write(args.output,data)
    atomic_json_write(args.certificate,dict(provenance,resources=resources,records=certificates))


if __name__=='__main__':main()
