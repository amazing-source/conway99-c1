# 212 — Deux certificats exacts pour des branches de deux étoiles

8 octobre 2026. Suite de la note 211 et de la relecture indépendante de
LAB. Cadre : droite générique au rang global 37, avec P=0. Les calculs
portent sur la boule cyclique (2,4,1), u=0, v=12, déjà exclue par les
calculs d'étoile unique. Les numéros d'apex sont les indices à partir
de zéro dans le pool trié des 473 supports communs.

**Résultat :** la branche 100 possède un certificat de propagation
exacte ; la branche 0, qui survit à cette propagation, possède un
certificat linéaire vérifié en entiers. Ces deux résultats remplacent
des verdicts de solveur par des preuves finies rejouables. Ils ne
constituent ni une nouvelle exclusion de boule, ni un lemme uniforme,
ni l'exclusion d'un rang global.

## 1. Domaines et compatibilité exacte

`joint_generic_stars.branch_domains` isole la construction des domaines
de la note 211. Fixer l'apex commun w laisse 18 variables : neuf
ombres privées de chaque côté. Les candidats restent des supports
binaires de six points, deux par couche, et satisfont les tests
unaires de la note 211.

`joint_star_propagation.setup` forme une table de compatibilité pour
chaque paire de variables. Pour deux candidats n_i,n_j, avec
a_ij=3−n_iᵀH⁺n_j modulo sept, elle exige :

1. a_ij∈{0,1} et |n_i∩n_j|≤2−a_ij ;
2. a_ij ne dépasse pas la capacité de degré de chaque candidat :
   1−(Gn_i)_centre dans son étoile, 2−(Gn_i)_autre-centre vers
   l'autre étoile ;
3. si a_ij=1, aucun point p avec (Gn_i)_p+n_i(p)=2 ne peut
   appartenir à n_j, et réciproquement ;
4. si les deux supports partagent p,q, leur contribution 2, plus
   w(p)w(q), ne dépasse pas K_pq.

Les capacités transversales sont des **égalités de degré**, et pas
seulement des majorants : pour une ombre z privée de S_u,

    deg_{S_v}(z) = 2 − (Gn_z)_v.

C'est la coordonnée (v,z) de NA_F=2J−(G+I)N, puisque n_z(v)=0.
L'apex commun est isolé dans l'union, donc le degré porte exactement
sur les neuf variables privées de S_v. Le degré interne vaut de même
1−(Gn_z)_u. Les tables n'utilisent que des conséquences nécessaires.

## 2. Branche 100 : propagation sans solveur

L'apex est {0,3,12,14,28,35}. Les domaines contiennent initialement
684 candidats. On répète deux règles :

- retirer un candidat sans partenaire compatible dans une autre
  variable ;
- retirer un candidat dont une coordonnée rend impossible la somme
  exacte des ombres de son étoile, même en utilisant séparément les
  minima et maxima des autres domaines.

Après 263 événements de suppression, dont 9 par somme et 254 par
absence de support, 464 candidats ont été supprimés et le domaine
de la variable 3 est vide. Cette variable est du côté u, groupe 5.

`data/codex_joint_star_propagation_100.json` conserve toute la trace.
La fonction `replay` ne relance pas l'algorithme de propagation :
elle vérifie chaque suppression sur les domaines encore vivants,
puis contrôle le domaine vide terminal. Toutes les opérations sont
entières ou modulo sept. Le générateur de domaines et les tables
sont communs au producteur et au vérificateur ; la relecture de leur
nécessité reste donc une partie distincte de l'audit.

## 3. Branche 0 : relaxation par marginales de paires

L'apex est {0,1,12,13,27,29}. La propagation retire 195 candidats sur
759 et laisse 564 candidats répartis dans les 18 variables. Elle ne
produit pas de contradiction. Sa trace est également archivée.

On introduit x_ic, poids du candidat c pour la variable i, puis
y_ijcd pour chaque paire de candidats compatible. Ce sont des
variables réelles dans [0,1], satisfaisant

    Σ_c x_ic = 1,
    Σ_d y_ijcd = x_ic,       Σ_c y_ijcd = x_jd.

Tout choix entier d'ombres fournit un tel point. On ajoute les
sommes exactes des étoiles et les degrés internes et transversaux
exacts, en écrivant l'adjacence comme la somme des poids y des
paires dont le produit de Green vaut 2.

Le modèle complet essayé ajoute aussi les plafonds d'incidence
proche/proche, les plafonds de voisins communs proche/lointain, et
les inégalités interdisant les prismes. Il comporte 22 339 variables
y, 564 variables x, 13 584 lignes et 384 581 coefficients non nuls.
Les équations de sommes multipliées par des indicateurs de candidats
(`--lift-sums`) ne sont pas utilisées dans le résultat présent.

HiGHS/IPM annonce l'infaisabilité en environ sept secondes. Son
interface ne fournissant pas de rayon dual exploitable sur ce test,
on résout explicitement un autre problème :

    minimiser bᵀλ + Σ_j z_j,
    Aᵀλ + z ≥ 0,    z ≥ 0,
    −1 ≤ λ_eq ≤ 1,  0 ≤ λ_ineq ≤ 1.

Une valeur strictement négative sépare le système Ax≤b, avec les
égalités interprétées comme telles et 0≤x≤1. Une solution numérique
sert uniquement à proposer des multiplicateurs entiers arrondis ;
elle ne fait pas partie du contrôle final.

## 4. Certificat entier et simplification

Le certificat archivé utilise 9 700 lignes avec multiplicateurs
entiers. Après remplacement de lignes redondantes, sa répartition
est :

| Famille | Lignes de poids non nul |
|---|---:|
| Normalisations des domaines | 18 |
| Équations de marginales de paires | 9 581 |
| Sommes des étoiles | 72 |
| Degrés internes ou transversaux | 29 |

Les seuls plafonds proche/proche du certificat brut contenaient u
ou v : ce sont exactement des lignes de sommes d'étoile. Les seuls
plafonds proche/lointain concernaient u ou v : leur ligne est
`degree(i,side) + 2*domain(i)`, de second membre 2. Leur remplacement
par ces égalités conserve exactement la combinaison des lignes.
Aucune inégalité de prisme n'avait de multiplicateur non nul.

Cela isole une obstruction dans les domaines filtrés, les marginales,
les sommes et les degrés. Les filtres des domaines et des paires
emploient toujours les contraintes de voisins communs décrites au
§1 ; on ne les a pas retirées.

La combinaison entière donne Cx≤−4589. Les bornes 0≤x_j≤1 donnent

    Cx ≥ Σ_j min(C_j,0) = −522.

Ainsi −522≤−4589 serait nécessaire, contradiction avec une marge
entière de 4067. Il reste 385 coefficients négatifs, pris en compte
exactement par les bornes supérieures, et 8 589 coefficients
positifs. Les bornes x,y≤1 découlent aussi des normalisations et des
marginales non négatives.

`verify_farkas` reconstruit C et les seconds membres en entiers
Python, vérifie le signe autorisé de chaque multiplicateur, et
contrôle cette stricte contradiction. `--verify-only` ne lance
aucun solveur. La preuve est exacte, mais son support de 9 700
lignes reste grand : il n'est pas encore une identité structurelle
courte transposable à toutes les boules.

## 5. Reproduction

Depuis la racine du dépôt, avec NumPy, SciPy, OR-Tools et highspy :

    python code/codex/joint_star_propagation.py --apex 100 --out data/codex_joint_star_propagation_100.json --verify-only
    python code/codex/joint_star_propagation.py --apex 0 --out data/codex_joint_star_propagation_000.json --verify-only
    python code/codex/joint_star_pair_lp.py --apex 0 --out data/codex_joint_star_pair_lp_000.json --verify-only

Pour rechercher de nouveau le certificat LP, enlever `--verify-only`
et utiliser `--seconds 60` (limite par résolution, y compris la
recherche duale). L'algorithme par défaut est IPM ; une tentative
simplex initiale avait retourné `Unknown`, sans conclusion.

Les deux scripts acceptent `--ball fichier.json`, clé `adjacency`
36×36, ainsi que `--u` et `--v`. Une branche déjà vide par propagation
se traite par le premier script, sans construire son LP.

Le contrôle de non-régression du modèle CP-SAT après extraction de
`branch_domains` retrouve l'infaisabilité de la branche 0 au
prétraitement. Les tests de vérificateurs rejettent aussi une
suppression avec un support encore vivant et un faux certificat
linéaire à la limite de faisabilité.

La suite utile est de réduire le support du certificat et de tester
si son mécanisme se retrouve sur d'autres boules génériques. Aucun
parcours exhaustif des 473 apex n'est revendiqué ici.
