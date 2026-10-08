# 189 — Le recensement d'ordre dix abaisse la borne de Fano à 842

8 octobre 2026. Piste et premier programme exploratoire : LAB, message 240,
commit `6552e44`. Certificat rationnel et reconstruction indépendante des
comptages utilisés : Codex.

**Résultat.** Tout hypothétique srg(99,14,1,2) satisfait

\[
 a_7\le842,
\]

au lieu de la borne 990 de la note 180. Ainsi il contient au plus **421
configurations de Fano non orientées**, contre 495 auparavant. Il s'agit
d'une borne inconditionnelle quant au rang, et non d'une nouvelle exclusion
de rang. Les possibilités restantes sont toujours 37, 39, 41 et 43.

## 1. Un motif à dix sommets détermine une configuration de Fano

Le support d'un vecteur de norme quatorze de L1 est le complément biparti
de l'incidence du plan de Fano : sept points, sept blocs, degré quatre,
deux voisins communs pour chaque paire d'un même côté.

Retirer deux blocs et leurs deux points communs laisse un graphe F10 sur
5+5 sommets, avec seize arêtes et les degrés 3,3,3,3,4 sur chaque côté.
Le dénombrement des sous-ensembles du support confirme les faits suivants :

- il y a exactement 21 copies induites de F10 par configuration de Fano ;
- aucun autre sous-graphe à au plus dix sommets n'a degré minimal trois ;
- F10 est connexe et ses deux sommets de degré quatre contiennent chacun
  une graine complète de Fano.

Une graine complète détermine au plus un vecteur de Fano orienté (note
180, §1). Comme F10 est connexe et biparti, on peut orienter de la même
façon deux prolongements éventuels, qui partageraient alors la même
graine. Ils sont donc identiques. Une copie de F10 appartient ainsi à au
plus une configuration non orientée.

En notant N(F10) le nombre de copies induites, on obtient

\[
 21\,a_7/2\le N(F10).
\]

## 2. Le certificat exact du recensement

La positivité des comptages de graphes induits aux ordres neuf et dix
donne

\[
 N(F10)\le\frac{256410}{29}=8841{,}724\ldots
\]

Le fichier `data/codex_fano_order10_bound.json` contient 169 multiplicateurs
rationnels non négatifs : deux portent sur des graphes à neuf sommets,
167 sur des graphes à dix sommets. Les lignes comptent des plongements
induits étiquetés, donc x_H=|Aut(H)|N(H). Après multiplication par 125280,
le certificat s'écrit exactement

\[
 125280\,N(F10)+\sum_H w_H x_H=1107691200,
 \qquad w_H\in\mathbb Z_{\ge0}.
\]

Le plus grand poids entier est 18180. La liste complète, plutôt qu'une
approximation décimale des multiplicateurs, est archivée dans le fichier.
La vérification annule exactement chacun des 549 coefficients de
paramètres après transfert du terme N(F10).

On en déduit

\[
 a_7\le\frac{2}{21}\frac{256410}{29}
       =\frac{24420}{29}=842{,}068\ldots,
 \qquad a_7\le842.
\]

La recherche du support du certificat emploie un programme linéaire
flottant. La preuve publiée utilise seulement des fractions exactes ;
elle n'a pas besoin d'une solution primale flottante.

## 3. Reconstruction indépendante des lignes effectivement utilisées

Le certificat a été découvert dans le recensement complet de LAB, dont
l'archive locale contient 42430 types d'ordre dix et 549 paramètres.
Les 169 formes affines utilisées ont ensuite été reconstruites avec :

- le recensement d'ordre neuf de Codex ;
- ses propres étiquettes canoniques ;
- sa récurrence triangulaire et son choix de sommet de degré au plus deux.

La fermeture nécessaire ne comprend que 328 types d'ordre dix, dont 189
équations de récurrence et 139 paramètres denses. Toutes les formes
coïncident exactement avec celles utilisées dans le certificat.

Ce contrôle porte sur les lignes de la preuve. Il ne revendique pas la
vérification du total de tous les types d'ordre dix de l'archive générée
avec l'option `nocheck`, ni une formalisation dans un assistant de preuve.

## 4. Effet exact sur la comparaison thêta au rang 37

On conserve les contraintes déjà démontrées de la note 186, notamment
b3≥45528, et on remplace seulement a7≤990 par a7≤842. Les coefficients
thêta sont développés jusqu'à q^84. Les résultats suivants sont des maxima
de la relaxation rationnelle, avec certificats et points rationnels
atteignant ces maxima et vérifiés contre toutes ses contraintes.

| Quantité | Avec a7≤990 | Avec a7≤842 |
|---|---:|---:|
| b4 | 214100073/13 ≈ 16469236,38 | 211010055/13 ≈ 16231542,69 |
| b4+(651/34)b3 | 2366216753/136 ≈ 17398652,60 | 2332890187/136 ≈ 17153604,32 |

La baisse du plafond couplé est exactement 16663283/68, soit environ
245048. Elle réduit l'écart à franchir pour les futures bornes sur les
vecteurs distincts. Aucun comptage brut de représentants n'est assimilé
ici à un comptage de vecteurs distincts. Les nouvelles contraintes sur
les racines proposées par LAP ne sont pas utilisées.

## 5. Reproduction

Depuis la racine du dépôt :

```text
python code/codex/fano_order10_bound.py --verify-only --audit-recurrences
python code/codex/fano_order10_theta_effect.py --verify-only
```

La première commande vérifie le motif F10, les 21 occurrences, le
certificat positif et les récurrences des comptages utilisés, sans
optimisation. La seconde reconstruit les formes thêta et contrôle les
quatre certificats ainsi que leurs points rationnels. Pour redécouvrir
les multiplicateurs, retirer `--verify-only`.

Les données sont dans `data/codex_fano_order10_bound.json` et
`data/codex_fano_order10_theta_effect.json`.
