"""New mass-eight class bound using LAB's no-twin-mills lemma (bridge 433).

Reuses the pair costs of note 226. No local enumeration is repeated.
The linear C8 bound assumes P=0 to remove the C14 support family.
"""
from fractions import Fraction as F
from itertools import product
import json

from higher_census_minima import ROOT


def main():
    source=json.loads((ROOT/'data/codex_small_collision_new_channels.json').read_text())
    costs={}
    for row in source['mass8_pair_bounds']:
        key=tuple(sorted((str(row['left']),str(row['right']))))
        costs[key]=max(costs.get(key,F(0)),F(row['total_bound']))
    cubic=['2022000','5683824','5691760']
    coefficients=dict(zip(cubic,(872,816,2840)))
    classes=[]
    for n in product(range(5),repeat=3):
        for mill in (0,1):
            # The common exterior has >=61 vertices: total support <=38.
            if sum(n)+mill<2 or 8*sum(n)+7*mill>38: continue
            cost=sum(F(n[i]*(n[i]-1),2)*costs[(code,code)]
                     for i,code in enumerate(cubic))
            cost+=sum(n[i]*n[j]*costs[tuple(sorted((cubic[i],cubic[j])))]
                      for i in range(3) for j in range(i+1,3))
            cost+=mill*sum(n[i]*costs[tuple(sorted((code,'weighted_mill')))]
                           for i,code in enumerate(cubic))
            linear=sum(n[i]*coefficients[code] for i,code in enumerate(cubic))
            assert linear>=cost
            classes.append({'cubic_counts':n,'mills':mill,'pair_cost_bound':str(cost),
                            'linear_bound':linear,'slack':str(linear-cost)})
    thirteen=['127305925','128354469','245715219']
    for code in thirteen:
        coefficients[code]=int(2*costs[(code,code)])
    inequalities=[]
    for i,a in enumerate(thirteen):
        for b in thirteen[i:]:
            lhs=coefficients[a]+coefficients[b]
            rhs=4*costs[tuple(sorted((a,b)))]
            assert lhs>=rhs
            inequalities.append({'types':[a,b],'coefficient_sum':lhs,
                                 'four_times_pair_bound':str(rhs)})
    report={'scope':__doc__,'new_lemma_source':'LAB bridge message 433',
            'max_mills_per_projection_class':1,
            'max_cubic_mill_class_size':4,
            'mass8_linear_coefficients':coefficients,'constant':0,
            'cubic_mill_class_compositions':classes,
            'thirteen_edge_pair_inequalities':inequalities,
            'scope_limit':'No new SRG or rank exclusion; masses seven and nine remain unchanged.'}
    (ROOT/'data/codex_mass8_no_twin_mills.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'coefficients':coefficients,'constant':0,'class_compositions':len(classes),
                      'tight_classes':[r for r in classes if r['slack']=='0']}))


if __name__=='__main__':main()
