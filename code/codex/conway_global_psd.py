"""Exact global PSD cuts, without a retained core or a rank hypothesis.

Let B be root incidence, M the root mate involution, and Gamma satisfy
all root counts. BB^t=11I+J-M and Gamma acts as12,-2,0 on im B^t,
with multiplicities1,6,7. On K=ker B, dim70, put T=3I-Gamma,
U=4I+Gamma. Their extensions by zero on im B^t are

  8T =24I-8Gamma-3B^tB-B^tMB+2J,
 15U =60I+15Gamma-4B^tB+B^tMB-2J.

For binary Gamma, trT=210 and tr(T^2)=1470=7trT. If both forms are
PSD, all eigenvalues theta of T are in[0,7], and their nonnegative
theta(7-theta) sum to zero. Thus T^2=7T, which gives ALL C2 equations.
Both PSD are therefore SUFFICIENT as well as necessary globally. This
uses neither a fixed core nor separate rank constraints.

Floating eigensolvers only suggest vectors. A cut is accepted after its
negative value is checked with integer arithmetic. A failed separation
does not certify PSD; the caller must retain its exact combinatorial test.
"""
from itertools import combinations
import json
from math import gcd
from pathlib import Path

import numpy as np


def bases(labels):
    assert all(len(p)==2 and p[1]!=(p[0]^1) for p in labels)
    incidence=np.array([[int(r in p) for p in labels] for r in range(14)],dtype=np.int64)
    overlap=incidence.T@incidence
    mates=incidence.T@incidence[[r^1 for r in range(14)]]
    identity=np.eye(len(labels),dtype=np.int64)
    return (24*identity-3*overlap-mates+2,
            60*identity-4*overlap+mates-2)


def canonical_cut(cut,labels):
    index={tuple(p):i for i,p in enumerate(labels)}
    form=('T','U').index(cut['form'])
    vector=[0]*len(labels)
    assert len(cut['labels'])==len(cut['weights'])
    for label,value in zip(cut['labels'],cut['weights']):
        assert isinstance(value,int)
        vector[index[tuple(label)]]+=value
    divisor=gcd(*vector)
    assert divisor
    vector=[v//divisor for v in vector]
    if next(v for v in vector if v)<0:
        vector=[-v for v in vector]
    return form,tuple(vector)


def linearize(cut,labels,graph,gram_bases=None):
    form,vector=canonical_cut(cut,labels)
    base=(gram_bases or bases(labels))[form]
    support=[i for i,v in enumerate(vector) if v]
    constant=sum(vector[i]*int(base[i,j])*vector[j] for i in support for j in support)
    scale=(-8,15)[form]
    terms={int(graph[i,j]):2*scale*vector[i]*vector[j] for i,j in combinations(support,2)}
    divisor=gcd(constant,*terms.values())
    assert divisor
    return {var:coefficient//divisor for var,coefficient in terms.items()},-constant//divisor


def load_library(path,labels):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    cuts=data.get('assembly',data).get('psd_cuts',[])
    unique={canonical_cut(cut,labels):cut for cut in cuts}
    return list(unique.values())


def integer_direction(matrix,direction):
    direction=direction/max(abs(direction))
    for exponent in range(13):
        vector=list(map(int,np.rint(direction*(2**exponent))))
        divisor=gcd(*vector)
        if not divisor:
            continue
        vector=[v//divisor for v in vector]
        value=sum(vector[i]*int(matrix[i,j])*vector[j]
                  for i in range(len(vector)) for j in range(len(vector)))
        if value>=0:
            continue
        # Only exact negative values authorize deletion of coordinates.
        improved=True
        while improved:
            improved=False
            for i,weight in enumerate(vector):
                if not weight:
                    continue
                dot=sum(int(matrix[i,j])*v for j,v in enumerate(vector))
                for replacement in (0,1 if weight>0 else -1):
                    if abs(replacement)>=abs(weight):
                        continue
                    change=replacement-weight
                    trial=value+2*change*dot+change*change*int(matrix[i,i])
                    if trial<0:
                        vector[i],value=replacement,trial
                        improved=True
                        break
        if next(v for v in vector if v)<0:
            vector=[-v for v in vector]
        assert value==sum(vector[i]*int(matrix[i,j])*vector[j]
                          for i in range(len(vector)) for j in range(len(vector)))<0
        return vector,value
    return None


def separate_psd(labels,candidate,max_per_form=12):
    cuts=[]
    for form,base,scale in zip(('T','U'),bases(labels),(-8,15)):
        matrix=base+scale*candidate
        values,vectors=np.linalg.eigh(matrix.astype(float))
        used=0
        for i,value in enumerate(values):
            if value>=-1e-8 or used>=max_per_form:
                break
            certificate=integer_direction(matrix,vectors[:,i])
            if certificate is None:
                continue
            vector,exact_value=certificate
            support=[i for i,v in enumerate(vector) if v]
            cuts.append(dict(form=form,labels=[labels[i] for i in support],
                             weights=[vector[i] for i in support],negative_value=exact_value,
                             scope='Universal global Gram PSD inequality; no retained core.'))
            used+=1
    return cuts


def fractional_center_times10(labels):
    """A C1-exact fractional center: Gamma|kerB=0, hence T=3P,U=4P.

Entries0 within each four-vertex physical-pair fibre,1/10 between fibres
sharing one physical pair,2/10 between disjoint physical-pair fibres.
This shows why integrality remains essential even with BOTH full PSD.
"""
    physical=[{r//2 for r in label} for label in labels]
    return np.array([[0 if p==q else 2-len(p&q) for q in physical] for p in physical],dtype=np.int64)
