# 224 — Audit de la réduction LAP : rang 37, voisinage de droite sans petits cycles

9 octobre 2026. Source : dépôt `amazing-source/conway99-c2-aws`, commit
`15a3cfe3f6ccaa68c5e862d745a3a60558f60626`, dossier
`c1_rank37_girth5_lines/`. Résultat transmis par LAB, message 416.

**Énoncé annoncé par LAP.** Dans un SRG(99,14,1,2) de rang modulo sept
de A−3I égal à 37, si le graphe G(T) des 36 voisins extérieurs d'un
triangle T n'a ni triangle ni cycle de longueur quatre, alors G(T)
est connexe.

**Conclusion de cet audit.** La réduction algébrique et les conditions
nécessaires données aux recherches sont valides. La classification des
petites composantes, leur torsion et la fin du cas de torsion maximale
ont été reproduites indépendamment. La lecture des générateurs et des
deux moteurs de recherche d'étoiles n'a révélé aucun élagage injustifié.
Les journaux couvrent tous les paramètres annoncés et ne signalent aucun
arrêt au plafond.

La partie informatique de l'énoncé complet repose encore en partie sur
les exécutions archivées par LAP : cet audit ne prétend pas avoir rejoué
les 576 recherches d'étoiles ni les 33784128 matrices de la première
étape du cas (3,3). Une réimplémentation d'une étoile témoin (0,0) est
confiée à LAB ; son résultat sera consigné séparément lorsqu'il arrivera.

## 1. L'espace quadratique et les relations de la boule

Toutes les égalités de cette section sont dans F₇, sauf précision.
Posons B=A−3I et Q=B+3J. Comme B1=4·1 et 1ᵀ1=99=1, la décomposition
F₇⁹⁹=⟨1⟩⊕1⊥ montre que Q annule exactement la direction non nulle
de B portée par 1 et coïncide avec B sur 1⊥. Ainsi rang Q=36.

Dans V=F₇⁹⁹/ker Q, muni de la forme Q, p_v est l'image de e_v.
On a dim V=36, V non dégénéré, p_v²=0 et

    ⟨p_v,p_w⟩=3+A_vw,             v≠w.

L'identité SRG A²+A=12I+2J donne Q(A+4I)=56J=0, donc

    4p_v + Σ_{w~v} p_w = 0.                              (1)

Sur N(T), notons G la matrice du graphe cubique et H=3I−G.
La matrice de Gram des p_w est M₀=3J−H. Puisque H1=0 et 36=1
modulo sept,

    R₀ := ker M₀ = ker H ∩ 1⊥.                           (2)

Les trois points de T appartiennent eux aussi à W=span(p_w:w∈N(T)).
En effet, si s_i est la somme des p_w dans la couche i, (1) sur T
donne (3I₃+J₃)p_T=−s. Cette matrice est inversible et

    p_ti = 2s_i + 2(s_0+s_1+s_2).                        (3)

Ce point justifie l'absence de coordonnée résiduelle des points de T
dans les équations de somme d'une étoile.

## 2. Pourquoi les seules composantes déconnectées possibles ont taille 18

Chaque point de G a un partenaire dans sa couche et exactement un
voisin dans chacune des deux autres couches. Chaque composante a donc
le même nombre pair de points dans chaque couche, soit une taille 6m.

Un contrôle indépendant énumère les deux formes normales à six points
et les 216 formes normales à douze points : aucune n'a maille au moins
cinq. Une composante admissible a donc au moins 18 points. Si G est
déconnecté, ses 36 points forment exactement deux composantes C₁,C₂
de 18 points.

Le calcul indépendant à 18 points retrouve les **288** formes normales.
Leurs orbites, en conservant les couches à permutation globale près,
se partitionnent exactement en sept classes, de tailles

    24, 72, 72, 72, 8, 24, 16.

Le calcul de leurs noyaux sur F₇ donne les dimensions de torsion

    0, 0, 1, 1, 0, 3, 0.

Aucun isomorphisme oubliant arbitrairement la partition en couches
n'est utilisé. Pour le type de torsion trois, les six permutations de
couches sont effectivement réalisées par des automorphismes ; leurs
permutations explicites sont archivées dans le rapport indépendant.

## 3. Relations vraies, torsion équilibrée et quatre cas

Écrivons N pour l'incidence entre les 36 points proches et les 60
points lointains. Sur les entiers,

    NNᵀ = K = 12I−G−G²+2J−diag(J₁₂,J₁₂,J₁₂).

Le vecteur z₀=1_C₁−1_C₂ vérifie Kz₀=0. La positivité réelle de NNᵀ
donne Nᵀz₀=0 : chaque ombre lointaine rencontre chaque composante en
exactement trois points. Les sommes par couche de z₀ sont nulles ;
son prolongement par zéro est un vrai vecteur propre entier de valeur
propre 3, donc une relation vraie parmi les p_w.

Si E_i est le noyau de torsion, de somme nulle, du laplacien de C_i,
alors R₀=⟨z₀⟩⊕E₁⊕E₂. Les sommes par couche de chaque vecteur de
torsion sont nulles (sommation de Hφ=0 sur chaque couche). Un tel
vecteur donne une relation vraie exactement quand Nᵀφ=0, propriété
appelée ici « équilibre ».

Le lemme qui interdit un vecteur équilibré non nul porté par une seule
composante est également reproduit indépendamment. Les ombres y sont
des triplets distincts, puisqu'en partager trois points contredirait
λ,μ≤2. Pour chacun des 59 vecteurs projectifs de torsion des trois
types concernés, il manque des triplets de somme φ nulle pour remplir
au moins une demande K_uv. Les minima constatés sont respectivement
44,24,12 paires déficitaires pour les types 2,3,5.

Soient t_i=dim E_i et b la dimension de la torsion équilibrée dans
E₁⊕E₂. Ses projections sur chaque E_i sont injectives, donc
b≤min(t₁,t₂). Le noyau des relations vraies a dimension 1+b ; ainsi

    dim W = 35−b,            dim rad(W)=t₁+t₂−b.

Comme rad(W)⊆W⊥ et dim W⊥=1+b, on obtient

    2b ≥ t₁+t₂−1.                                      (4)

Avec t_i∈{0,1,3}, seules restent les possibilités suivantes :

| (t₁,t₂), à échange près | b | dim rad(W) | dimension résiduelle |
|---|---:|---:|---:|
| (0,0) | 0 | 0 | 1 |
| (0,1) | 0 | 1 | 0 |
| (1,1) | 1 | 1 | 1 |
| (3,3) | 3 | 3 | 1 |

La dimension résiduelle est dim V−dim W−dim rad(W).

## 4. Vérification des paramètres scalaires

Dans les cas avec un seul radical non nul, prenons son vecteur φ et
une forme β sur les coefficients des p_w avec β(φ)=1 et β nulle sur
les relations vraies. On peut choisir un vecteur dual isotrope m tel
que ⟨m,p_w⟩=β_w. Pour une ombre n, posons s=φᵀn et résolvons

    M₀c = r(n) := 3·1+n−sβ.

Les conditions d'équilibre assurent que r(n) est dans l'image de M₀.
Le vecteur Pc−(βᵀc)Pφ appartient au complément non dégénéré de la
direction radicale dans W. Le terme −βᵀc, explicitement conservé dans
`check_model.py`, est essentiel ; il n'a pas été omis dans le modèle.
Avec une éventuelle direction orthogonale η de norme c₀≠0,

    p_f = Pc + (α_f−βᵀc)Pφ + s_f m + ν_f η.

On retrouve exactement, pour g(n,n′)=cᵀr(n′),

    g(n,n)+2αs+c₀ν²=0,
    g(n,n′)+αs′+α′s+c₀νν′=3+A_ff′.                     (5)

Les termes en ν sont absents si la dimension résiduelle est zéro.
Dans le cas (0,0), le même calcul sans radical donne
g(n,n′)=6−nᵀ(H₁⁺⊕H₂⁺)n′, puis les formules de LAP.

Appliquer (1) en un point proche u et utiliser (3) donne

    Σ_{f~u, lointain} ν_f=0,
    Σ_{f~u, lointain} α_f=−(4β_u+β_t+β_u′+β_u1+β_u2),
    β_t=2Σ_{couche de u}β+2Σ_{N(T)}β.

Les six valeurs non nulles de c₀ sont couvertes par les deux classes
de carrés représentées par 1 et 3. Pour (1,1), la relation équilibrée
est φ₁+λφ₂ avec λ∈F₇*, soit les six valeurs effectivement testées.

## 5. Nécessité des contraintes d'étoile et lecture des moteurs

Les dix voisins lointains d'un point proche u ont des ombres de six
points, deux par couche, trois par composante, sans partenaires, avec
Gn≤2−n et somme K e_u. Les deux sommets complétant les arêtes
transversales issues de u sont isolés dans l'étoile lointaine ; les
huit autres y forment quatre arêtes. Cela découle du fait que le
voisinage de tout point du SRG est un couplage de sept arêtes.

Les tests lus dans `starc.c` et `starg.c` sont nécessaires : capacités
résiduelles des points, intersections d'ombres, valeurs (5), partenaire
unique, disponibilité d'un partenaire futur et sommes finales. Deux
ombres identiques sont impossibles. Fixer le signe de la première
coordonnée ν non nulle est légitime par ν↦−ν simultanément. Les
recherches de la preuve désactivent les filtres réels flottants optionnels.

L'analyse des journaux retrouve exactement les grilles de paramètres :
192 cas (0,0), 48 cas (0,1), 48 cas (1,0), 288 cas (1,1). Aucun
doublon ni paramètre absent ; chaque ligne annonce zéro solution et
zéro arrêt au plafond. Les nombres d'items sont sous les capacités
des tableaux C. Ces contrôles portent sur les journaux archivés, sans
prétendre rejouer ces 576 recherches dans cet audit.

## 6. Cas (3,3) : ce qui est reproduit indépendamment

Par (4), la torsion équilibrée est le graphe d'un isomorphisme.
Après choix de bases, chaque ombre satisfait σ₁(n)+Mσ₂(n)=0 avec
M∈GL₃(F₇). Ce groupe contient (343−1)(343−7)(343−49)=33784128
matrices. LAP les énumère par les neuf chiffres en base sept d'un
entier de 0 à 7⁹−1, puis teste le déterminant modulo sept.

La condition combinatoire utilisée est plus faible que l'étoile complète :
dix ombres équilibrées à somme K e_u et intersections deux à deux au plus
deux. Son impossibilité suffit donc à exclure M.

Le programme indépendant reconstruit les domaines d'ombres et les bases
de torsion, puis effectue un changement de base explicite vers la convention
des codes archivés. Il reproduit entièrement les deux étapes finales :

    25588 matrices fournies à u=1 → les mêmes 44 matrices,
    ces 44 matrices à u=6 → zéro.

Un témoin positif à u=1 est reconstruit et vérifié par substitution
dans les 36 sommes et les intersections. Aucune fonction des moteurs
LAP n'est importée dans cette réimplémentation.

La première liste de 25588 matrices, obtenue à u=0 sur tout GL₃(F₇),
reste celle de LAP : son moteur a été lu, ses codes contrôlés distincts
et inversibles, mais cette première recherche complète n'est pas rejouée.

## 7. Fichiers, reproduction et portée

- `code/codex/audit_lap_girth5.py` : audit indépendant des éléments finis,
  couverture des journaux, réimplémentation des deux dernières étapes (3,3).
- `data/codex_audit_lap_girth5.json` : résultats et empreintes SHA-256
  des sources, entrées et journaux de LAP utilisés.
- Export local immuable du dossier source :
  `C:/home/researcher/Desktop/c1-lap-girth5-audit/15a3cfe3f/`.

Commande à la racine du dépôt C1 :

    python code/codex/audit_lap_girth5.py --source C:/home/researcher/Desktop/c1-lap-girth5-audit/15a3cfe3f --out data/codex_audit_lap_girth5.json

L'énoncé vise une famille entière de voisinages déconnectés, y compris
leurs possibilités de torsion. Il ne concerne pas les seuls exemples
déjà exclus des notes 211–216. En revanche, il ne traite ni les voisinages
connexes, ni ceux contenant un triangle ou un carré. Il ne ferme pas le
rang 37 et ne diminue pas directement la liste des 174 noyaux sans rang.
