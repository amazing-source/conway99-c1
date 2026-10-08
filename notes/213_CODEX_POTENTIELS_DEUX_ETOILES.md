# 213 — Une preuve par potentiels, sans les équations de degré

8 octobre 2026. Suite de la note 212. Sur la branche 0 de la boule
cyclique (2,4,1), u=0, v=12, le certificat de deux étoiles se simplifie
encore : **les équations exactes de degré peuvent être supprimées**.
Après arrondissement de petits potentiels entiers, une contradiction
de marge 7 subsiste. Le contrôle n'utilise plus la matrice du LP.

Il s'agit du même exemple de contrôle déjà exclu. Les domaines et
compatibilités restent ceux de la note 212, y compris leurs filtres
de voisins communs et de capacités de degré. Supprimer les équations
de degré ne supprime pas ces filtres, ni la propagation préalable.

## 1. Critère exact par potentiels locaux

Soient D_i les 18 domaines d'ombres privées, s(i)∈{0,1} leur côté,
n_i(c) leur vecteur d'incidence, et E_ij⊆D_i×D_j les paires
compatibles. On cherche des choix c_i tels que

    (c_i,c_j)∈E_ij,
    Σ_{i:s(i)=s} n_i(c_i) = t_s = K e_centre(s) − w.

Choisissons deux vecteurs entiers β_s de longueur 36 et, pour chaque
paire i<j, deux fonctions entières η_ij^i sur D_i et η_ij^j sur D_j.
Définissons

    F_i(c) = β_s(i) · n_i(c) − Σ_{j≠i} η_ij^i(c),
    P_ij(c,d) = η_ij^i(c) + η_ij^j(d),
    L = Σ_i min_{c∈D_i} F_i(c)
        + Σ_{i<j} min_{(c,d)∈E_ij} P_ij(c,d).

L'indice η_ij^i désigne aussi η_ji^i lorsque j<i. Les potentiels se
compensent exactement dans la somme. Tout choix admissible vérifie

    Σ_i F_i(c_i) + Σ_{i<j} P_ij(c_i,c_j)
      = β_0·t_0 + β_1·t_1.

Le membre de gauche est au moins L. Par conséquent,

    L > β_0·t_0 + β_1·t_1

est un certificat d'impossibilité. C'est un argument fini par
addition d'inégalités locales. Il vaut aussi pour des distributions
x_i et y_ij de masse un et de marginales cohérentes, en prenant
l'espérance de chaque terme. Il ne requiert pas les bornes séparées
x_j≤1 utilisées dans le premier certificat de la note 212.

## 2. Extraction et suppression des degrés

Les multiplicateurs des sommes d'étoile fournissent β, ceux des
équations de marginales fournissent η. Les 18 multiplicateurs de
normalisation s'annulent entre la borne et le second membre ; on
les omet. Avec des multiplicateurs γ des degrés encore présents,
il faut ajouter −Σ_t γ_it cap_it(c) à F_i, et
(γ_i,s(j)+γ_j,s(i)) a_ij(c,d) à P_ij.

Sur le certificat de la note 212, la borne par masses un donne une
marge entière de 4531, contre 4067 pour la borne par boîtes. En
mettant **tous les γ à zéro**, sans aucune nouvelle optimisation,
la marge demeure strictement positive : 1875. Ce calcul établit
précisément que les équations de degré ne sont pas nécessaires à
ce rejet, sur les domaines filtrés conservés.

Les changements de jauge suivants raccourcissent les données :

- une constante retirée à η_ij^i augmente F_i d'autant et diminue
  P_ij d'autant, sans changer la marge ;
- ajouter une constante à β sur une couche ne change pas la marge,
  puisque toutes les ombres ont deux points par couche ;
- une coordonnée β_p peut être annulée lorsque chaque domaine de
  l'étoile a une incidence constante en p et que leurs constantes
  somment au bon t_s(p).

Après ces changements, on arrondit les potentiels divisés par une
unité entière et on **recontrôle toutes les inégalités exactement**.
L'arrondissement n'est jamais supposé préserver une preuve.

| Unité de division | Marge exacte après arrondissement |
|---|---:|
| 1 | 1875 |
| 2 | 900 |
| 5 | 353 |
| 10 | 163 |
| 20 | 53 |
| 50 | 7 |
| 100 | −4, ne certifie rien |

Le fichier publié retient l'unité 50. Il contient 41 coefficients
β non nuls et 3244 valeurs de potentiels η non nulles, toutes de
valeur absolue au plus 46, contre 9700 lignes pondérées dans le
certificat précédent. Les 36 coefficients γ sont nuls.

Les 18 minima unaires somment à −236, et les 153 minima de paires
à −169. Ainsi

    L = −405 > −412 = β_0·t_0 + β_1·t_1.

La contradiction a une marge exacte de 7. Le nombre 7 est ici une
marge entière issue du choix d'arrondissement ; on n'en déduit
aucune interprétation arithmétique modulo sept.

## 3. Vérification et portée

`code/codex/two_star_potentials.py` fournit une deuxième vérification
arithmétique, indépendante de la construction de la matrice LP :
il évalue directement les 18 fonctions F_i et les 153 tables P_ij,
avec des entiers Python. Il partage toujours le générateur des
domaines, les tables de compatibilité et le replay de propagation
de la note 212. Cette dépendance est explicite.

`data/codex_two_star_potentials_000.json` contient le graphe d'entrée,
l'apex, les indices des candidats conservés, tous les potentiels et
tous les minima. Il se vérifie sans le certificat Farkas original
et sans résoudre de LP :

    python code/codex/two_star_potentials.py --out data/codex_two_star_potentials_000.json --verify-only

Pour le régénérer :

    python code/codex/two_star_potentials.py --source data/codex_joint_star_pair_lp_000.json --drop-degrees --search-rounding --out data/codex_two_star_potentials_000.json

Pour un certificat provenant d'un autre poste, `--ball fichier.json`
permet de fournir le graphe localement lorsque le chemin d'origine
n'est pas accessible. Une branche déjà contradictoire par propagation
se traite directement avec le vérificateur de la note 212.

LAB a reproduit nos deux certificats et annoncé trois parcours
complets supplémentaires : boules aléatoires 5 et 9, respectivement
368 et 464 branches toutes rejetées par propagation ; boule 12,
412 branches rejetées par propagation et quatre par certificats LP.
Les sources et résumés sont au commit `7a02454`, et les quatre
vecteurs Farkas complets au commit `db1d993` de
`lab/theta-lp-2026-10-08`. Ce sont également des boules déjà exclues
par étoile unique. La suppression des degrés et les petits potentiels
de cette note sont, à ce stade, vérifiés uniquement sur notre branche 0.

La prochaine question précise est de trouver des β et η définis
uniformément à partir des ombres, de K et de H⁺, dont la marge reste
positive pour toute boule générique admissible. Une moyenne de
certificats obtenus sur des domaines différents peut suggérer une
formule, mais n'en prouve aucune des inégalités locales.
