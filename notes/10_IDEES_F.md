# 10 — Chercheur F : idées (liste ouverte)

Principe commun : Γ ressemble jusqu'au rayon 2 à la boule de rayon 2 de H(7,3) (1 + 14 + 84 = 99). Les deux graphes
qui existent dans la famille (9 et 243) sont des *quotients de Hamming* (tout quadrangle dans une grille 3×3,
τ = mate partout). 99 ∤ 3⁷, donc Γ doit être **tordu**. Les pistes A/B/C de ChatGPT mesurent toutes cette torsion
(A : cohérence T/Δ = fermeture des grilles ; B : monodromie des τ ; C : défaut de l'action de H_lab sur ker B).
La question centrale devient : **la torsion est-elle compatible avec les contraintes globales ?**

Statut : P = proposée, T = tuée (voir 20_ATTAQUES_R.md), S = survivante, M = mutée.

| # | Idée | Type | Statut |
|---|------|------|--------|
| F1 | Connexion canonique des ombres, holonomie de droite ρ_ℓ ∈ Sym(12), courbure = prismes manquants | B reformulée | P |
| F2 | **Rigidité q = 3** : « localement (t+1)K₂ + μ = 2 ⇒ grid-full ⇒ quotient de H(t+1,3) ». Tuerait 99, 6273, 494019 d'un coup | radicale | P |
| F3 | Ensembles serrés (tight sets) × transitions : les grilles sont serrées, (A − 3I)g = g_tot·1 ; chercher les autres configurations serrées forcées par la torsion | mixte spectral/local | P |
| F4 | **Torsion de Fano / octonions** : τ induit sur les 7 classes de mates une structure ; conjecture « cohérence de classes » ⇒ STS(7) = plan de Fano (7 = t+1 = r−s, seul cas ouvert avec un STS) | très risquée | P |
| F5 | **Genre entier / formule d'oddité** : le réseau Λ₃ = E₃ ∩ Z⁹⁹ est 2-adiquement pair unimodulaire de rang 54 ⇒ contrainte de parité reliant les exposants 3, 7, 11 de son déterminant ; combiner avec le recollement 7-adique local (piste C) | risquée, algébrique | P |
| F6 | Invariant d'Arf mod 2 (A idempotent sur F₂, rang 54 forcé) | risquée | P |
| F7 | Algèbre T/Δ (piste A) : points W(C,·) de chaque quadrangle ; cohérence ⟺ grille | A | P |
| F8 | Réseau de transition (piste C) : ker B ∩ Z⁸⁴ comme Z[H]/(H²+H−12)-module, indice de recollement 7^k, opérateur de défaut D = T − PB | C | P |
| F9 | Complexe triangles + quadrangles : incidence angles–quadrangles (2079 + 2079, 4-régulière), composantes = « grilles tordues fermées », homologie | topologique | P |
| F10 | **Tissu de 11 grilles** (99 = 11 × 9) : partition en 11 grilles serrées, chaque point a 1 voisin dans chaque autre grille, 2-(11,3,9) sur les droites transverses | très risquée, ansatz | P |
| F11 | Complexe cubique / variété plate : si toutes les fermetures 3-cubes existent, Γ = 1-squelette d'une cubulation d'une 7-variété plate R⁷/π, 99 sommets exigent une holonomie non triviale | risquée | P |
| F12 | Réflexions ponctuelles σ_x (flip canonique en x) comme automorphismes approchés ; défaut d(x) ; lien direct avec la branche C2 | mixte | P |
| F13 | Algèbre de Terwilliger relative à une droite (code complètement régulier ℓ) × holonomie ρ_ℓ : composantes du graphe cubique Γ₁(ℓ) équilibrées | mixte | P |

## Deuxième vague (après les premières attaques)

| # | Idée | Type | Statut |
|---|------|------|--------|
| F14 | Rigidité de type design sphérique (annulation de Krein) | classique | **T** : tous les q_ij^k de 99 sont > 0 (q₁₁¹ = 1629/49, …) |
| F15 | **Point de Hamming** : exclure un sommet dans ses 21 grilles (τ = mate en x). Le serrage des grilles (propre à 99) force une bijection φ entre les 4-cycles de deux grilles disjointes et une quasi-1-factorisation de K₅ en chaque sommet de X | lemme spécial | en cours (`hamming_point.py`) |
| F16 | **Rigidité ⇒ symétrie** : montrer qu'une réflexion ponctuelle σ_x est forcément un automorphisme, ce qui ramène C1 à C2 | stratégique | P (les exemples tordus ont beaucoup de σ_x automorphismes, mais ils sont petits et symétriques) |
| F17 | **Torsion ⇒ plan projectif d'ordre t** (très risquée) : les géométries tordues trouvées viennent de plans projectifs (t = 3 : PG(2,3), t = 5 : PG(2,5), tri-incidence (S, −2S, S)). Si toute géométrie locale tordue exigeait un plan d'ordre t, alors t = 6 (Bruck–Ryser) n'aurait aucune torsion, et L1 tuerait 99. Même mécanisme pour t = 10 (Lam) ⇒ unicité de BvLS, et t = 55 (Bruck–Ryser) ⇒ 6273 n'existe pas. | radicale | P, falsifiable : un seul exemple tordu t = 6 (non SRG) la tue |
| F18 | Profil n_min(t) : ordre minimal d'une géométrie locale tordue (t = 2 : 20, t = 3 : 39, t = 5 : ≤ 93) ; 99 = boule ⟺ SRG | expérimentale | P |

## Troisième vague

| # | Idée | Type | Statut |
|---|------|------|--------|
| F19 | Mécanisme « plan d'ordre 10 » (Lam) : un code aux poids contraints force des sous-structures, exclues ensuite par recherche locale | transplant | T (pour l'instant) : pas de code autodual binaire/ternaire naturel ; sur F₇ l'auto-orthogonalité ne contraint pas les poids |
| F20 | « Torsion ⇒ excès > 0 » (forme SRG de F2) | conjecture | équivalente au problème ; non testable à petit t |
| F21 | **Hodge** : sur le complexe triangles + quadrangles, L₁ = 15I + Q, Q = graphe signé des « arêtes opposées » O (12-régulier sur 693 arêtes) ; les triangles de O sont exactement les prismes ; 6P = 2268 − Σν³ (ν = spectre de Q sur la partie rotationnelle, 595 valeurs, Σν = 84, Σν² = 7056) ; H₁(K;Q) = 0 automatiquement | reformulation spectrale | vérifiée sur srg(9) et BvLS ; pas encore de contrainte |
| F22 | Calcul de règles locales démontrables à la main (R0, L12, L13, comptes d'étiquettes) extraites des réfutations par propagation (`explain_up.py`) ; objectif : preuves lisibles de la frontière | méthode | en cours |

## Détail des énoncés testables

**F1.** Pour une arête x–a, l'ombre b ↦ ab est une bijection canonique N(x)∖ℓ → N(a)∖ℓ. Autour de la droite
ℓ = {x,a,ā} on obtient ρ_ℓ. Conjecture : une identité globale (comptage de 6-cycles, trace de A⁶, spectre local)
force Σ_ℓ fix(ρ_ℓ) = 2·#prismes, et cette valeur est incompatible avec la torsion nécessaire.

**F2.** Énoncé fort : tout graphe connexe fini, localement (t+1)K₂, avec μ = 2 pour les paires à distance 2, est
grid-full. Énoncé SRG : tout PQ(2,t,2) est grid-full. Test décisif : chercher des exemples tordus pour petit t ;
témoin de contrôle : l'analogue q = 2 (λ = 0, μ = 2), où Gewirtz est tordu et existe.

**F3.** Un sous-graphe induit S est « −4-serré » si 1_S ∈ ⟨1⟩ ⊕ E₃ ; ex. grilles (9 points, 4-régulier),
H(3,3) (27 points). Plus généralement tout vecteur propre de A_S de valeur 3 (resp. −4) et de somme nulle
se prolonge par 0 en vecteur propre de A. Chercher les configurations tordues qui ont un tel vecteur propre.

**F4.** Projeter τ_a sur les classes : chaque τ_a induit sur les 6 autres classes un 2-multigraphe régulier
(boucles = mate-fixes, arêtes doubles = « classe-cohérent », cycles longs). Conjecture : λ/μ forcent τ_a
classe-cohérent ; alors les triplets de classes {[a],[b],[τ_a b]} forment un STS(7) (Fano) ou τ = mate.

**F5.** Voir 00_FONDATIONS F7. Λ₃ = E₃ ∩ Z⁹⁹ : déterminant d₃ = 7^α 3^β 11^γ (à vérifier), 2-adiquement
pair unimodulaire de rang 54 ⇒ d₃ ≡ 3 ou 7 (mod 8, à carrés près) ⇒ α + β + γ impair. Chercher β, γ forcés,
puis relier α au rang 7-adique (rank₇(A − 3I)) et au recollement local sur ker B.

**F10.** Hypothèse : V = G₁ ⊔ … ⊔ G₁₁ (grilles). Alors (serrage) chaque point a 4 voisins dans sa grille et 1 dans
chacune des 10 autres ; les 165 droites transverses forment un 2-(11,3,9) sur les grilles.
