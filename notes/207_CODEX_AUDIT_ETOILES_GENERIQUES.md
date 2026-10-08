# 207 — Audit des étoiles génériques : témoin des apex et noyaux à sept ombres

8 octobre 2026. Sources retrouvées par LAB dans le dépôt privé
`amazing-source/conway99-structures-lab`, révision
`3e9690b73955a781e0bf64baef36e5f29ac4dc39`.

**Résultat de l'audit.** Le rapport ultérieur d'Astra contient déjà un
témoin qui réfute une obstruction fondée seulement sur les deux apex,
même renforcée de la somme entière et des inégalités d'incidence. Sa
reconstruction indépendante passe tous les contrôles annoncés. Les
exclusions de trois étoiles par sept groupes sont également reproduites
avec les bonnes inégalités de capacité. Elles restent des exclusions
de boules particulières, et non une preuve uniforme du rang 37.

## 1. Ce que signifie « 42/42 »

Les notes S24/S26 et `logs/random_balls_star_calibration.log` rapportent :

- la boule initiale d'Astra ;
- les six boules cycliques génériques de nombre d'arbres non carré
  modulo 7 parmi les cent triplets de la famille considérée ;
- 35 boules génériques admissibles de nombre d'arbres non carré,
  obtenues parmi 92 tirages.

Les 42 tests sont négatifs. Ce décompte de tests n'est ni une
classification de toutes les boules, ni un décompte certifié de classes
d'isomorphisme. L'audit présent ne relance pas les 42 recherches.

## 2. Contre-exemple à la réduction aux deux apex

Source précise : `astra/RAPPORT_ASTRA_SUIVI4_ET_AUDIT_S5.md`, message 1,
§1. Le témoin est antérieur à cet audit ; nous ne le revendiquons pas
comme une nouvelle construction.

On reconstruit la boule cyclique (2,4,1) sur trois couches de douze
points, indexés par (i,t) dans Z/6 × {0,1}. Les couplages internes ont
les décalages 0,2,4 ; les couplages A–B et A–C sont l'identité et celui
de B–C a le décalage 1. Posons

    H = 3I − G,
    H⁺ = (H+J)⁻¹ − J           sur F₇,
    K = 12I − G + 2J − G² − D,
    D = diag(J₁₂,J₁₂,J₁₂).

Le nombre d'arbres calculé en entiers est 3 096 828 960 300 ≡ 5 mod 7.
On vérifie HH⁺ = I−J, H⁺1 = 0 et la symétrie de H⁺.

Les dix supports du rapport sont enregistrés intégralement dans
`data/codex_generic_star_apex_audit.json`. Notre script indépendant
`code/codex/generic_star_apex_audit.py`, sans import du code source
d'Astra ni de celui du dépôt structures, vérifie :

- deux points non partenaires dans chaque couche ;
- Gn ≤ 2·1−n, en entiers ;
- nᵀH⁺n = 6 pour chacune des dix colonnes ;
- les produits 3 de chaque apex avec les neuf autres colonnes ;
- Σn = Ke₀ en entiers ;
- toutes les intersections de colonnes distinctes au plus 2 ;
- M★M★ᵀ ≤ K, entrée par entrée, en entiers.

Les apex sont les groupes 4 et 11. Les capacités sont
(1,1,1,0,1,1,1,1,1,0). Il reste exactement **19 paires non apex** dont
le produit de Green n'est ni 2 ni 3, notamment g(n₁,n₂)=4. Le témoin
n'est donc pas une étoile complète. Il montre exactement quelles
conditions ne peuvent pas suffire à une contradiction universelle.

Les « 18 conditions des apex » comptent deux fois leur produit mutuel :
il y a 17 paires distinctes. Sous la somme et les normes, ce produit
mutuel est même impliqué par les 16 produits avec les non-apex.

## 3. Forme précise des contraintes restantes

Supposons la somme entière Σn=Keᵤ, les dix normes 6 et deux apex a,b
de capacité zéro ayant produit 3 avec toutes les autres ombres. Pour
une ombre non apex n, l'identité de Green du dossier donne

    Σ_{m≠n} g(n,m) = 5 + (Gn)ᵤ = 5.

Après retrait des deux termes apex, les sept produits avec les autres
non-apex ont donc somme 6 modulo 7. S'ils valent tous 2 ou 3, et si d
d'entre eux valent 2, leur somme est 21−d. Avec 0≤d≤7, on obtient
d=1. Ainsi les 28 conditions binaires sur les huit non-apex imposent
automatiquement un couplage parfait 4K₂ ; il n'est pas nécessaire
d'ajouter leur égalité de capacité lorsque la somme exacte et les
conditions des apex sont déjà imposées.

Le Gram complet est 3I₁₀+3J₁₀−A_(4K₂+2K₁), de déterminant 2 dans
F₇. Le plan des apex a Gram [[6,3],[3,6]], de déterminant 6.
En posant zᵢ=nᵢ−5(a+b), les huit zᵢ sont orthogonaux aux apex et ont
le Gram prescrit

    3I₈ + J₈ − A_(4K₂),        déterminant 5 dans F₇.

Les quatre différences des paires couplées sont mutuellement
orthogonales, chacune de norme 1 pour Green. Ces identités exactes
sont également vérifiées dans le script. Elles reformulent le
problème ; leur seule dimension ne donne aucune contradiction.

## 4. Audit des sous-étoiles

`scripts/star_substars.py` utilise `full=True` même pour un sous-ensemble
de groupes. Cela exige que chaque ombre atteigne sa capacité au sein
du sous-ensemble. Une étoile complète peut au contraire apparier une
ombre choisie avec une ombre omise. Par conséquent :

- une sous-étoile faisable reste un témoin valable ;
- une sous-étoile infaisable avec cette égalité n'est pas à elle seule
  un noyau d'infaisabilité valable pour l'étoile complète ;
- pour rechercher un tel noyau, il faut garder les inégalités de
  capacité, avec `full=False`.

Les exclusions publiées à sept groupes ne souffrent pas de ce défaut.
Leurs scripts utilisent bien les inégalités. Nous les avons relancées
avec `star_shadows.py` et `full=False` :

| Boule | Groupes | Nœuds | Solution |
|---|---|---:|---|
| Astra | 1,2,3,4,5,6,8 | 27 626 | aucune |
| cyclique (2,4,1) | 1,2,3,4,5,7,11 | 39 574 | aucune |
| cyclique (2,4,3) | 1,2,3,4,5,7,9 | 41 826 | aucune |

Ces trois relances emploient le code existant, relu : ce ne sont pas
trois nouvelles implémentations indépendantes. La provenance et le
SHA-256 du script sont dans `data/codex_generic_star_core_recheck.json`.
La minimalité de ces noyaux n'est pas affirmée ici.

Le test baptisé `only_green` conserve la forme des supports, les normes,
les produits de Green et les capacités dépendant de G. Ses échecs ne
signifient donc pas qu'un Gram abstrait de rang dix soit impossible.
L'estimation heuristique de 10⁻¹⁵ solutions dans les logs n'est pas
une preuve de l'origine, ni de l'uniformité, de l'obstruction.

## 5. Où un filtre d'échange peut réellement agir

LAP propose d'exploiter les restrictions sur les petits échanges de
colonnes de N. Dans une seule étoile centrée en u∈A, les projections
sur A sont eᵤ+eᵥ, pour dix v distincts. Chaque v est une coordonnée
pivot unique. Les dix colonnes sont donc déjà indépendantes sur tout
corps, et aucune égalité entre deux sous-familles distinctes n'est
possible en entiers. Ce filtre est automatiquement satisfait ici.

Son domaine utile est le couplage de plusieurs étoiles, où cette
indépendance par coordonnées pivots disparaît. La preuve uniforme
recherchée doit encore contrôler les interactions entre ombres ; les
résultats finis et le témoin ci-dessus délimitent ce travail.

Validation autonome du témoin et des identités de Gram :

    python code/codex/generic_star_apex_audit.py --verify-only
