# Carte maîtresse du travail sur le graphe de Conway srg(99,14,1,2), du 21/09 au 20/10/2026

**État : ÉBAUCHE en cours d'assemblage (20/10 au soir).** Les sections marquées « à remplir » attendent les lots L09
et L11 (messages du pont), la recombinaison (R1 à R3) et sa vérification adverse.

Chaque affirmation renvoie à une fiche (`fiches/<lot>.jsonl`, identifiant `Lxx-NN`) ou à une source. Les fiches renvoient
elles-mêmes aux sources d'origine. Les statuts suivent `CONSIGNES_AGENTS.md` :
- **P** : preuve écrite ;
- **C** : calcul exact certifié ;
- **E** : calcul exact sans certificat exporté ;
- **S** : verdict de solveur ;
- **H** : heuristique ;
- **O** : ouvert ;
- **R** : réfuté ;
- **X** : retiré.

**Aucune preuve de ce dossier n'a été relue par un humain**, sauf une lecture partielle de C3 par Cesarz–Woldar.

---

## 0. Démarrer ici (à remplir en dernier)

---

## 1. Le problème, les conventions et les faits de base

Les dérivations de cette section sont courtes ; elles sont refaites ici pour qu'on n'ait pas à les rechercher.

**1.1 Équation.** Γ est un srg(99,14,1,2) hypothétique, de matrice d'adjacence A. Alors A² = 14I + A + 2(J − I − A), donc
**A² = 12I − A + 2J**.

**1.2 Spectre.**
- Les valeurs propres non triviales sont les racines de x² + x − 12 = 0, soit 3 et −4.
- Leurs multiplicités vérifient f + g = 98 et 14 + 3f − 4g = 0, d'où **14 (×1), 3 (×54), −4 (×44)**.
- Projecteurs :
  - E₋ = (3I − A + J/9)/7, de rang 44 ;
  - E₃ = (A + 4I)/7 − (2/77)J, de rang 54 ;
  - E₃ + E₋ + J/99 = I. La vérification sur 1 passe par −18 + 11 + 7 = 0 (sur 693).

**1.3 Configuration de vecteurs.**
- La matrice 63·E₋ = 27I − 9A + J est un Gram entier de rang 44 : 28 sur la diagonale, −8 sur une arête, 1 sur une
  non-arête.
- Les vecteurs w_v = √7·E₋e_v vérifient 4w_x + Σ_{y∼x} w_y = 0 pour tout x, car E₋(A + 4I) = 0, ainsi que Σ_v w_v = 0.
- Un ensemble S de sommets dont les w_v sont indépendants est un « bord positif » : 3I − B_S + J/9 > 0, où B_S est
  l'adjacence induite. On a |S| ≤ 44 (théorème V15 de Codex, L05-108, L07-443).

**1.4 Cadre d'un sommet** (preuve complète).
- λ = 1 : N(x) induit un couplage parfait 7K2.
- Un sommet lointain y (y ≁ x) a μ = 2 voisins a, b dans N(x), et a ≁ b. Sinon a et b auraient deux voisins communs,
  x et y.
- Réciproquement, une non-arête {a, b} de N(x) a un second voisin commun z ≠ x, et z ∉ N(x) : sinon z serait le
  partenaire de a et celui de b dans le couplage.
- Les 84 sommets lointains sont donc en bijection avec les 84 = C(14,2) − 7 non-arêtes de N(x).
- La structure (x, N(x), sommets lointains avec leur adjacence vers N(x)) est unique à isomorphisme près, et
  **Aut(cadre) = 2⁷·7! = 645 120**.
- Une complétion est un graphe sur les 84 sommets lointains : chacun y a 12 voisins.
- **Principe de symétrie forcée** (L07-032, L10-052) : si Aut(Γ) = 1, les 645 120 réétiquetages du cadre donnent des
  complétions étiquetées toutes distinctes.

**1.5 Droites.**
- λ = 1 : chaque arête est dans un seul triangle, ce qui donne 99·14/6 = **231 droites**.
- Pour une droite T, on a la partition 3 + 36 + 60.
- Les 36 voisins de T sont distincts, sinon une arête de T aurait deux voisins communs.
- Le graphe G_T induit sur ces 36 sommets est **cubique**. Un voisin u de a ∈ T y a exactement trois voisins :
  - son partenaire dans le triangle de l'arête au ;
  - un voisin du côté de b, second voisin commun de u et b ;
  - un voisin du côté de c.
- Notations : c(T) est le nombre de composantes de G_T, et t(T) le nombre de triangles transversaux.
- Un prisme triangulaire est automatiquement induit, et Σ_T t(T) = 2P, où P est le nombre de prismes
  (`exploration_2026-10-16/merge_2026-10-19/THEOREME_REDUCTION_R37.md`, Lemme 2.1, P).

**1.6 Rangs et dictionnaire avec le dépôt externe.**
- L'équipe note **r = rang_7(A − 3I)**. Le dépôt externe conway-99-research note r_ext = rang_F7(2A − J + I).
- **Proposition (P, faite ici le 20/10) : r = r_ext + 1.** Elle était au statut H (L03a-103).
  - Posons N = A − 3I. Modulo 7, on a 2A − J + I ≡ 2N − 11ᵀ.
  - Comme N1 = 11·1 ≡ 4·1, on peut écrire 2N − 11ᵀ = 2N(I − 11ᵀ), car 8 ≡ 1.
  - Le projecteur Π = I − 11ᵀ vérifie Π² = I + 97·11ᵀ ≡ Π. C'est donc un projecteur, de noyau ⟨1⟩ (car 98 ≡ 0) et
    d'image 1^⊥, si bien que r_ext = dim N(1^⊥).
  - De plus 1 ∈ im N (1 = N(2·1)), et ker N = (im N)^⊥ ⊆ 1^⊥. Le vecteur 1 ∉ N(1^⊥) : une solution de Nv = 1 s'écrit
    v = 2·1 + k avec k ∈ ker N, et 1ᵀv ≡ 2 + 0 ≠ 0.
  - Comme im N = N(1^⊥) + ⟨1⟩, on conclut rang N = dim N(1^⊥) + 1. ∎
  - Contrôle : sur des matrices symétriques aléatoires de F7^{99×99} avec N1 = 4·1, on a bien
    rang(2N − J) = rang N − 1 (4 essais).
- **Conséquences.**
  - La parité externe (W66 : r_ext pair dans {28, …, 42}) donne r impair dans {29, …, 43}.
  - Les résultats externes « au rang 28 » portent sur r = 29, donc hors de la fenêtre actuelle.
- **Fenêtre de l'équipe : r ∈ {37, 39, 41, 43}** (C, programme thêta de niveau 7, audité par Codex ; L06-023, L06-024).

**1.7 Symétries.**
- La littérature donne |Aut| ∈ {1, 2, 3} (L01-01, L03a-16).
- C3 est fermé : P et formalisation Lean 4 complète, C (L04).
- C7 est fermé en Lean (L01), C11 par la littérature.
- C2 est fermé par la route C avec réserves (S, avec une composante ouverte ; L02, L01-85).
- **Il reste C1, Aut(Γ) = 1.** Les réserves sont détaillées au §2.

---

## 2. État au 20/10 (à remplir après L09/L11)

## 3. Arbre de ce qui reste à prouver (à remplir)

## 4. Routes fermées : ne pas refaire (à remplir)

## 5. Questions ouvertes classées par levier et par coût (à remplir)

## 6. Les dossiers finis et chiffrés (à remplir)

## 7. Recombinaison : résultats (à remplir après R1 à R3 et la vérification adverse)

## 8. Incohérences de statut à trancher

**8.1 P ≤ 852 : il n'y a pas de désaccord sur les faits, seulement sur l'étiquette.**
- Le certificat est exact : 16 poids ≥ 0 avec Σ w_H N_H = 11088/13 − P identiquement.
- Il a été vérifié sur deux implantations indépendantes du recensement d'ordre 9 (celle de Codex et `census2.py`), sans
  aucun écart sur les 6 533 formules.
- Le recensement lui-même est engendré par programme, sans dérivation lisible.
- Sources : `exploration_2026-10-16/audit_2026-10-18/AUDIT_EXCLUSIONS_2026-10-18.md:226-238` (« pourquoi c'est une
  preuve ») et `THEOREME_REDUCTION_R37.md:157-174, 958`.
- **Étiquette retenue : C relativement au recensement ; recensement E en double implantation.**
- Pour passer à P, il faudrait dériver à la main les identités des 16 types utilisés.

**8.2 L23.**
- « PROUVÉ » (CORE:148), P (SYN:41), « A, non audité » (THM:966).
- Étiquette retenue : P non audité (L08-001, L08-176).
- L23 a été établi trois fois : note Codex 102 (25/09), RD (09/10), TL 17.80.

**8.3 m = 4 exclu.**
- « 79/79 à la racine de budget » (SYN:314) contre « 79/79 à la racine minimisant 9s + 8g ; 76/79 pour une racine de
  budget quelconque (7, 9, 19 non couverts) » (MAND:77).
- Statut S dans tous les cas (CP-SAT).
- Voir L08-055, L08-070, L08-143.

**8.4 Doublons entre lots à statuts différents.** Il y en a 41 paires
(`assemblage/DOUBLONS_PROBABLES.tsv`). Ce sont surtout des écarts E/C, selon que le certificat a été exporté ou non, et
P/H.
- Règle d'assemblage : garder le statut le plus faible, sauf si la fiche plus forte cite un certificat vérifié.
- À trancher une à une (à remplir).

## 9. Chronologie depuis conway99-involution (21/09) (à remplir)

## 10. Règles de travail de l'utilisateur

La liste datée et sourcée est dans `fiches/L10_sessions_memoires.md` §8. Elle sera complétée par les consignes relayées
dans le pont (lots L11). Ajouts et corrections du 20/10 :
- **Le pont LAB <-> Codex peut être lu.** L'utilisateur, le 20/10 : « jai jamais dis que tu pouvais pas tu peux les
  lire ».
  - L'ancienne interdiction d'ouvrir `claude-codex-bridge`, recopiée comme « règle de sécurité constante » dans L10 §8,
    venait de mes propres résumés, pas de l'utilisateur.
  - Seul `state/runtime.json`, qui contient le jeton du pont, ne doit jamais être lu ni copié (README du pont).
- Transfert de méthode = analogie, pas transposition. Il faut dire ce qui diffère entre les objets (utilisateur, 17/10
  et 20/10).
- Puissance de calcul quand le PC est libre, coupure dès qu'un programme s'ouvre ; agents Opus permis (20/10).

## 11. Index des lots et couverture (à compléter)

| lot | contenu | résultats | P | C | E | S | H | O | R | X |
|---|---|---|---|---|---|---|---|---|---|---|
| L01 | origines, C2 (21/09 → 14/10) | 125 | 66 | 13 | 22 | 2 | 4 | 9 | 5 | 4 |
| L02 | campagne C2 sur AWS | 463 | 182 | 23 | 158 | 30 | 17 | 24 | 7 | 22 |
| L03a | session eeaf2d22, dépôt externe (1re moitié) | 112 | 46 | 10 | 9 | 2 | 26 | 10 | 7 | 2 |
| L03b | dépôt externe (2e moitié) | 216 | 93 | 42 | 13 | 4 | 2 | 46 | 14 | 2 |
| L04 | C3 | 37 | 16 | 7 | 3 | 3 | 1 | 4 | 2 | 1 |
| L05 | Codex | 238 | 121 | 60 | 25 | 10 | 6 | 10 | 4 | 2 |
| L06 | arithmétique C1 (LAB) | 182 | 79 | 25 | 34 | 7 | 17 | 7 | 6 | 7 |
| L07 | C1, asymétrie, lois locales | 484 | 253 | 32 | 82 | 35 | 30 | 25 | 19 | 8 |
| L08 | C1, branche exploratoire | 235 | 91 | 10 | 63 | 21 | 16 | 22 | 4 | 8 |
| L09 | structures, Astra, coordination | à venir | | | | | | | | |
| L10 | sessions et mémoires | 127 | 44 | 21 | 26 | 13 | 8 | 6 | 7 | 2 |
| L11a-f | messages du pont (1 277) | à venir | | | | | | | | |

Outils : `tools/` (inventaire, triage, lots, export du pont, extraction, fusion). Inventaire : `inventory/` (6 320
contenus distincts). Sauvegarde du scratchpad : `work/scratchpad_LAB_2026-09-30/` (MANIFEST.csv, 32 archives).
