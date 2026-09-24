# 91 — Décortiquer le problème : la hiérarchie exacte d'ordre 8 et le « mur L16 » (2026-09-24, nuit)

*Consigne de l'utilisateur : « décortique le problème, pose-toi des questions, utilise du calcul s'il le faut ».*

## 0. Les questions, et ce qu'elles imposent
- **Que faut-il ?** Une contradiction, donc une quantité avec deux contraintes incompatibles.
- **Qu'est-ce qui a déjà tué des configurations ?** Seulement des équations exactes (SAT local, variance de
  Lou–Murin). Tout ce qui est moyenne, positivité ou genre passe.
- **Pourquoi ?** La torsion forte ressemble à du hasard, et le hasard satisfait les moyennes. Tous les résultats
  connus (frontière SAT, L12/L13, Lou–Murin, L16) poussent vers *plus* de désordre ; aucun ne pénalise le désordre.
- **Qu'est-ce qui « voit » n = 99 ?** (i) les comptages globaux (termes n − m), (ii) la géométrie euclidienne
  (dimension 44, noyau 28/−8/1, orthogonalité), (iii) l'intégralité. L16 a mordu parce qu'il combine (i) et (ii).
- **Donc que tenter ?** Pousser (i) + (ii) + (iii) aussi loin que le calcul le permet : tous les comptages exacts
  jusqu'à 8 sommets, avec toutes les positivités raisonnables. C'est le prolongement naturel de Reimbayev (ordres
  6, 7 à la main) et de L16 (degré 3).

## 1. Machinerie (tout validé)
- **Équations exactes de comptage** (`code/subgraph_lp.py`) : pour tout sous-graphe induit F et U ⊆ V(F), |U| ≤ 2,
  le nombre de sommets extérieurs adjacents à tout U est fixé (n − m, k − deg, λ/μ − communs). Contrôle : 0 violation
  sur srg(9,4,1,2), Petersen, Paley(13), Clebsch (comptages exacts).
- **Résolution exacte en rationnels** (`exact_system.py`, `exact_region.py`) : ordre 6 → 99 variables, rang 98, une
  variable libre ; **ordre 7 → 208 types (le nombre de Reimbayev), deux variables libres = 3P et S/2 exactement**
  (L18), polygone 0 ≤ P ≤ 1386, 0 ≤ S ≤ n₃. Remarque : HiGHS en flottants déclarait le système « infaisable »
  (artefact d'échelle, résidu 1e-4 sur des nombres ~1e9) ; le calcul exact montre qu'il est cohérent.
- **Ordre 8** : 916 types admissibles ; équations 7 → 8 (`order8_region.py`).
- **Positivité euclidienne** (`euclid_gram.py`) : pour des configurations B d'au plus 4 points et des tenseurs
  symétriques de degré d (avec « témoins »), la matrice de Gram des sommes de tenseurs est positive, et chaque entrée
  est une combinaison exacte des comptages d'ordre ≤ 8. Variantes : noyaux E₋₄ (28, −8, 1) et E₃ (42, 9, −2),
  projection harmonique (sans trace), version enracinée (Σ_x des Gram locaux, entrées d'ordre ≤ 7). **Contrôle :
  calcul direct avec les vrais vecteurs propres de srg(9) et de Petersen, erreur relative ~1e-15 pour toutes les
  variantes.**
- **Positivité de drapeaux** (`flag_sdp.py`, Razborov en comptages exacts) : pour chaque type σ ≤ 6 sommets,
  Σ_copies x·xᵀ ⪰ 0 (profils d'extension). Contrôle : erreur 0 sur srg(9) et Petersen.
- **Contrôle global sur BvLS** (qui existe) : le même SDP y admet P ∈ [0, 8910], et BvLS a P = 8910.

## 2. Résultats pour srg(99,14,1,2)
| relaxation (comptages exacts jusqu'à 8 sommets) | P admissible | S admissible |
|---|---|---|
| programme linéaire d'ordre 7 (= Reimbayev) | [0, 1386] | [0, n₃] |
| programme linéaire d'ordre 8 | [0, 1386] | [0, n₃] |
| + positivité de drapeaux (99 blocs, types ≤ 6) | [0, 1386] | [0, 4158] |
| + Gram euclidien degré 4 (Sym⁴, bases ≤ 4 points) | [0, 1386] | — |
| + Gram euclidien degré 2 (E₋₄, E₋₄ + E₃) | [0, 1386] | [0, 4158] |
| + Gram euclidien degré 3 à témoins, E₃ seul | [0, 1386] | [0, 4158] |
| + Gram euclidien degré 3 à témoins, E₋₄ (ou E₋₄ + E₃) | **[0, 1151,08]** | [0, 4158] |
| enraciné : degré 3 (harmonique ou non), degré 2 harmonique | **P ≤ 1151,08** | tout S |
| enraciné : degré 1 (E₋₄) ; enraciné noyau E₃ (degrés 1 à 3) | [0, 1386] | tout S |
| intégralité à l'ordre 7 | P et S/2 entiers, rien d'autre | |

## 3. Le « mur L16 »
Trois familles de positivité indépendantes (degré 3 global, degré 3 enraciné, **degré 2 harmonique enraciné**)
butent exactement sur la même valeur P = 1151,08, celle de L16 (points + droites au degré 3). Aucune combinaison
des informations d'ordre ≤ 8 ne fait mieux, et aucune ne fournit de borne inférieure sur P ni de contrainte sur S.
**Conclusion rigoureuse (au niveau de ces relaxations) : l'information locale jusqu'à 8 points, même combinée à
toute la positivité spectrale et combinatoire naturelle, est entièrement contenue dans L16 et L18.** Si Γ n'existe
pas, la contradiction est invisible à cet ordre : elle est globale (fermeture en diamètre 2 avec exactement
99 sommets), ou d'ordre bien plus élevé.

## 4. Ce que cela dit de la suite
- Améliorer L16 vers le bas ne suffirait pas : une contradiction demande soit P < 0 (même la torsion maximale
  interdite, or P = 0 est confortablement positif), soit une borne inférieure sur P (un plafond de torsion), et
  rien d'accessible ne pénalise le désordre.
- Pistes qui restent : (a) ordre 9–10 (la configuration interdite de Lou–Murin a 9 sommets, mais leur argument est
  « copie par copie », avec de l'intégralité ; une relaxation agrégée risque de ne pas la voir) ; (b) une idée
  globale (revêtement, rigidité, arithmétique fine du réseau des droites via les formes modulaires) ; (c) la
  recherche exhaustive, hors de portée du portable.
