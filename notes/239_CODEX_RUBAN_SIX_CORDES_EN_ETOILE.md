# 239 — Exploitation de la preuve reçue : les cordes concentrées en un sommet

**Suite reçue au message LAB 476 :** les deux formes résiduelles décrites
ci-dessous sont annoncées exclues par des certificats exacts, commit LAB
589ea52. La note 240 utilise ce résultat attribué, sans audit en double,
et prolonge la réduction aux cordes disjointes ou à un triangle de centres.
Le corps de cette note conserve la portée de notre preuve initiale.

9 octobre 2026. Le texte « C1 — Obstruction arithmétique aux rubans de
longueur six », fourni directement par l'utilisateur, démontre qu'un ruban
fermé à six étapes, sur dix-huit sommets distincts, exige au moins deux
cordes. Nous utilisons ses fonctions propres et son lemme d'annulation au
bord pour contraindre **plusieurs cordes à la fois**, sans reprendre sa
campagne de vérification. Son fichier annoncé `verify_ribbons.py` n'a pas
été fourni ni exécuté ici.

## 1. Conséquence nouvelle dans cette étape

Soit E l'ensemble de toutes les arêtes supplémentaires du sous-graphe
induit sur les dix-huit positions de H_(6,epsilon).

**Théorème.** Si toutes les cordes de E ont un sommet commun u, alors u
est nécessairement un centre. À symétrie du support près, u=c_0 et E est
exactement l'un des deux ensembles suivants :

    {c_0 a_4, c_0 b_3},
    {c_0 c_2, c_0 c_4}.

Ces deux ensembles ne sont que des possibilités nécessaires : aucun
prolongement en SRG n'est affirmé. En particulier, **des cordes toutes
incidentes à un même sommet latéral ne réparent jamais le ruban**, quel
que soit leur nombre. Pour un centre fixé, trois cordes ou davantage
ne peuvent pas être la totalité de la réparation.

Le résultat suppose dix-huit sommets distincts. Il ne force pas la
présence d'un ruban six dans C1 et ne traite pas les cordes réparties
sur plusieurs sommets sans sommet commun.

## 2. Lemme spectral pour une étoile de cordes

Les deux fonctions de la preuve reçue sont

    F(a_i)=F(b_i) :  3, 0,-3,-3, 0, 3
    F(c_i)       :  2,-2,-4,-2, 2, 4
    G(a_i)=G(b_i) :  0,-3,-3, 0, 3, 3
    G(c_i)       : -2,-4,-2, 2, 4, 2.

Elles sont de somme nulle et propres de valeur trois pour les deux
fermetures. Écrire e_v=(F(v),G(v)), T l'ensemble des extrémités autres
que u de l'étoile, et s=Σ_(v∈T)e_v.

Pour toute combinaison h=xF+yG, la perturbation de sa forme quadratique
par les cordes vaut 2 h(u) Σ_(v∈T)h(v). La borne de Rayleigh trois impose

    e_u sᵀ + s e_uᵀ ≤ 0.

Comme e_u n'est jamais nul, cette condition équivaut à

    s = -t e_u,   t≥0.                                  (S)

En effet, dans une base dont le premier vecteur est porté par e_u, la
forme a la matrice [[2a,b],[b,0]]. Être négative semi-définie impose
b=0 et a≤0.

La combinaison h qui s'annule en u satisfait alors Σ_(v∈T)h(v)=0.
La matrice des cordes annule donc h sur chaque sommet : h reste propre
de valeur trois sur tout le support augmenté. Le lemme de prolongement
nul de la preuve reçue impose encore Σ_(N(z)∩H)h=0 à chaque sommet extérieur.

Ainsi l'argument arithmétique ne se limite pas à une corde dont les deux
extrémités portent zéro : pour une étoile, les valeurs aux autres
extrémités peuvent **se compenser**, ce qui conserve la même obstruction.

## 3. Étoile centrée en un sommet latéral

Les symétries du support permettent de prendre u=a_0. Ce ne sont pas
des automorphismes supposés du SRG. Chaque corde doit être possible seule,
puisque ajouter d'autres arêtes ne réduit aucun nombre de voisins communs.
Les seuls voisins supplémentaires possibles de a_0 sont :

| Fermeture | Extrémités possibles |
|---|---|
| 0 | a_3, b_2, b_3, b_4, c_2, c_3 |
| 1 | a_3, a_4, b_2, b_3, c_2, c_3 |

Il y a 63 sous-ensembles non vides pour chaque fermeture. Les budgets
locaux `(A²+A)_uv≤2` en laissent respectivement 12 et 11. La condition (S)
est ici `Σ_T G=0, Σ_T F≤0`. Il reste exactement :

| Fermeture | T |
|---|---|
| 0 | {a_3}, {b_3}, {b_2,b_4}, {a_3,b_2,b_4} |
| 1 | {a_3}, {b_3}, {a_4,b_2} |

La fonction harmonique conservée est G. Les deux singletons sont déjà
exclus par la preuve reçue, modulo trois. Pour les nouveaux cas :

* Si T={b_2,b_4} en fermeture 0 ou T={a_4,b_2} en fermeture 1,
  la paire a_0,c_2 a exactement un voisin commun interne. Un voisin
  commun extérieur est donc obligatoire. Ses autres voisins possibles
  sont contenus dans {a_4,b_4}, dont les valeurs de G sont 3,3. Or
  G(a_0)+G(c_2)=-2. L'annulation donnerait -2+3k=0, impossible.
* Si T={a_3,b_2,b_4} en fermeture 0, prendre la paire a_1,c_3.
  Elle n'a aucun voisin commun interne. Les autres voisins possibles
  d'un voisin commun extérieur sont contenus dans {a_5,b_0,b_5,c_5},
  de valeurs G égales à 3,0,3,2. La somme initiale vaut -1 ; aucune
  somme de ces valeurs n'est égale à 1.

Toutes les étoiles de cordes centrées sur un sommet latéral sont exclues.

## 4. Étoile centrée en un centre

Prendre u=c_0. Pour les deux fermetures, les extrémités possibles sont

    {a_3,a_4,b_3,b_4,c_2,c_3,c_4}.

Sur les 127 sous-ensembles non vides, 14 respectent les budgets locaux.
La condition (S) laisse exactement

    {c_3}, {a_4,b_3}, {a_3,b_4}, {c_2,c_4}.

La fonction conservée est Q=(F+G)/3. Le singleton {c_3} est exclu par
la contradiction de parité de la preuve reçue. Les deux ensembles
mixtes s'échangent par l'échange global a↔b. Cela laisse les deux formes
du théorème. Aucune exclusion supplémentaire n'est annoncée pour elles.

## 5. Certificat exact et portée pratique

Le programme `code/codex/ribbon_six_star.py` utilise uniquement des entiers
et la bibliothèque standard Python. Il couvre les quatre cas
fermeture/type du sommet commun, applique les budgets locaux et la forme
2×2, puis construit les contradictions de sommes au bord. Il écrit
`data/codex_ribbon_six_star.json`.

Pour borner les autres voisins possibles d'un sommet extérieur adjacent
à u,v, le programme garde un sommet w seulement si les trois adjacences
simultanées satisfont tous les budgets `bA≤2·1-b` et toutes les paires
saturées. Les contraintes entre plusieurs w sont ensuite oubliées : les
listes de sommes sont donc des sur-ensembles, ce qui rend leur impossibilité
concluante sans classer les masques extérieurs complets.

    python code/codex/ribbon_six_star.py

Cette exploitation renforce la condition « au moins deux cordes » par
une restriction de leur implantation. Pour chaque sommet latéral u d'un
ruban six injectif, il faut désormais une corde non incidente à u :

    Σ_(vw corde potentielle, u∉{v,w}) A_vw ≥ 1.

C'est une contrainte conditionnelle au ruban présent. Elle complète la
note 238, qui donne une restriction obligatoire sur chaque fenêtre de
huit centres et traite aussi les répétitions de sommets dans le déroulé.
Ni ces conditions ni la preuve reçue ne ferment C1 à elles seules.
