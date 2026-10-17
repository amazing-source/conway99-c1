# 185 — Famille (4,4) : première borne complète après collisions

8 octobre 2026. Cette note complète les masses six et sept laissées ouvertes
dans la note 183. Elle fournit une soustraction sûre de toutes les collisions
de la famille `(4,4)` avec elle-même et avec les anciennes familles de norme huit.
La majoration des pertes est volontairement non optimale : son ajout ne relève
pas encore le minimum uniforme 3371634 obtenu dans la note 182.

Notations : P,ρ,τ,H,Ω sont celles des notes 179–183. C_c désigne le nombre de
copies du type à huit sommets de code c. Posons C14=C_127242964.

## 1. Réduction exhaustive

Un nouveau représentant est ψ=1_W−1_Y avec |W|=|Y|=4, e(W)=e(Y)=4 et W,Y
anticomplets. Sa somme est zéro. Les anciennes familles de sommes ±3 et ±6
sont séparées par la congruence modulo neuf de la somme des représentants.
Les seules anciennes familles à examiner sont donc les familles équilibrées :

- `(1,1)` : différence de deux points adjacents ;
- `(2,2)` : différence de deux arêtes anticomplètes ;
- `(3,3)` : triangle moins chemin de longueur deux, anticomplets, ou deux triangles
  reliés par une seule arête.

La masse positive d'une différence nouvelle–ancienne est au plus 5,6,7,
respectivement. Il n'y a pas de collision de masse au plus cinq. Les différences
de masses six et sept sont binaires : les croisements de signes, qui produiraient
une coordonnée deux, sont exclus par S≥4h. Elles sont donc données par deux
prismes jumeaux, ou deux copies de D de même projection.

Entre nouveaux représentants, les masses six et sept correspondent respectivement
à deux ou un points communs de même signe. La masse huit est intégralement traitée
dans la note 183, y compris les moulins pondérés.

## 2. Collisions contre les anciennes familles

Pour une paire de prismes jumeaux, le complément de chacune des neuf arêtes
dans un prisme a quatre sommets et quatre arêtes. La famille `(2,2)` produit
donc **2·9²=162** collisions avec la nouvelle famille.

Contre `(3,3)`, la masse six laisse un point commun z. Les points extérieurs
de degré un dans chaque prisme sont au nombre de soixante ; chacun donne douze
paires de représentants. Les trois points de degré deux donnent chacun vingt-quatre
paires. Les deux signes et les deux orientations des supports sont inclus :

    60·12+3·24 = 792 collisions par paire de prismes.

Ces facteurs sont aussi vérifiés directement dans les modèles finis du programme.

Pour une paire de supports D, la masse sept ne laisse aucun point commun.
Chaque D contient deux triangles, et dix chemins induits à trois sommets évitant
le centre. Le complément de chacun possède quatre sommets et quatre arêtes.
Deux triangles donnent la branche à une arête transversale ; un triangle et un
chemin donnent la branche anticomplète. On obtient

    2·(2·2+2·2·10) = 88 collisions par paire de D.

Les pertes contre les anciennes familles sont ainsi au plus **954τ+88Ω**.

## 3. Deux points communs : masse six entre nouveaux représentants

Fixons deux prismes jumeaux. Leurs 87 points extérieurs se répartissent en trois
apices A de degré deux dans chacun, soixante points B de degré un, et vingt-quatre
points Z de degré zéro. Posons t=e(A), donc 0≤t≤3.

Les six fibres de B au-dessus des sommets de chaque prisme ont taille dix et
contiennent chacune cinq arêtes. Les trente arêtes qui restent dans une fibre
du premier prisme et les trente du second sont distinctes : sinon une arête
aurait deux voisins communs.

Pour un apex a, les équations λ,μ avec les sommets d'un prisme donnent

    d_B(a)=4−2d_A(a),       d_Z(a)=6+d_A(a).

Pour un point b de B, elles donnent d_B(b)=8−2d_A(b). Donc

    e(A,B)=12−4t,       e(A,Z)=18+2t,       e(B)=228+4t.

La cellule de B voyant un sommet u du premier prisme et v du second contient
un point si leurs arêtes transversales ont le même apex, et deux sinon. Chacune
des quatre combinaisons de triangles des deux prismes contient ainsi quinze points.

Les deux points communs des représentants doivent appartenir aux cas suivants.
Le tableau inclut les deux signes et compte des paires non ordonnées de représentants.

| Points communs | Condition nécessaire | Borne de perte |
|---|---|---:|
| B,B de même signe | adjacents ; au plus six collisions s'ils partagent une fibre, deux sinon | 696+8t |
| A,Z de même signe | adjacents ; deux collisions | 36+4t |
| A,B de même signe | les deux voisins de B appartiennent aux deux arêtes de l'apex ; douze paires de points possibles | 24 |
| B,B de signes opposés | non adjacents et dans des triangles opposés dans les deux prismes ; au plus 2·15² paires | 900 |
| A,A de signes opposés | non adjacents ; huit collisions | 24−8t |

Les autres cas ne donnent aucun représentant. Le premier total est
6·60+2(e(B)−60)=696+8t. La somme du tableau vaut **1680+4t**.
Le programme vérifie les nombres et les conditions exactes sur les 1526
configurations locales admissibles de deux points extérieurs.

Pour un prisme, deux apices adjacents, ajoutés à son support, donnent le type C14.
Réciproquement ce type contient exactement deux prismes ainsi obtenus. Donc
Σ_prismes t=2C14. Les prismes d'une même classe de projection ont les mêmes
trois apices et chaque classe a taille au plus six. Par conséquent

    Σ_paires jumelles t ≤ (5/2)Σ_prismes t =5C14.

La perte nouvelle–nouvelle de masse six est au plus 1680τ+20C14 ; avec le §2,
la perte totale de cette masse est donc

    **2634τ+20C14.**                                      (1)

## 4. Un point commun : masse sept entre nouveaux représentants

Dans D, les voisinages extérieurs possibles ont taille au plus deux. Il y a
exactement sept types de paires de voisins : chacun apparaît une fois, par les
déficits λ,μ. Pour deux supports D de même projection, ces sept points sont donc
appariés par une permutation σ entre les deux listes de types.

Dans le codage du programme, le centre est 6, ses voisins sont 2,3,4,5, et les
sept paires sont

    01, 12, 13, 04, 24, 05, 35.

Notons r leur nombre de voisins du centre, et t leur poids combinatoire dans
la collision. Les deux listes sont

    r=(0,1,1,1,2,1,2),       t=(4,3,3,3,0,3,0).

Pour les points de degré un, le poids vaut 0 aux sommets 0,1, vaut 1 aux quatre
voisins du centre et vaut 2 au centre. Les budgets de voisins communs entre les
deux supports donnent, avant soustraction des points de degré deux, 104 paires
de représentants. Les points doubles retirent 2Σr_i r_σ(i) de cette contribution,
puis ajoutent 2Σt_i t_σ(i). Le total exact pour une permutation compatible est donc

    104+2Σ_i(t_i t_σ(i)−r_i r_σ(i)).

Pour les trois couples possibles (t,r)=(4,0),(3,1),(0,2), on a
|t_i−t_j|≥|r_i−r_j|. En sommant l'inégalité quadratique correspondante sur une
permutation, le terme de somme est au plus Σ(t_i²−r_i²)=40. La perte est donc
au plus **184 par paire de D**. Le programme vérifie également les 5040 permutations.

Avec les 88 collisions anciennes du §2, la perte totale de masse sept est

    **272Ω.**                                             (2)

## 5. Borne complète de la nouvelle famille

En ajoutant (1),(2) aux pertes de masse huit de la note 183, une borne sûre du
nombre de paires à soustraire est

    L44 = 997920+2794τ+272Ω+(668/3)C14
          +72C_2022000+32C_5683824+128C_5691760
          +100C_127305925+144C_128354469+64C_245715219.

Le nombre de nouvelles images non déjà comptées est au moins F8−L44. Lorsque
cette expression est négative, on garde simplement la borne antérieure. Les
classes multiples peuvent rendre certaines soustractions redondantes ; cela
affaiblit la borne sans l'invalider.

En ajoutant F8−L44 à la borne de sept sommets, on obtient la nouvelle contrainte

    b4 ≥ 8105328−252P−8H−13572ρ−3274τ−370Ω
          −66C_2022000−28C_5683824−120C_5691760
          −110C_127305925−156C_128354469−64C_245715219
          −(668/3)C14.                                    (3)

## 6. Une borne supplémentaire sur les paires de prismes

Les classes de prismes ont taille au plus six. Si une classe a taille six,
ses 36 sommets, ses trois apices et les soixante points de degré un occupent
tous les sommets du graphe. Pour un apex a, la régularité impose alors

    14=12+d_A(a)+(4−2d_A(a)),

donc d_A(a)=2. Les trois apices forment un triangle et chaque prisme de la classe
se complète en une grille. Au plus 6ρ prismes appartiennent donc à des classes
de taille six. Comme C(m,2)≤2m pour m≤5 et C(6,2)=2·6+3, on en déduit

    **τ≤2P+3ρ.**                                         (4)

Cette borne est compatible avec 2τ≤5P et les deux sont conservées.

LAB propose également, au message 223, une borne qui relie τ au recensement à
neuf sommets. Soit N4 le compte signé des différences « prisme moins triangle
lointain », ligne `Q4_edges9_3_cross0` de la note 182. Les prismes d'une même
classe de projection sont disjoints ; chaque prisme jumeau fournit donc deux
triangles lointains distincts. Une paire non ordonnée de prismes jumeaux donne
quatre couples (prisme, triangle), tandis que N4 compte deux fois ces couples.
Ainsi

    **8τ≤N4.**                                            (5)

Le certificat `nine_vertex_twin_coupling.py` donne N4≤17325 sur la relaxation de
comptage. L'intérêt de (5) est surtout son couplage avec les mêmes invariants
que les familles N6,N8 à neuf sommets. Elle est incluse dans l'optimisation ci-dessous.

En combinant ces contraintes avec le recensement complet à neuf sommets, on
obtient aussi le nouveau plafond certifié **τ≤1890**, contre 2130 déduit jusque-là
de P≤852 et 2τ≤5P. Le certificat rationnel est archivé avec celui de N4.

## 7. Vérification et résultat d'optimisation

`four_four_small_mass_audit.py` vérifie les comptages finis. `four_four_bound.py`
combine (3),(4), les anciennes bornes, et la non-négativité des 5311 comptes de
graphes à neuf sommets. Les certificats rationnels donnent :

| Cas | Avant (3) | Après (3) |
|---|---:|---:|
| Sans condition supplémentaire | 3371634 | 3371634 |
| P=0 | 5764374 | 5764374 |

Cette première borne complète ne suffit donc pas à relever le minimum uniforme.
Elle permet néanmoins d'utiliser la famille `(4,4)` avec une perte justifiée
dans un système couplé, ou de localiser les majorations de pertes à affiner.
Les familles `(6,3)` et `(7,1)` ne sont pas comptées comme injectives par cette note.

À titre de cible conditionnelle, le même système géométrique vérifie exactement

    N8+(651/34)N6−1000τ ≥64543248/5.

La pénalité 1000τ est absorbée sans baisse de cette ancienne minoration conjointe.
Ce certificat utilise 2τ≤5P et (4) ; le coefficient de (5) dans ce certificat est
nul. Avec une pénalité exploratoire 2794τ, le seuil certifié devient 373884525/34.
**Ces pénalités ne sont pas des pertes démontrées de la famille `(6,3)`** : elles
servent seulement à mesurer les objectifs possibles pour son futur audit.

Certificats : `data/codex_four_four_small_mass_audit.json` et
`data/codex_four_four_bound.json`. Le rang 37 reste ouvert.
Les cibles conditionnelles sont dans `data/codex_nine_vertex_twin_coupling.json`.
