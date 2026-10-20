# VERIF R1-05 — « plafond de torsion » : de P ≥ 1152 à P ≥ 853

Vérificateur adverse, contexte neuf, 20/10/2026. Lecture seule. Script : `check_misc.py` (scratchpad de la session),
arithmétique exacte.

## Verdict : DÉJÀ CONNUE (logique correcte, avec une réserve de formulation)

- **La logique tient.** Depuis P ≤ 852, toute minoration P ≥ 853 suffit à exclure le graphe. Le seuil qu'un mécanisme
  de « plafond de torsion » doit atteindre descend donc de 1152 à 853.
- **Les équivalences sont justes.** Il en manque une, ajoutée au §2 : H ≤ 210 885.
- **Réserve de formulation.** « Impossible tel qu'énoncé » ne veut pas dire « improuvable ». Cela veut dire :
  incompatible avec P ≤ 852 dans un graphe hypothétique.
  - Énoncés pour tout srg(99,14,1,2), « P ≥ 1152 » et « P ≥ 853 » sont tous deux équivalents à la non-existence, compte
    tenu de P ≤ 852.
  - Seule change la cible quantitative d'une méthode de minoration de P.
  - Les conditionnels de septembre (« si P ≥ 1152, contradiction avec L16 ») restent vrais. Ils sont seulement dépassés.
- **Déjà connu.** C'est implicite depuis le 08/10 et explicite le 15/10 (§4).

## 1. Énoncés exacts

- **`conway99-c1`, `origin/main:notes/100_SYNTHESE_DES_LEMMES.md` :**
  - l. 39 : « il manque un plafond (P ≥ 1152) » ;
  - l. 174 : « L15 | P = 1386 − Σ|W|/6 » ;
  - l. 175 : « L16 | P ≤ 1151, c'est-à-dire Σ|W| ≥ 1410 » ;
  - l. 187 : « Aucune ligne n'est un plafond de torsion (une borne inférieure sur P) ».
- **`notes/123_PORTE_IX_TORSION_MAXIMALE.md` :**
  - l. 27 : « H = 213 444 − 3P » (hexagones induits ; Reimbayev) ;
  - l. 29 : « Le plafond visé par notes/100 (P ≥ 1152) équivaut donc à H ≤ 209 988 ».
- **Note 182:5 et 182:135** (`origin/codex/c1-arithmetic-audit`, 08/10) : « P ≤ 11088/13, donc P≤852 ». Le certificat
  entier est à 182:137-145.
- **Statut de P ≤ 852** (CARTE §8.1) : C relativement au recensement d'ordre 9. Le recensement lui-même est E, en double
  implantation (Codex et `census2.py`), avec 6 533 formules concordantes.

## 2. Équivalences recalculées

Les identités utilisées sont n₃ = 4158 − 3P (le nombre de N3, toujours un multiple de 3), L15 et H = 213 444 − 3P.

| seuil | n₃ | Σ_x\|W(x)\| | H |
|---|---|---|---|
| P ≤ 1151 (L16) | ≥ 705 | ≥ 1410 | ≥ 209 991 |
| **P ≥ 1152** (plafond de septembre) | ≤ 702, donc « ≤ 704 » | ≤ 1404, donc « ≤ 1409 » | ≤ 209 988 |
| P ≤ 852 (C) | ≥ 1602 | ≥ 3204 | ≥ 210 888 |
| **P ≥ 853** (nouvelle cible) | ≤ 1599 | ≤ 3198 | **≤ 210 885** (absent de R1) |

- **Pourquoi « n₃ ≤ 704 » équivaut à « P ≥ 1152 » :** n₃ est un multiple de 3.
- **Pourquoi « Σ|W| ≤ 1409 » équivaut à « P ≥ 1152 » :** Σ|W| = 6(1386 − P) est un multiple de 6.
- **Les formulations de L09-COND-036, -037 et -087 sont donc cohérentes**, avec n₃ = 4158 − 3P.
- **Piège I9 de R1.** « n₃ » a trois sens. Ici c'est bien 4158 − 3P = −χ(Σ), voir C6 en 100_SYNTHESE:204. La grandeur
  χ(Σ) = 3P − 4158 ≤ −705 est cohérente avec L16.

## 3. Chaîne réécrite

1. **(L15, P, septembre.)** P = 1386 − Σ|W|/6. **(Note 123, P.)** H = 213 444 − 3P.
2. **(Note 182, C relativement au recensement E.)** P ≤ 852.
3. **Logique.** Si une méthode prouve P ≥ p₀ avec p₀ ≥ 853, il n'existe pas de Conway. L'ancienne exigence p₀ ≥ 1152,
   qui venait de L16, est remplacée par p₀ ≥ 853.
4. **Statut de la réduction : C**, celui de P ≤ 852.

## 4. Redécouverte

- **08/10.** Dès P ≤ 852 (note 182), le seuil utile est 853. C'est implicite.
- **15/10.** `work/stars_rank_2026-10-14/THREE_RESULTS_2026-10-15.md:47-49` : « A CEILING is still required [...]
  (T8)/(T15) (AUDIT O3) is a much weaker ceiling that also suffices together with P <= 852 ».
  - Le même jour, deux plafonds de ce type sont utilisés exactement contre 852 :
    - P ≥ 866,25 (l. 61) ;
    - P ≥ 924 (l. 102).
  - Ce sont les chaînes R1-06 et R1-07.
- **16/10.** La REVUE_GLOBALE le reprend.
- R1 déclare lui-même « deja_connue : oui ».

## 5. Ce qui manquerait

- **Mécanisme.** Il manque toujours un mécanisme de minoration de P, aussi faible soit-il au-dessus de 852. Aucun n'est
  connu (100_SYNTHESE:187, CARTE §4).
- **Statut.** Pour passer à P, il faudrait dériver à la main les 16 identités du certificat de P ≤ 852 (CARTE §8.1).
- **Fiches.** Il faut corriger le mot « réfutée » appliqué aux énoncés de septembre (R1 l. 963-964, 1014). Il vaudrait
  mieux écrire « dépassée : hypothèse incompatible avec P ≤ 852 ; cible ramenée à P ≥ 853 ». Un conditionnel dont
  l'hypothèse est impossible n'est pas réfuté.
