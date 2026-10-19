"""Canonicalize one missing profile under a finite stabilizer of a 2K2 block.

These are relabellings of a fixed partial block, NOT automorphisms assumed
for a putative completed graph. Every completion has a relabelled completion
whose chosen profile is least in its stabilizer orbit. Necessary continuation
cuts remain valid for that relabelled completion too.
"""

from root_component_known_block_isomorphism import mappings, transform, check


def certificate(rows, known, outside, domains, x):
    block={'rows':rows,'known_labels':known,'outside_labels':outside}
    group=[]
    for m in mappings(known):
        if transform(rows,m)!=tuple(rows):continue
        if sorted(m['letter_permutation'][l] for l in outside[x])!=list(outside[x]):continue
        check(block,block,m);group.append(m)
    perms=[];lookup={tuple(p):i for i,p in enumerate(domains[x])}
    for m in group:
        perm=[lookup[tuple(sorted(m['known_vertex_permutation'][v] for v in p))] for p in domains[x]]
        assert sorted(perm)==list(range(len(domains[x])));perms.append(perm)
    allowed=[p for p in range(len(domains[x])) if all(p<=perm[p] for perm in perms)]
    result={'kind':'profile_minimum_under_fixed_block_stabilizer', 'outside_index':x,
            'outside_label':outside[x], 'group':group, 'profile_permutations':perms,
            'allowed_profile_indices':allowed,
            'forbidden_profile_indices':[p for p in range(len(domains[x])) if p not in allowed]}
    assert check_certificate(rows,known,outside,domains,result)
    return result


def check_certificate(rows, known, outside, domains, result):
    block={'rows':rows,'known_labels':known,'outside_labels':outside};x=result['outside_index']
    assert list(result['outside_label'])==list(outside[x])
    group=result['group'];n=len(domains[x]);lookup={tuple(p):i for i,p in enumerate(domains[x])}
    letters={tuple(m['letter_permutation']) for m in group}
    assert tuple(range(14)) in letters and len(letters)==len(group)
    for a in letters:
        for b in letters:assert tuple(a[b[l]] for l in range(14)) in letters
    observed=[]
    for m in group:
        check(block,block,m)
        assert sorted(m['letter_permutation'][l] for l in outside[x])==list(outside[x])
        perm=[lookup[tuple(sorted(m['known_vertex_permutation'][v] for v in p))] for p in domains[x]]
        assert sorted(perm)==list(range(n));observed.append(perm)
    assert observed==result['profile_permutations']
    allowed=[p for p in range(n) if all(p<=perm[p] for perm in observed)]
    assert allowed==result['allowed_profile_indices']
    assert [p for p in range(n) if p not in allowed]==result['forbidden_profile_indices']
    # Directly check that each of the original profiles has an allowed orbit
    # representative. This binds the finite reduction to the actual domains.
    assert all(any(perm[p] in allowed for perm in observed) for p in range(n))
    return True


def check_cnf_position(inp, learning, cnf, learned_clause_count):
    canon=learning.get('canonicalization')
    if canon is None:return None
    check_certificate(inp['rows'],inp['known_labels'],inp['outside_labels'],inp['domains'],canon)
    units=[[-inp['profile_literals'][canon['outside_index']][p]] for p in canon['forbidden_profile_indices']]
    end=len(cnf)-learned_clause_count
    assert cnf[end-len(units):end]==units
    return {'group_order':len(canon['group']), 'outside_label':canon['outside_label'],
            'original_profiles':len(inp['domains'][canon['outside_index']]),
            'remaining_profiles':len(canon['allowed_profile_indices']),
            'completion_preserved_up_to_explicit_block_relabelling':True}
