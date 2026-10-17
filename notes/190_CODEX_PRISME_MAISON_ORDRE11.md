# 190 — Test exact du motif prisme + maison éloignée à l'ordre onze

8 octobre 2026. Cible proposée par LAB au message 240 ; fermeture calculée
indépendamment par Codex et LAB (message 242). Certificat et point
rationnels ci-dessous : Codex.

**Résultat du test.** La fermeture triangulaire de ce motif ne comprend
que **44 types**, dont **32 nouveaux paramètres** de degré minimal trois.
Même avec les 1932 inégalités d'extension marquée visibles depuis cette
fermeture, la relaxation donne exactement

\[
 N(\text{prisme + maison éloignée})\le\frac{712800}{29}.
\]

Le majorant ainsi obtenu pour les paires de prismes jumeaux est

\[
 \tau\le\frac{59400}{29}=2048{,}275\ldots,
\]

donc 2048 après arrondi entier. Il est **moins fort que la borne déjà
démontrée τ≤1890** (note 185). Ce test ne remplace donc pas la borne actuelle.

## 1. Pourquoi douze fois le nombre de paires est majoré par ce comptage

Une paire de prismes jumeaux consiste en deux prismes disjoints et sans
arête entre eux. En retirant un sommet quelconque de leur union, on
obtient un prisme et une maison éloignée. Les douze retraits donnent
douze sous-ensembles distincts.

Réciproquement, une copie de ce motif à onze sommets permet au plus une
complétion en deux prismes. La maison possède une unique arête joignant
deux sommets de degré deux ; son troisième voisin commun, unique puisque
λ=1, est nécessairement le sommet manquant du second prisme. Cela prouve
l'injection des retraits dans les copies du motif, soit

\[
 12\tau\le N(\text{prisme + maison éloignée}).
\]

## 2. Fermeture et inégalités utilisées

Pour chaque graphe rencontré ayant un sommet de degré au plus deux, le
nombre de plongements induits est exprimé par le budget d'extension de
son graphe privé de ce sommet, moins les extensions où le nouveau sommet
a des voisins supplémentaires. Les budgets sont 99−10, 14−d, ou
λ/μ moins le nombre de voisins communs déjà présents.

Ces identités engendrent 44 types à onze sommets : 32 sont laissés comme
paramètres de degré minimal trois, les douze autres ont une équation de
récurrence. Toutes les équations ont été contrôlées en fractions exactes.

Le programme ajoute la positivité de tous les comptages de LAB aux ordres
six à dix, la positivité des 44 comptages nouveaux, ainsi que 1932
inégalités obtenues en ne conservant que ces types dans les identités
d'extension marquée. Les types omis ont des comptages non négatifs : on
obtient bien des inégalités valides, sans supposer leur absence.

La maximisation a fourni un certificat de 144 poids rationnels non
négatifs. Un point rationnel atteignant 712800/29 est également archivé
et vérifié contre toutes les contraintes. Ce maximum est donc exact
pour cette relaxation précise ; le point ne prétend pas décrire un
graphe réel ni des comptages entiers.

## 3. Pourquoi la cible directe à douze sommets ne suffit pas

L'union de deux prismes éloignés est déjà de degré minimal trois.
La récurrence triangulaire s'arrête donc immédiatement : elle en fait
un nouveau paramètre libre, dont la seule positivité ne fournit aucun
majorant. Sa fermeture propre a un seul type, mais d'autres relations
sont nécessaires pour le contrôler.

Le présent calcul ne ferme pas les approches d'ordre onze ou douze en
général. Il montre seulement que le majorant global fourni par cette
cible et ces inégalités ne bat pas le majorant déjà disponible.

## 4. Reproduction

```text
python code/codex/prism_house_order11.py
python code/codex/prism_house_order11_bound.py --verify-only
```

La première commande reconstruit la fermeture, vérifie ses équations et
les douze retraits d'une paire de prismes, puis reconstruit les inégalités
d'extension marquée. La seconde vérifie le certificat et le point
rationnels sans solveur d'optimisation. Retirer `--verify-only` pour
redécouvrir le certificat.

Archives : `data/codex_prism_house_order11.json.gz` et
`data/codex_prism_house_order11_bound.json`.
