"""Necessary six-pair exact cover for a unique K3 triplet completion.

Pair the two T vertices with the same letter off root 3. Each pair
must use two distinct S vertices and two distinct Y triples, obey
its shared-letter quota and the common-neighbour bound. Forgetting
the root-3 bit orientation gives a six-group exact-cover relaxation.
An exhaustive negative result includes a small branch DAG, checked
without another search. SAT here is only a necessary condition.
"""

from functools import lru_cache
from itertools import product


def option_groups(data):
    mask=int(data['allowed_triplets'],16)
    if mask.bit_count()!=12:return None
    triples=[(t//16+12,t//4%4+16,t%4+20) for t in range(64) if mask&(1<<t)]
    index={t:i for i,t in enumerate(triples)};domains=data['domains'][36:48];groups=[]
    for letter in range(6):
        options=set()
        for a,b in product(domains[2*letter],domains[2*letter+1]):
            if a[0]==b[0] or tuple(a[1:])==tuple(b[1:]):continue
            if len(set(a)&set(b))>1:continue
            if any(int(v in a)+int(v in b)>data['letter_deficits'][v][letter]
                   for v in set(a)|set(b)):continue
            options.add((1<<a[0])|(1<<b[0])|(1<<(12+index[tuple(a[1:])]))|
                        (1<<(12+index[tuple(b[1:])])))
        groups.append(tuple(sorted(options)))
    return groups


def check_cover_dag(groups,proof):
    all_slots=(1<<24)-1;checked=set()
    def check(remaining,used):
        key=f'{remaining:x}/{used:x}'
        if key in checked:return
        assert remaining and key in proof
        node=proof[key]
        viable={g:[m for m in groups[g] if not m&used]
                for g in range(6) if remaining&(1<<g)}
        if 'uncoverable_slots' in node:
            union=used
            for row in viable.values():
                for mask in row:union|=mask
            assert union!=all_slots and int(node['uncoverable_slots'],16)==all_slots^union
        else:
            group=node['group'];assert group in viable
            children=node['children']
            assert [int(c['option'],16) for c in children]==viable[group]
            for child in children:
                mask=int(child['option'],16);nxt=remaining^(1<<group);covered=used|mask
                assert child['child']==f'{nxt:x}/{covered:x}'
                check(nxt,covered)
        checked.add(key)
    check(63,0)
    return {'checked_states':len(checked),'root_refuted':True}


def pair_cover(data,node_budget=200000):
    groups=option_groups(data)
    if groups is None:return {'status':'NOT_APPLICABLE_MULTIPLE_TRIPLET_DESIGNS'}
    all_slots=(1<<24)-1;proof={};calls=0
    @lru_cache(None)
    def search(remaining,used):
        nonlocal calls
        calls+=1
        if calls>node_budget:raise TimeoutError
        if not remaining:
            assert used==all_slots
            return ()
        key=f'{remaining:x}/{used:x}'
        viable={g:[m for m in groups[g] if not m&used] for g in range(6) if remaining&(1<<g)}
        union=used
        for row in viable.values():
            for mask in row:union|=mask
        if union!=all_slots:
            proof[key]={'uncoverable_slots':hex(all_slots^union)};return None
        group=min(viable,key=lambda g:len(viable[g]));children=[]
        for mask in viable[group]:
            nxt=remaining^(1<<group);covered=used|mask;result=search(nxt,covered)
            if result is not None:return ((group,mask),)+result
            children.append({'option':hex(mask),'child':f'{nxt:x}/{covered:x}'})
        proof[key]={'group':group,'children':children};return None
    out={'group_sizes':list(map(len,groups)),'option_masks':[[hex(m) for m in row] for row in groups]}
    try:
        answer=search(63,0)
    except TimeoutError:
        return {**out,'status':'UNKNOWN_T_PAIR_COVER','nodes':calls}
    if answer is not None:
        return {**out,'status':'PASSES_T_PAIR_COVER','nodes':calls,
                'choices':[{'group':g,'option':hex(m)} for g,m in answer]}
    return {**out,'status':'EXCLUDED_T_PAIR_COVER','nodes':calls,'proof_dag':proof,
            'proof_check':check_cover_dag(groups,proof)}
