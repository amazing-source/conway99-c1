# Audit rapide, 18/10/2026 au soir (LAB) — branche c = 3 à la racine de budget

Demande de l'utilisateur : « Refais moi un petit audit rapide aussi ».

## Bases

- P ≤ 852 (racine de budget, k ≤ 12 grilles) : revérifié ce matin (`audit_2026-10-18/census/`).
- Recensement c ≥ 3 : 510 926 gabarits. Les deux énumérateurs indépendants sont identiques.
- Test de Gram (V3, run verif1a + verif1c) : CP-SAT et HiGHS sont d'accord sur 510 946 gabarits, avec **0 désaccord et
  0 inconnu**. Il exclut 500 874 gabarits.

## Registre des 10 052 gabarits ouverts après le Gram (`c3_ledger.py`)

| Méthode | Exclus | Repose sur |
|---|---:|---|
| P1 : étoile complète, 60 s par représentant d'orbite, sans transport (c3oa, c3ob) | 3 574 | modèle exact de Codex (156fda14) ; symétrie des lettres (test d'équivariance + Codex) ; aucune lecture de domaine dans ce chemin (grep) |
| P2 : couverture de Gram complète + table sur toutes les entrées (c3ga, c3gb) | 1 232 | couvertures complètes (assertion) ; 1 222 confirmées par `enumerate_grams` de Codex, toutes les différences étant des violations de la coupe de connexité ; **10 non confirmées** (énumération de Codex inachevée en 300 s) : gz 155, 894, 1138, 2253, 5780, 5928, 5989, 6982, 7027, 7914 |
| Moments par Gram | 2 (5128, 4192) | `moment_bounds.py` (LAB, réécrit de zéro) et `root_component_corner_moment_bounds` (Codex), verdicts identiques Gram par Gram ; certificats entiers de Codex |
| P3 (découpage par Gram) et noyau dur (gc1a, gc2a) | 9 | coins, signatures de Schur (h ∈ im R, hᵀR⁺h ≤ 5/2), CR = 0 |
| **Total** | **4 814** | |

**Reste : 5 238 gabarits non exclus.**
- La 2ᵉ passe n'est pas finie : 4 421 tâches en file.
- 636 gabarits UNKNOWN : 3ᵉ passe c3gs lancée (3 964 tranches). 22 échecs techniques au démarrage
  (NoCredentialsError au téléchargement S3), à relancer.
- Environ 82 gabarits ont des couvertures géantes (plus de 20 000 Gram, ou énumération inachevée), surtout en
  dimension 6. Aucune méthode à ce jour.

## Rétractation du jour

- Modèle sans Gram (`gram_free_moment.py`) : bug `domain[-1]` d'OR-Tools 9.15.
- Tous ses verdicts sont nuls, et aucun n'avait été compté.
- Voir `c3_cost_2026-10-18/C3_GRAM_COVER_2026-10-18.md` et le commit ae27601.

## Autres branches

- **c ≥ 4 (Codex)** : fermé par CP-SAT (commit ecb50673). Pas de certificat portable. Pas de vérification indépendante
  du LAB : la tentative passait par le modèle bogué.
- **c ≤ 2** :
  - recensement c = 1 (k ≥ 1) : 4 708 882 gabarits à S7 près, std = la exactement ;
  - comparaison c = 2 en cours ;
  - k = 0 (K7) non recensé ;
  - **0 exclusion**.

## Conclusion

- Aucune exclusion comptée n'a été trouvée fausse.
- La branche c = 3 n'est pas fermée : 52 % des 10 052 restent à traiter.
- Points à reconfirmer : les 10 couvertures P2 non confirmées par l'énumérateur de Codex.
- Trou de méthode : les couvertures géantes.
