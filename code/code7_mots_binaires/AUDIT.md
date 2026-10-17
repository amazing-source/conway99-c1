# Corrections ciblées au rapport « Acculer le 99-graphe dans son refuge asymétrique »

Le contrôle porte sur les implications mathématiques et sur la coordination avec le dépôt, non sur une validation exhaustive de toutes les références bibliographiques de 2026.

## Non-unicité, transitivité et asymétrie

Plusieurs réalisations symétriques d'un même ensemble de paramètres réfutent l'unicité, pas une éventuelle symétrie obligatoire. Les valeurs Aut=4320,864,3888 ne réfutent donc pas l'implication « tout SRG(v,k,1,2) a un automorphisme non trivial ».

La table du dépôt donne les orbites [3,60,180], [27,108,108] et [81,162]. Les trois graphes, et pas seulement les deux premiers, sont non sommet-transitifs.

La symétrie peut être forcée sans unicité : dans un graphe de Cayley, les translations préservent les arêtes par construction ; plusieurs graphes de Cayley non isomorphes peuvent avoir les mêmes paramètres. Une preuve générale de symétrie pour une famille n'est donc pas exclue par sa non-unicité.

Les statistiques d'asymétrie de familles connues ne définissent pas une probabilité d'existence pour le paramétrage 99. Elles ne peuvent remplacer un modèle probabiliste explicite.

## WL et comptes de motifs

Le théorème de Dvořák–Dell–Grohe–Rattan porte sur les nombres d'homomorphismes, non sur les nombres de copies induites ou injectives sans qualification. Référence primaire : Dell, Grohe, Rattan, Lovász Meets Weisfeiler and Leman, ICALP 2018, arXiv:1802.08876. Voir aussi Arvind, Fuhlbrück, Köbler, Verbitsky, On Weisfeiler-Leman Invariance: Subgraph Counts and Related Graph Properties, arXiv:1811.04801.

Les graphes des tours 4x4 et de Shrikhande ont les mêmes paramètres (16,6,2,2), donc ne sont pas distingués par 2-WL, mais ont respectivement 36 et 12 C4 induits. Leurs nombres d'homomorphismes depuis C4 sont identiques : 1536. Le vérificateur fourni construit les deux graphes et contrôle tous ces comptes.

De plus, « un invariant ne distingue pas deux réalisations » n'est pas un théorème d'impuissance de cet invariant pour les questions de faisabilité d'autres paramètres.

## Ensemble distinguant ≠ graphe déterminé par son sous-graphe induit

Pour chaque paire u,v, exactement 24 autres sommets distinguent leurs voisinages. Un ensemble S d'au plus 30 sommets permet donc de distinguer tous les sommets après individualisation (la borne se renforce à 24 par échantillonnage sans remise : C(99,2) C(73,24)/C(99,24) < 1).

Mais les profils d'attache vers S font partie des données requises. Le seul graphe induit sur S ne donne ni ces profils, ni les arêtes entre sommets extérieurs. La discrétisation par raffinement ne prouve pas l'unicité d'une complétion.

## Doublons repérés dans le dépôt

Révision consultée : 76fd9a53993163f99c34cdb6430de0101d12a261.

* notes/90_SECONDE_VARIABLE.md et code/reimbayev7.py : les 208 expressions d'ordre 7 sont déjà transcrites et leur non-négativité a déjà été analysée. La note enregistre 2 n3 <= z11 <= 4 n3 et n3 <= 4158, ainsi que z11=4n3-2S. Ces résultats sont cités comme état du dépôt, pas comme une nouvelle validation indépendante de toutes les transcriptions.
* notes/172_RESEAU_Q_ALPHA22.md : l'arithmétique du genre et ses limitations sont déjà documentées. Une nouvelle campagne de déterminants seuls doit préciser son ingrédient supplémentaire.
* notes/173_CONJECTURE_K7.md : connexité de Gamma_c union M_c, rang local 13 et rang résiduel 9 intégrés ; K7 reste ouverte.

## Apport mathématique joint

THEOREME.md prouve la classification des mots binaires du noyau F7 de A+4I : seuls les poids 0,63,77 sont possibles. L'absence d'un mot binaire non nul n'est pas exclue. Ni K7 ni alpha=22 ne sont résolus.

Aucune modification de la branche distante, aucun lancement de solveur, aucun calcul massif.
