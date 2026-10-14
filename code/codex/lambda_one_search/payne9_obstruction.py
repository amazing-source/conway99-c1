"""Exact obstruction to the attempted GF9 Payne 3-ovoid construction.

Let M be the 891 by 729 point-line incidence matrix. Binary elimination
gives rank 441. The 288 kernel basis vectors have weight divisible by four
and even pairwise intersections. Therefore ker_F2(M) is doubly even:
wt(x+y) = wt(x)+wt(y)-2*|supp(x) intersect supp(y)|.

A 3-ovoid would have 243 points by incidence counting (891*3/11).
Its complement would meet every 9-point line in 6 points, so its indicator
would lie in this kernel, with weight 729-243=486, not divisible by four.
Contradiction. This excludes all 3-ovoids of THIS constructed quadrangle,
before imposing mu or asymmetry. It does not exclude arbitrary SRG243,
other generalized quadrangles, or asymmetric lambda-one SRGs in general.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))


def binary_kernel_certificate(lines,n=729):
    rows=[sum(1<<v for v in L) for L in lines]
    pivots={}
    for original in rows:
        x=original
        while x:
            j=x.bit_length()-1
            if j not in pivots:
                pivots[j]=x
                break
            x^=pivots[j]
    free=sorted(set(range(n))-set(pivots))
    basis=[]
    for j in free:
        x=1<<j
        for k,row in sorted(pivots.items()):
            if (x&row).bit_count()%2:
                x|=1<<k
        assert all((x&row).bit_count()%2==0 for row in rows)
        assert all(bool(x&(1<<k))==(j==k) for k in free)
        basis.append(x)
    weights=[x.bit_count() for x in basis]
    odd_pairs=sum((x&y).bit_count()%2 for i,x in enumerate(basis) for y in basis[i+1:])
    return {'binary_rank':len(pivots),'kernel_dimension':len(basis),
            'independence_verified_on_free_coordinates':True,
            'kernel_membership_verified':True,
            'basis_weight_residues_mod4':{str(w):sum(k%4==w for k in weights) for w in range(4)},
            'odd_pairwise_intersections':odd_pairs,
            'doubly_even':all(w%4==0 for w in weights) and odd_pairs==0,
            'free_coordinates':free,'kernel_basis_hex':[hex(x) for x in basis]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    from payne9_construct import geometry
    _,_,_,lines,_=geometry()
    result=binary_kernel_certificate(lines)
    assert result['binary_rank']==441 and result['kernel_dimension']==288
    assert result['doubly_even']
    result.update(status='proven_no_3_ovoid_in_this_GQ',
                  selected_size=243,complement_size=486,required_weight_modulus=4,
                  complement_weight_residue=486%4,
                  incidence_sha256=hashlib.sha256(json.dumps(lines,separators=(',',':')).encode()).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  scope='This explicit Payne-derived GF9 quadrangle only; no general SRG nonexistence claim')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['free_coordinates','kernel_basis_hex']}))


if __name__=='__main__':main()
