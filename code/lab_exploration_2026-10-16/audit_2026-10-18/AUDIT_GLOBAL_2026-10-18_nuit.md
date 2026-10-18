# Audit global de C1, 18/10/2026 vers 21 h 15 (LAB)

Demande de l'utilisateur : « fais moi un audit global quand tu peux ».

Statuts employés :
- **démontré** : preuve écrite et relue ;
- **certificat** : objet entier vérifiable sans solveur ;
- **verdict** : sortie de CP-SAT ou de HiGHS, sans certificat portable ;
- **mesure** : échantillon ou estimation.

## 1. Le cadre et ses bases

- **Méthode.** On travaille à une racine de budget x. Les 7 droites et les 21 rectangles en x donnent un gabarit : le graphe J
  des rectangles non grille, et les partitions en blocs à chaque racine. c est le minimum, sur les 7 droites, du nombre de
  composantes de G_l. Il y a trois branches : c ≥ 4, c = 3 et c ≤ 2.
- **P ≤ 852 et racine de budget** (τ ≤ 51, donc k ≤ 12) : revérifié ce matin (`audit_2026-10-18/census/`).
- **Faits de modèle** (AUDIT_EXCLUSIONS_2026-10-18.md §3), relus par le LAB le 17 et le 18/10 :
  - TBᵀ = 0, T² = 7T et les formules de R ;
  - Tσ = 0 sur chaque composante, d'où les équations de composante ;
  - E3, démontré par Codex et relu par le LAB ;
  - les coupes de connexité.
- **Recensements.**
  - c ≥ 3 : 510 926 gabarits, deux énumérateurs indépendants identiques.
  - c = 1 (k ≥ 1) : 4 708 882 classes à S7 près, identiques entre std et la (comparaison exacte).
  - c = 2 (k ≥ 1) : 338 millions de lignes brutes produites par les deux énumérateurs. **La comparaison std/la n'est pas
    faite.**
  - **k = 0 (J = K7) : non recensé.** Le balayage c21sweep s'est arrêté avec 6 tâches k = 0 finies sur 142.

## 2. Branche c ≥ 4 (Codex)

- Fermée par CP-SAT (commit ecb50673) : c'est un **verdict**, sans certificat portable.
- Le LAB n'en a fait aucune vérification indépendante : la tentative passait par le modèle bogué (domain[-1]).
- Nouveau ce soir (zscan1, méthode de comptage de Codex, sans Gram ni budget), sur un échantillon de 200 gabarits c ≥ 4 :
  164 certificats entiers, 3 verdicts CP, 33 UNKNOWN. C'est une confirmation partielle par une autre méthode, mais
  toujours avec le code de Codex.

## 3. Branche c = 3 (LAB)

**Test de Gram V3** : CP-SAT et HiGHS sont d'accord sur 510 946 gabarits (0 désaccord) et en excluent 500 874 (**verdict**).
Il en reste 10 052.

**Registre des 10 052** (`c3_ledger.py`) : 7 998 exclus, **2 054 ouverts**.

| Méthode | Gabarits | Statut |
|---|---:|---|
| P1 (étoile complète, modèle exact de Codex 156fda14) | 3 574 | verdict |
| P2 (couverture de Gram + table) | 1 232 | verdict |
| ZC (plan de comptage de Codex, zscan1) | 7 361 sur les 10 052 | **certificat** (Farkas entier) |
| ZCP (même run, infaisable en CP) | 392 sur les 10 052 | verdict |
| MOM, P3, GC (noyau dur) | 11 | MOM : deux implémentations + certificats de Codex |

- 4 566 gabarits sont exclus par deux méthodes indépendantes (P1 ou P2, plus ZC).
- **Points faibles :**
  - 6 exclusions ne reposent que sur une couverture P2 non confirmée par l'énumérateur de Codex : gz 155, 1138, 2253, 5928,
    5989 et 7914. Les 4 autres de cette liste ont un certificat ZC. La tâche de nettoyage (contre-vérification en 3 600 s) est
    prête mais pas lancée.
  - Environ 80 gabarits ont des couvertures géantes et aucune méthode ne les traite.
- **En cours :** c3ga (2ᵉ passe, 4 162 tâches sur 5 988) et c3gs (3ᵉ passe, 263 sur 3 964). 2 097 des tâches c3ga encore en
  attente portent sur des gabarits déjà exclus : elles ne font plus que confirmer.

## 4. Branche c ≤ 2 (LAB), travail de la soirée

**Démontré : le lemme FG (grille forcée).** Les lignes h sont des pondérations à somme nulle du graphe des blocs Ĵ. Si
aucune marche alternée ne passe par un rectangle non grille q, alors q serait une grille.
- Le test est un parcours exhaustif, sans solveur.
- **Donnée :** sur tout le recensement c = 1 (k ≥ 1), il tue 2 406 345 classes sur 4 708 882 (51,1 %). Il en reste 2 302 537.

**Verdicts : R1, plan global du premier ordre.** C'est la symétrie de R plus E3 et les histogrammes de coins, sans aucun
produit.
- Il tue environ 64 % des survivants de FG (tirage de 300 classes c = 1, k = 1, **mesure**).
- Un exemple a été lu à la main (gabarit 391).

**Certificats : le PL de Codex étendu à toute dimension.** C'est mon catalogue de lignes par parcours en profondeur (identique
à celui de Codex là où les deux tournent) plus `linear_system` et `find_certificate` de Codex, inchangés.
- Il exclut environ 67 % des survivants de R1 (**mesure** sur 100).

**En cours : run glob1** (Spot, Ohio, 92 workers) :
- FG et clés S7 sur tout c = 2 ;
- R1 puis PL sur les 2 302 537 survivants FG de c = 1.

**Le noyau dur.**
- Sur l'échantillon uniforme de 419, il reste 74 gabarits après toutes les méthodes de comptage (c = 2 : aucun pour k ≤ 4).
- Ces survivants passent aussi le Gram V3 (70 sur 74). Le modèle JOINT de Codex (adjacence avec lettres) reste UNKNOWN à
  110 s.
- **Mesure :** estimation grossière d'environ 5 % du recensement c = 1 après le PL. **Aucune méthode ne les traite à cette
  échelle.**

**Nouveau fait, au niveau des lettres (démontré, et contrôlé sur un graphe réel).**
- Énoncé : soit K une composante de G_{l_a}. Le vecteur d^K des déséquilibres de lettres (voisines dans K adjacentes à a*,
  moins celles adjacentes à a′), porté par les 60 étiquettes hors de la droite a, vérifie A[D_a] d^K = −d^K.
- Il porte aussi des sommes de bord imposées et une matrice de Gram fixée : 8(6 diag(p) − ppᵀ).
- Preuve : il découle de T² = 7T et du vecteur propre −4 associé à f_K − (|P|/6) f_a ∈ ker B. Elle vaut pour tout srg(v,k,1,2).
- **Contrôle positif :** exact sur les 423 composantes testées d'un vrai srg(243,22,1,2), sans aucun échec.
- Il n'est pas encore utilisé pour exclure quoi que ce soit.

## 5. Erreurs et rétractations du jour

- **Modèle sans Gram (GFM).** Bug `domain[-1]` d'OR-Tools 9.15, trouvé par un contrôle positif CP sur srg(243). Tous ses
  verdicts sont nuls ; aucun n'avait été compté (commit ae27601).
- **Instances à la demande** lancées contre la règle « Spot uniquement » (12 machines). C'est corrigé : le lanceur refuse
  désormais tout ce qui n'est pas Spot, et une règle est inscrite en mémoire.
- **Erreur de lecture de ma part** sur le certificat 391 (une composante mal lue). Elle a été corrigée avant toute
  conclusion : le certificat de Codex est juste.
- Aucune exclusion comptée n'a été trouvée fausse.

## 6. Ce qui manque pour fermer C1

1. **c ≤ 2 n'est même pas entièrement énuméré.** k = 0 reste à recenser, et la comparaison c = 2 std/la reste à faire.
2. **Le noyau dur c ≤ 2 compatible avec le comptage.** Plusieurs centaines de milliers de classes probables : il faut un
   niveau « lettres » (le fait du §4 en est le premier élément) ou une autre idée.
3. **c = 3 :** 2 054 ouverts, environ 80 couvertures géantes, 6 exclusions P2 à reconfirmer.
4. **Portabilité.** La plupart des exclusions sont des verdicts CP-SAT : V3, P1, P2, R1, et la fermeture c ≥ 4 de Codex. Seuls
   FG (preuve) et les certificats de Farkas (ZC, PL étendu) sont vérifiables sans solveur.
5. **c ≥ 4 :** aucune vérification indépendante par le LAB.

**Verdict : C1 n'est pas fermé.**
- Branche c ≥ 4 : déclarée fermée par verdict.
- Branche c = 3 : 98 % du recensement est exclu (Gram), et 80 % des 10 052 restants.
- Branche c ≤ 2 : la moitié du recensement c = 1 est tuée par un lemme démontré, et le reste est en cours.
