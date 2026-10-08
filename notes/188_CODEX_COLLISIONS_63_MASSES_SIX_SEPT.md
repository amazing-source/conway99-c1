# 188 — Famille (6,3) : pertes internes de masses six et sept

8 octobre 2026. Réductions proposées par LAP, transmises par LAB aux messages
235–236 du pont ; énumérations, contraintes et certificats par Codex.

On considère les représentants signés ψ=±(1_W−1_Y), |W|=6, |Y|=3,
W∩Y=∅, **e(W)≤8**, aux normes Q=6 et Q=8. Pour ces deux normes, les seules
possibilités omises par e(W)≤8 sont celles où W est un prisme.

Les nombres de paires non ordonnées de représentants en collision, **avec
les deux signes**, satisfont les bornes suivantes par paire de supports jumeaux :

| Masse de la différence | Supports du noyau | Q=6 | Q=8 |
|---|---|---:|---:|
| 6 | Deux prismes | 756 | 12814 |
| 7 | Deux copies de D | 108 | 3612 |

En notant C_(q,s) le nombre global de collisions internes de norme q et de
masse positive s, on obtient donc

    C_(6,6) ≤756τ,       C_(6,7) ≤108Ω,
    C_(8,6) ≤12814τ,     C_(8,7) ≤3612Ω.

Les deux bornes concernant D valent même sans la restriction e(W)≤8.
Les différences de masses huit et neuf, ainsi que les collisions avec les
familles déjà comptées, restent à traiter. Cette note n'affirme donc pas
encore de nouvelle minoration complète de b3 ou b4.

## 1. Une paramétrisation exhaustive des petites masses

Pour une collision de même somme +3, la différence est un vecteur propre entier
de valeur +3. À masse positive six ou sept, le lemme S≥4h impose des coordonnées
dans {0,±1}. Les supports sont les deux prismes ou les deux copies de D déjà
classifiés dans les notes 168 et 181. Aucune coordonnée ne peut être commune
avec des signes opposés.

Fixons les deux supports X,X′ de taille m=6 ou 7, et leur orientation
δ=1_X−1_X′. Tous les représentants vérifiant ψ−ψ′=δ sont de la forme

    ψ  =1_X −1_B−1_B′+1_C−1_K,
    ψ′ =1_X′−1_B−1_B′+1_C−1_K,

avec B⊆X, B′⊆X′, C,K extérieurs aux deux supports, disjoints, et

    |C|=c,   |K|=9−m−c,   |B|=|B′|=m−6+c.

Ainsi les points communs extérieurs sont exactement trois pour m=6 et deux
pour m=7. L'énumération parcourt tous les choix B,B′,C,K, calcule Q directement
et conserve, pour la sous-famille retenue, e(W),e(W′)≤8.

Pour une orientation fixée de δ et une somme +3, chaque paire non ordonnée
est comptée une seule fois. Les représentants opposés donnent les collisions
de somme −3 : on multiplie donc par deux. Cette involution n'a pas de point fixe.
La différence détermine sa paire de supports, ce qui permet ensuite de multiplier
par τ ou Ω sans ambiguïté sur le type de perte.

Le programme énumère **64312 configurations locales** autour de deux prismes
et **7424** autour de deux copies de D. Il rejette toute configuration violant
les budgets λ≤1,μ≤2 sur les sommets visibles. Pour chaque type de degrés et
d'arêtes extérieurs, il contrôle aussi le calcul incrémental par la formule
quadratique complète sur les deux représentants : normes égales, somme trois,
neuf coordonnées non nulles, et restriction sur les arêtes positives.

## 2. Géométrie extérieure à deux prismes

Les 87 sommets extérieurs sont répartis en Z,B,A, selon leur nombre commun
d=0,1,2 de voisins dans chaque prisme :

    |Z|=24,   |B|=60,   |A|=3.

Les trois apices A sont les troisièmes points des arêtes transversales.
Après avoir apparié les arêtes transversales des deux prismes par leur apex,
un sommet B possède un voisin u dans le premier et v dans le second. La cellule
(u,v) contient exactement un point si les deux arêtes transversales ont le même
apex, et deux sinon. Il y a donc **40 profils** : Z, 36 cellules simples et 3 apices.

Si t=e(A), les comptes d'arêtes entre classes valent

| Classe | Nombre d'arêtes |
|---|---:|
| Z,Z | 33+t |
| Z,B | 252−4t |
| Z,A | 18+2t |
| B,B | 228+4t |
| B,A | 12−4t |
| A,A | t |

Le complément de la paire possède donc 543 arêtes. Ses degrés sont 14 sur Z,
12 sur B et 10 sur A, donnant 6279 chemins de longueur deux comptés par leur
sommet central, triangles inclus avec multiplicité trois.

Chaque sommet d'un prisme possède onze voisins extérieurs. Dans son voisinage,
qui est un appariement, dix de ces points forment cinq arêtes ; le dernier est
l'apex associé à son arête transversale. Il y a donc 12·5=60 arêtes extérieures
dont le troisième point de triangle appartient au noyau. Chacune des 543−60
autres arêtes appartient à un triangle entièrement extérieur : il y a exactement

    (543−60)/3=161 triangles extérieurs.

## 3. Le modèle complet des profils autour des prismes

Les seules classes Z,B,A donnent des bornes trop faibles. Le programme conserve
donc chaque profil individuel. Il introduit :

- E_ij, le nombre d'arêtes entre profils i,j ;
- X_(i,j,k;H), le nombre de triples de profils i,j,k dont les arêtes extérieures
  sont celles du type H, modulo les permutations des profils égaux.

Les effectifs n_i sont connus exactement. Les variables sont non négatives et
majorées par le nombre de paires ou de triples possibles dans leurs profils.
Les identités imposées sont les suivantes :

1. Pour un profil i de masque de voisins a_i dans les douze sommets du noyau,
   la somme des degrés extérieurs vaut n_i(14−|a_i|).
2. Pour chaque sommet u du noyau, le nombre de voisins communs de u avec les
   points de profil i est n_i(λ ou μ−|N_noyau(u)∩a_i|). C'est une somme de E_ij.
3. Chaque multiensemble de trois profils contient exactement le nombre
   combinatoire de triples prévu par les n_i. Chaque marge d'arête est E_ij
   multiplié par le nombre de choix du troisième point disponible.
4. Pour une paire de profils i,j, tous les couples ont c_ij=|a_i∩a_j| voisins
   communs dans le noyau. Si V_ij est leur nombre, la somme des voisins communs
   extérieurs vaut (2−c_ij)V_ij−E_ij. Pour les seuls couples adjacents, elle vaut
   (1−c_ij)E_ij. Ces deux identités s'expriment par les chemins et triangles
   des variables X.

Tout véritable graphe avec la paire de prismes satisfait ces contraintes.
On n'affirme pas la réciproque. Le système comprend **64147 variables**, dont
les variables de paires, et **89154 lignes d'inégalités** ; une égalité est
représentée par ses deux sens. La fonction à majorer est la somme du nombre
exact de collisions associé à chaque type local, multiplié par sa variable X.

## 4. Certification rationnelle sans supposer le point flottant exact

Le simplexe fournit des multiplicateurs candidats pour des lignes
a_i0+Σ_j a_ij x_j≥0. Ils sont remplacés par des rationnels non négatifs de
dénominateur commun 10^9. Si f=c_0+Σ_j c_jx_j est l'opposé du nombre de collisions,
on calcule exactement les résidus

    r_j=c_j−Σ_i w_i a_ij,       0≤x_j≤U_j.

Il vient, sans hypothèse numérique,

    f ≥ c_0−Σ_i w_i a_i0 + Σ_(r_j<0) r_j U_j.             (1)

Les plafonds rationnels obtenus, après ce contrôle exact, sont

    Q6 : 151451854779/200000000 =757,259273895,
    Q8 : 3203671164451/250000000 =12814,684657804.

Les collisions comptées avec leurs opposées sont en nombre pair. On peut donc
arrondir ces plafonds **vers le bas au nombre pair**, donnant 756 et 12814.
Les poids, résidus et bornes de variables sont archivés. L'appel `--verify-only`
reconstruit les lignes et vérifie (1) exactement, sans relancer le LP.

## 5. Deux copies de D : les sept profils doubles sont appariés

Les copies de D sont disjointes, avec pour seule arête entre elles celle des
centres. Les 85 points extérieurs satisfont

    |Z|=17,   |B|=61,   |A|=7.

Les sept voisinages doubles possibles dans chaque copie apparaissent chacun
une fois. Ils évitent le centre. Leur bijection entre les deux copies est
inconnue ; on parcourt les **5040 permutations**. Pour une permutation donnée,
chaque cellule simple (u,v) possède exactement

    [λ ou μ]−|N_noyau(u)∩N_noyau(v)|
       − #{apices adjacents à u et v}

points. Un effectif négatif est une contradiction combinatoire exacte : cela
élimine 560 permutations. Les **4480 restantes** sont toutes conservées.

Pour t=e(A), les comptes d'arêtes sont

| Classe | Nombre d'arêtes |
|---|---:|
| Z,Z | 14+t |
| Z,B | 182−4t |
| Z,A | 28+2t |
| B,B | 254+4t |
| B,A | 42−4t |
| A,A | t |

En particulier 0≤t≤10, par intégralité et e(A,B)≥0. Pour les établir, un point
extérieur de degré d dans chaque copie, voyant éventuellement c,c′ des deux
centres, satisfait

    2d_A+d_B=14−4d−c−c′,     d_Z=2d+c+c′+d_A.

Les apices ne voient aucun centre, et les deux centres ont chacun neuf voisins
extérieurs, tous simples. La somme des c+c′ sur B vaut donc dix-huit, ce qui
donne le tableau en sommant ces identités par classe.

Pour chaque permutation et chaque entier t entre zéro et dix, chaque paire
de profils a un coût de collision connu avec ou sans arête. On affecte les
arêtes disponibles, dans chaque classe du tableau, aux plus grands incréments
de coût. Les arêtes localement forcées ou interdites sont respectées. Ce calcul
par tri est une majoration entière exacte ; ignorer les autres contraintes
du graphe ne peut que l'augmenter.

Le maximum sur toutes les permutations et tous les t vaut **108** pour Q6
et **3612** pour Q8, avec ou sans restriction e(W)≤8. Les 4480 résultats
individuels sont archivés ; aucun solveur flottant n'intervient dans cette étape.

## 6. Reproduction et périmètre restant

    python code/codex/six_three_small_mass_bounds.py
    python code/codex/six_three_mass6_profile_lp.py
    python code/codex/six_three_mass6_profile_lp.py --verify-only
    python code/codex/six_three_mass7_matching_bound.py

Les patrons locaux sont dans `data/codex_six_three_mass6_patterns.json.gz`
et `data/codex_six_three_mass7_patterns.json.gz`. Les certificats finaux sont
`data/codex_six_three_mass6_profile_lp.json` et
`data/codex_six_three_mass7_matching_bound.json`. Le fichier
`data/codex_six_three_small_mass_bounds.json` conserve aussi les majorations
intermédiaires par seules classes de degrés, moins fortes.

Le moteur indépendant LAB du commit `4199134`, importé par `e317a1b`, fournit
le recensement complet à dix sommets : **42430 types, 549 paramètres**.
Il a été régénéré localement en 222 secondes ; `full_order10_crosscheck.py`
retrouve exactement les **3875 formules** du recensement ciblé, coefficient
par coefficient, après conversion des conventions canoniques.
L'archive est `data/codex_lab_full_order10.json.gz`. La génération a employé
`nocheck` : les données d'ordre dix sont des comptes de plongements étiquetés,
et le contrôle de la somme C(99,10) par division de tous les automorphismes
n'a pas été exécuté à cet ordre. Cette limite est inscrite dans les métadonnées.

Ses nombres globaux de représentants
ne peuvent être utilisés comme coefficients thêta avant le traitement des
collisions restantes. Les présentes bornes ferment les composantes internes
de masses six et sept pour la sous-famille choisie ; elles ne ferment pas
encore l'audit entier de `(6,3)` ni le cas du rang 37.
