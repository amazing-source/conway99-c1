# 234 — Connexité des murs opposés d'un quadrilatère

9 octobre 2026. Réduction sans hypothèse de rang, de généricité ou de
symétrie. Point de départ : les 44 voisins extérieurs d'un quadrilatère
(note 172, §1.1), remis en avant par LAB au message 460. La preuve
ci-dessous utilise seulement des comptages entiers.

**Théorème.** Dans un SRG(99,14,1,2), fixer un quadrilatère induit
`q0 q1 q2 q3`. Noter `Wi` les dix sommets dont le seul voisin dans
le quadrilatère est `qi`. Les deux graphes induits sur
`W0 ∪ W2` et sur `W1 ∪ W3` sont connexes.

Ce résultat exclut les structures de murs déconnectées. Il ne constitue
pas une exclusion du rang 37, d'un autre rang, ou de C1. Aucune
énumération des structures connexes n'est revendiquée.

## 1. Structure exacte des 44 voisins

Soit `zi` le troisième point du triangle contenant l'arête `qi q(i+1)`
(indices modulo quatre). Les quatre `zi` sont distincts. Les autres
voisins extérieurs sont les quatre ensembles `Wi`, chacun de taille dix.
Écrire `S = W0 ∪ W1 ∪ W2 ∪ W3 ∪ Z`, avec `Z={z0,z1,z2,z3}`.

Soient `T` l'adjacence du quadrilatère, `B` son incidence vers `S`, et
`C` l'adjacence sur `S`. L'identité du SRG donne exactement

    BC = 2J − (I+T)B.

Chaque `Wi` induit cinq arêtes disjointes : dans le voisinage de `qi`,
les deux autres voisins du quadrilatère ont déjà pour partenaires les
deux points spéciaux incidents à `qi`. Il reste dix points appariés.

Un point spécial n'a aucun voisin dans les deux murs de ses extrémités.
Entre points spéciaux, seules les deux arêtes `z0 z2`, `z1 z3` sont
possibles. Noter `t ∈ {0,1,2}` leur nombre. Un spécial appartenant à
l'une de ces arêtes n'a aucun voisin simple dans `S`. Un spécial non
apparié a exactement un voisin dans chacun des deux murs qui ne sont
pas ceux de ses extrémités.

Pour `x ∈ Wi`, poser `e_x=|N(x)∩Z|`. Alors

    degré dans les 40 sommets simples = 5−2e_x,
    degré dans S = 5−e_x,
    |N(x)∩W(i+2)| = 2−e_x,
    somme_{x∈Wi} e_x = 2−t.

En particulier, le graphe sur les 40 simples n'est 5-régulier que
pour `t=2`. Chacun des deux murs consécutifs fournit normalement un
voisin simple ; chaque spécial adjacent en consomme exactement un.
Le nombre de voisins simples de `x` dans l'autre couple de murs est
donc `2−e_x`.

## 2. Tailles et déficits des composantes

Considérer `P = Γ[W0 ∪ W2]` et l'une de ses composantes `K`. Poser

    a=|K∩W0|,  b=|K∩W2|,  h=a+b,
    δ0=Σ_{K∩W0}e_x,  δ2=Σ_{K∩W2}e_x,  δ=δ0+δ2.

Les partenaires d'un même mur appartiennent à la même composante, donc
`a,b` sont pairs. Le comptage des arêtes entre les deux murs donne

    2a−δ0 = 2b−δ2.

Or `0≤δi≤2−t≤2`. Si `a≠b`, la parité impose `|2(a−b)|≥4`,
impossible. Ainsi `a=b` est pair, `h` est un multiple de quatre,
`δ0=δ2`, et `δ` vaut zéro, deux ou quatre. Sur toutes les composantes,

    Σ δ = 4−2t ≤ 4.

Une composante de taille quatre a deux partenaires dans chaque mur.
Aucun sommet ne peut être adjacent aux deux partenaires de l'autre
mur : leur arête aurait alors deux voisins communs, ce sommet et le
coin du quadrilatère. Le degré entre murs est donc au plus un et
`δ≥4`.

## 3. Deux identités entières pour tout sous-ensemble

Pour un ensemble `H` de `n` sommets, écrire `k_u` ses degrés internes,
`s1=Σ_H k_u`, `s2=Σ_H k_u²`, et `d_v=|N(v)∩H|` à l'extérieur.
L'identité `A²+A=12I+2J` donne

    Σ_ext d_v = 14n−s1,
    Σ_ext d_v² = 12n+2n²−s1−s2.

Pour tout entier `d`, les deux polynômes

    (d−1)(d−2),       (d−2)(d−3)

sont non négatifs. On utilisera leurs sommes, parfois en isolant
des sommets extérieurs dont le profil est déjà connu.

## 4. Composantes cubiques de tailles 8, 12 ou 16 interdites

Supposer `δ=0`, et prendre `H=K∪{q0,q2}`. Les `h` points de `K`
ont degré interne quatre ; les deux coins ont degré `h/2`. Donc

    n=h+2,  s1=5h,  s2=16h+h²/2,
    Σ_ext d_v = 9h+28,
    Σ_ext d_v² = 3h²/2−h+32,
    |extérieur| = 97−h.

Il suit que

    Σ_ext (d_v−1)(d_v−2) = 3h²/2−30h+142.

Pour `h=8` et pour `h=12`, le membre droit vaut **−2** : contradiction.

Pour `h=16`, utiliser plutôt

    Σ_ext (d_v−2)(d_v−3) = 26.

Les quatre simples de `(W0∪W2)\K` ont exactement un voisin dans `H` :
leur coin, puisqu'aucune arête de `P` ne rejoint une autre composante.
Les quatre spéciaux ont aussi exactement un voisin dans `H` : un
coin, puisque `δ=0`. Ces huit sommets contribuent donc **16**.

Les vingt simples de `W1∪W3` ont des degrés vers `H` dans `{0,1,2}`,
de somme `2h=32`. Si `n_j` est leur effectif de degré `j`, alors

    n0+n1+n2=20,  n1+2n2=32,  n1+2n0=8.

Leur contribution vaut `6n0+2n1=16+2n0≥16`. La somme totale serait
au moins **32**, alors qu'elle doit valoir 26. Contradiction.

## 5. Taille 8 et déficit 2 interdits

Supposer `h=8`, `δ=2`. Chaque mur de la composante a un déficit un,
donc exactement un sommet avec `e_x=1`; tous les autres ont `e_x=0`.
Dans `H=K∪{q0,q2}`, les degrés internes sont huit fois quatre et
deux fois trois. Les identités précédentes deviennent

    n=10,  s1=38,  s2=146,
    Σ_ext d_v=102,  Σ_ext d_v²=136,
    Σ_ext (d_v−1)(d_v−2)=136−3·102+2·89=8.

Les vingt simples de l'autre couple de murs n'ont, au total, que
`2h−δ=14` incidences vers `H`. Au moins six d'entre eux ont donc
degré zéro. Leur seule contribution à cette dernière somme est au
moins **12**, contradiction.

## 6. Connexité

Les tailles des composantes de `P` forment une partition de vingt
en multiples de quatre, et la somme de leurs déficits est au plus quatre.

- S'il existe une composante de taille quatre, elle consomme tout le
  déficit disponible. Les autres composantes sont cubiques, de tailles
  strictement inférieures à vingt : quatre est impossible par le §2,
  et huit, douze, seize sont exclus par le §4.
- Sinon, la seule partition non triviale est `8+12`. La composante
  de taille huit n'a déficit ni zéro (§4), ni deux (§5). Elle consomme
  donc tout le déficit quatre, laissant une composante cubique de
  taille douze, exclue au §4.

Ainsi `P` est connexe. Le même raisonnement vaut pour `W1∪W3`.

## 7. Portée pour la recherche

Une recherche par quadrilatère peut désormais imposer deux graphes
connexes sur vingt sommets, chacun formé des partenaires dans les murs
et des arêtes entre murs opposés. Leurs déficits totaux sont respectivement
`4,2,0` pour `t=0,1,2`. Leur classification et leur couplage demeurent
ouverts. Ce théorème n'affirme ni que le bloc de 44 sommets est
inversible, ni que ses structures connexes sont impossibles.
