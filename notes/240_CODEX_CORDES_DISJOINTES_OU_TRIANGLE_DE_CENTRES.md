# 240 — Deux cordes disjointes, ou un triangle de centres

9 octobre 2026. Cette note exploite le message LAB 476, qui ferme les
étoiles de cordes laissées ouvertes par la note 239. Elle ajoute une
exclusion arithmétique du triangle latéral dans le ruban tordu.

## 1. Réduction obtenue

Soit un ruban fermé à six étapes, sur dix-huit sommets distincts, dans
un hypothétique SRG(99,14,1,2). Soit E **l'ensemble de toutes les cordes**
du sous-graphe induit sur ces sommets.

**Théorème, utilisant le résultat de pair précisé au §2.** Une des deux
possibilités suivantes a nécessairement lieu :

1. E contient deux arêtes sans extrémité commune ;
2. E est exactement le triangle `{c_0c_2,c_2c_4,c_4c_0}`, à rotation près.

Le second cas vaut pour les deux fermetures du ruban. Il reste ouvert.
Le premier peut comporter deux, trois ou davantage de cordes : aucune
réalisation en SRG n'est affirmée. Le résultat ne suppose ni rang ni
automorphisme de C1, mais suppose bien les dix-huit sommets distincts.

En particulier, une réparation par **exactement deux cordes** doit employer
quatre extrémités distinctes. Si toutes les cordes sont portées par au
plus trois sommets, seuls les triangles de centres alternés subsistent.

## 2. Apport LAB : toutes les étoiles de cordes sont exclues

La note 239 exclut les étoiles centrées sur un sommet latéral. Pour un
centre commun c_0, elle ne laisse que `{c_0a_4,c_0b_3}` ou `{c_0c_2,c_0c_4}`
à symétrie près.

LAB annonce au message du pont **476**, commit **589ea52**, l'exclusion
exacte de ces deux formes pour les deux fermetures. Les fichiers annoncés
sont `ribbon6_star_forms.py` et `ribbon6_star_forms.json`, section 14 de
son fichier de travail. Les masques extérieurs satisfont les axiomes
locaux et les deux compléments de Schur exacts. Les équations imposent
leur nombre total, les degrés résiduels et les voisins communs résiduels.

Les nombres de masques annoncés sont 119,119,111 pour les deux représentants
mixtes puis le représentant entre centres du cylindre ; 118,118,107 pour
ceux du ruban tordu. LAB indique avoir vérifié les vecteurs de Farkas contre
tous ces masques. Ce résultat de pair est utilisé avec cette attribution ;
il n'est pas réaudité ici. Il ferme exactement le reliquat de la note 239.

On en déduit que **les cordes ne peuvent pas avoir un sommet commun**.
La coupe de la note 239 est donc valable pour chacun des dix-huit sommets u,
et plus seulement les sommets latéraux :

    Σ_(vw corde potentielle, u∉{v,w}) A_vw ≥ 1.

## 3. Pourquoi il suffit ensuite de considérer un triangle

Un graphe simple non vide dans lequel toute paire d'arêtes se rencontre
est soit une étoile, soit un triangle. Preuve courte : prendre uv et uw.
S'il existe une arête ne contenant pas u, elle doit être vw. Toute arête
rencontrant simultanément uv,uw,vw est alors une de ces trois arêtes.

L'exclusion des étoiles entraîne donc la dichotomie : deux cordes
disjointes, ou exactement trois cordes formant un triangle.

La classification locale de ces triangles est minuscule. Ajouter les
trois arêtes sur chacun des triplets de positions qui sont des non-arêtes
du ruban, puis imposer `(A²+A)_uv≤2` pour u≠v, ne laisse que :

* fermeture ordinaire : `{c_0,c_2,c_4}` et `{c_1,c_3,c_5}` ;
* fermeture tordue : les deux mêmes triangles de centres et les quatre
  triangles latéraux `{a_0,a_4,b_2}`, `{a_1,a_5,b_3}`,
  `{a_2,b_0,b_4}`, `{a_3,b_1,b_5}`.

Les deux triangles de centres sont équivalents par rotation. Les quatre
triangles latéraux du ruban tordu le sont également : dans l'ordre du
cycle latéral à douze positions, leurs indices sont `{j,j+4,j+8}`.

## 4. Exclusion nouvelle du triangle latéral tordu

Soit F le ruban tordu augmenté exactement des trois arêtes du triangle
`{a_0,a_4,b_2}`. Il a dix-huit sommets et trente-neuf arêtes. Il reste
81 sommets extérieurs. Poser `D=2-A_F-A_F²` hors diagonale.

Chaque voisinage extérieur b est un vecteur binaire satisfaisant

    |b|≤14,
    b A_F ≤ 2·1-b,
    b_u b_v=0 lorsque D_uv=0.

Il existe exactement 288 masques satisfaisant ces conditions. Le masque
vide est inclus. **Aucun filtre spectral n'est utilisé dans cette preuve.**
Les multiplicités x_b≥0 devraient satisfaire

    Σ_b x_b = 81,
    Σ_b x_b b_u = 14-deg_F(u),
    Σ_b x_b b_u b_v = D_uv.

Le certificat entier archivé combine soixante de ces égalités. Son
coefficient sur chaque x_b est non négatif, tandis que sa combinaison
des seconds membres vaut **−3**. C'est une contradiction. Par rotation,
les quatre triangles latéraux tordus sont donc exclus. Cela achève la
réduction du §1.

La recherche du certificat a utilisé un programme linéaire. Sa validité
finale est contrôlée exclusivement avec des entiers et ne dépend pas du
statut numérique du solveur. Il se trouve dans
`data/codex_ribbon6_triangle_certificate.json`, avec les 288 masques et
l'ordre des lignes : total, dix-huit degrés, puis les paires dans l'ordre
lexicographique. Indices a_i=i, b_i=6+i, c_i=12+i.

Le contrôle autonome, bibliothèque standard Python seulement, est :

    python code/codex/ribbon_six_matching.py

Il reconstruit la classification des triangles, tous les masques et les
coefficients de la combinaison. Il ne recontrôle pas les certificats de
pair du §2 ; cette dépendance est explicitement annoncée.

## 5. Exploration du reliquat : les triangles forcés de deux cordes

Une corde dont les extrémités n'ont pas de voisin commun interne exige
un troisième sommet extérieur dans son triangle. Pour les quatre exemples
de deux cordes disjointes donnés par LAB, le pilote
`code/codex/ribbon_two_chord_triangles.py` impose conjointement ces deux
sommets, les budgets locaux et les deux compléments de Schur 2×2 exacts.

| Cordes, fermeture ordinaire | Paires de masques/adjacence restantes |
|---|---:|
| c_0c_3, c_1c_4 | 126 |
| c_0c_2, c_1c_4 | 87 |
| a_0b_3, a_1b_4 | 358 |
| a_0c_2, a_1c_4 | 106 |

Dans ces exemples, les deux sommets complétant les triangles sont
nécessairement distincts : aucun masque admissible ne contient les deux
cordes. Mais leur réalisation conjointe n'est pas exclue par ce test.
Les nombres de la table ne sont pas des graphes C1 construits.

Les deux supports avec un triangle de centres alternés ont aussi une
relaxation de multiplicités numériquement faisable ; ce n'est pas une
preuve d'existence. Leur transport interne déterminé ne révèle pas de
nouveau cycle fermé : il retrouve seulement le cycle six de départ.
Ces essais sont bornés, ne ferment pas les familles restantes et ne
justifient pas de relancer une grande campagne identique.

Le résultat positif de cette étape est la dichotomie du §1 : une réparation
sur trois sommets est réduite au triangle de centres alternés, et toute
autre réparation contient deux cordes disjointes. Aucun rang ni noyau
global n'est déclaré exclu.
