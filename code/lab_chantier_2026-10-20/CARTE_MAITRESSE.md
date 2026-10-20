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

## 4. Routes fermées : ne pas refaire

Le détail, sourcé, se trouve dans la section « Routes fermées » de chaque fiche : L01 §4, L02 §12, L03a §4, L03b §4,
L04 §4, L05 §4, L06 §4, L07 §4, L08 §5, L09, L10 §5. On regroupe ici par mécanisme. Pour chaque famille, on dit
**pourquoi elle meurt**. « Fermée » veut dire que la méthode ne peut pas conclure seule ; cela n'exclut pas le graphe.

**4.A Solveurs génériques sur le modèle complet** (SAT, CP-SAT, MILP, recuit, cubes, CDCL).
- **Bilan.** Tout est UNKNOWN :
  - 21-25/09 sur C2 (L01 §4.A, L10 §5) ;
  - CP-SAT complet en 4 min (L08 §5) ;
  - R8 en CDCL pur : 5·10⁷ à 10¹² heures-cœur (L08-213) ;
  - route Ω : étage colonnes ≥ 1,7·10¹⁰ h CPU, et Kissat ne retrouve même pas BvLS (L07 §4.9).
- **Pourquoi.** Les contraintes λ = 1, μ = 2 sont satisfiables localement presque partout, et les espaces symétriques
  sont énormes. Le solveur ne voit ni le rang ni l'intégralité globale.

**4.B Relaxations convexes** (PL, SDP, moments, Lasserre, flag algebras, Delsarte, Gegenbauer, Jacobi, positivité du
recensement).
- **Bilan.** Toutes sont faisables :
  - centre fractionnaire exact Γ0 avec T = 3P, U = 4P (L05-167) ;
  - point entier P = 0 du recensement d'ordre 9 (L05-149) ;
  - moments automatiques (L06 §4.23) ;
  - Jacobi faisable même à P = 0 (L08 §5) ;
  - flags ≤ 9 sans contrainte au-delà de P ≤ 852 (L10 §5).
- **Pourquoi.** Les paramètres de Conway satisfont toutes les conditions de faisabilité. Seules l'intégralité, le rang
  et l'arithmétique mordent.
- **Exception utile.** P ≤ 852 vient d'un PL sur le recensement (§8.1).

**4.C Réseaux, genre, discriminants, invariants de Hasse.**
- **Bilan.** Toutes les conditions locales sont satisfaites :
  - contre-modèle Golay au genre seul pour C2 (L01 §4.H) ;
  - Hasse aux premiers ≠ 7 (L06 §4.21) ;
  - les 271 designs passent pour α = 22 (L05, L07 §4.5) ;
  - le transfert du genre de C3 à C2 ne redonne que le théorème A (L10 §5).
- **Pourquoi.** L'obstruction n'est pas locale en un premier ; il faut une donnée globale (classification, rang,
  positivité).

**4.D Séries thêta et formes modulaires de niveau 7.** C'est ce qui a donné la fenêtre de rang (r ≤ 35 exclu, L06-023).
- **Fermées au-delà :**
  - thêta harmonique quartique (64/64 coins faisables au rang 37, L06 §4.3, L10 §5) ;
  - programmes « côté 3 » (marges de 10¹² à 10¹⁶, L06 §4.1) ;
  - route de Hermite et de Minkowski (note 110) ;
  - séries thêta pour le rang 37, épuisées (L08 §5).
- **Pourquoi elle s'arrête.** Le chemin critique passe par les normes 18 et 26 (L06-103), hors de portée exhaustive.

**4.E Comptages** (recensements, collisions, comptage du rang 37).
- **Bilan.** Clos par leurs propres marges :
  - point mort 13 900 < 16 496 (L10 §5) ;
  - canaux de masses 7 à 9 de 20 à 35 fois trop grands (L06 §4.7) ;
  - aucune congruence dans le recensement jusqu'à l'ordre 10 (L06 §4.5, L08 §5).
- **Pourquoi.** Un double comptage exprime des moyennes, et un graphe hypothétique peut équilibrer ses moyennes.

**4.F Tests de Gram locaux** (un sommet, une étoile, une droite, sans rang).
- **Bilan.** Ils ne peuvent exclure aucun des rangs 37, 39 et 41 :
  - plafond local de 14, espace hyperbolique de dimension 14 sur F7 (L05 §4, L06 §4.10) ;
  - la relaxation algébrique de l'étoile se prolonge toujours (L05-056) ;
  - deux apex ne suffisent pas (L05-044).
- **Ce qui marche quand on y ajoute le rang et l'intégralité :**
  - test d'étoile au rang 37, route finie (§6) ;
  - au rang 39, l'étoile meurt 5 fois sur 5 (E, L08-181) ;
  - aux rangs 41 et 43, c'est insuffisant en l'état (L08 §1.8).

**4.G Lois locales devinées sur des données** (lois à quatre étoiles).
- **Lois réfutées** par des témoins exacts : (H3), (H4), (A), (A4), plafonds de relations mixtes, (N9), (NOGRID), (LOW),
  (R7), ODD9, SUM14, KER-SYM universelle (L07 §4.13).
- **Pourquoi.** Chaque loi venait d'une seule famille symétrique et tombait dès la première famille indépendante. Les
  données (≈ 1,14 M structures) ne sont même pas des blocs de Conway, car aucune base ne s'étend (L07-103).
- srg(243) est un mauvais banc d'essai pour ces lois (L07 §4.15).

**4.H Mécanismes d'asymétrie et constructions.**
- **Fermés :**
  - deux-graphe (k ≠ 2μ) ;
  - commutation de Godsil-McKay à une classe (k ≥ 14) ;
  - déformation d'un Conway symétrique (il n'y en a pas) ;
  - routes structurées vers un λ = 1 asymétrique : 243 est rigide sans hôte GQ, et 378 a un stabilisateur minimal S3
    (L07 §4.1-4.4).
- **Symétrie forcée.** Avec Aut = 1, on a au moins 645 120 complétions du cadre. Il manque une borne supérieure du
  nombre de complétions, et aucune méthode n'est en vue (L07 §4.2).

**4.I Reformulations.** Q7, ODD-PURE, H46, a ≤ 1, b ≥ 1, etc. : elles n'ont rien fermé (L10 §5, critique de
l'utilisateur du 17/10).

**4.J C2 et C3** (pour mémoire).
- Les routes génériques sont closes, voir L01 §4 et L02 §12.
- C3 est fermé par la congruence de deux structures entières (Q entière, M hermitienne sur ℤ[ω]) modulo 1 − ω, avec des
  déterminants incompatibles (L04).
- C2 est fermé par la classification des réseaux unimodulaires impairs de rang 24 (156 réseaux de Borcherds), réseau par
  réseau (L01, L02).

**Méta-leçon (H, lecture de l'assembleur).** Les seules exclusions obtenues combinent trois ingrédients sur un objet qui
a une **classification finie** :
1. une donnée **arithmétique globale** : congruence modulo 7 ou 1 − ω, classification de réseaux ;
2. la **positivité ou le rang** ;
3. l'**intégralité**.

Exemples : la fenêtre de rang par thêta de niveau 7 (arithmétique + positivité), C3 (deux structures entières
congruentes), C2 (classification de Borcherds + calcul fini), le test d'étoile au rang 37 (rang + intégralité +
positivité sur une liste finie de droites). Chaque méthode qui n'utilise qu'un ou deux de ces ingrédients s'est révélée
satisfiable par les paramètres de Conway.

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

## 9. Chronologie depuis conway99-involution (21/09)

Chronologies détaillées : §2 de chaque fiche. On ne garde ici que les jalons. Heures en UTC sauf mention.

**Avant (littérature et externe)**
- Makhnev–Minakova 2004 : Fix(g) est vide ou un triangle.
- Behbahani 2009 et Behbahani–Lam 2011 : |Aut| ∈ {1, 2, 3}.
- Dépôt externe conway-99-research, 22-29/07/2026, vagues 1 à 205 (L03a, L03b).
- Ishida, arXiv 2606.29183 ; Reimbayev, arXiv 2608.19410 ; Thakkar–Severini.

**Septembre**
- **21/09 11:56** : première session (eeaf2d22). Décision : branche involution C2 (L03a).
  - 17:02 : dépôt `conway99-involution`.
  - Théorème de rang F2.
  - Batterie SAT de nuit, entièrement UNKNOWN (L01).
- **22/09** : workflow de 8 agents interrompu (quota), suivi de la consigne « plus d'agents sauf demande ». Archive
  `conway99-lab-archive`.
- **22-23/09** : C3.
  - Route calculatoire arrêtée à 10:14.
  - Le même jour, preuve à la main C3X, avec Lean et le comparateur paranoïaque OK au commit 874903f (L04).
- **23-27/09** : C2 par « familles » : lemme des étoiles, H-β, M1, tout-tordu (circuits simples), AD2 (L01, L09).
- **24-26/09** : C1, session Claude-C1, lemmes L1 à L25. Tous sont des planchers ; le profil P = 0, k = 28 les satisfait
  tous (L09-103).
- **25/09** : carnet C2 sans solveur ; Astra trouve que le théorème A v1 est faux ; ouverture du labo « structures » (L01,
  L09).
- **27/09** : route (C) de Sol, avec 156 réseaux de Borcherds, qui devient la voie principale de C2 (L01, L09).
- **28-29/09** : rank-17 ; théorème caractéristique d'Astra (228/751) ; passage à AWS (L09, L10).
- **30/09-01/10** : espace du chercheur 2 (T4, (S), L_N) ; EX ouvert (L01).

**Octobre**
- **02/10** : C7 sans ordinateur, avec Lean (conway-C7).
- **03-07/10** : campagne AWS de C2 (L02).
  - **07/10 17:47** : tracker 156/156, T16, T18 et T20 acceptés ; article C2 ; calculs parqués à 20:42.
  - ~21:00 : C1 ouvert, Codex en tête (L01, L02, L10).
- **07-08/10** : programme thêta de niveau 7 : r = 33 exclu (07/10 22:57), puis **r = 35 exclu (08/10 01:23)**, d'où la
  fenêtre {37, 39, 41, 43} (L06). Le même jour : P ≤ 852 et ρ ≤ 126 (Codex) ; comptage du rang 37 clos par ses marges.
- **09/10** :
  - 05:08 : l'utilisateur arrête tous les calculs ; 09:15 : trois mandats ;
  - 174 noyaux de Makhnev (Codex) ;
  - priorité à l'« exploration » (L05, L06, L10).
- **10/10 00:02** : lemme N14 : pas de vecteur propre −4 de norme 14 au rang 37 (E, non audité) (L06-092).
- **12/10** :
  - changement de cap vers les SRG asymétriques ;
  - question S3 UNSAT, DRAT vérifié le 13/10 ;
  - nouveaux srg(243) ;
  - défauts de cocliques V5 à V11 (L05, L06, L07).
- **13/10** :
  - V12 à V14, dont la rigidité de rang 2 ;
  - mission « C2 sans calcul » ;
  - relecture et réécriture de C3 ;
  - Cesarz–Woldar réécrivent les §1-3 de C3 (L01, L04, L05).
- **14/10** :
  - **V15** : un bord positif de 43 sommets admet au plus 2 complétions (Codex) ;
  - nuit « sans anciennes notes », jugée ratée par l'utilisateur (redécouverte de la fenêtre) ;
  - cap sur l'asymétrie ; construction de srg(378,52,1,8) avec |Aut| = 6 (L05, L07, L10).
- **15/10** :
  - audit des exclusions ;
  - (H-MATCH) ⇒ pas de Conway ;
  - ODD9, KER-SYM et SUM14 réfutées ;
  - (N9-NG), NG5 et NG7 (L05, L07).
- **16/10** :
  - nuit H-MATCH : la route locale est épuisée à 08:00 ;
  - aucun germe à quatre étoiles ne s'étend ;
  - revue globale en 9 relectures ;
  - R7 SAT, R8 ouvert ; branche exploratoire Q7 (L07, L08, L09).
- **17/10** :
  - c = 1 (H46, lemme 2-coupe) ;
  - E3 (Codex) ;
  - tout est fusionné sur `main` (L05, L08, L10).
- **18/10** :
  - **bug OR-Tools 9.15** (11:40 locale), avec retraits ;
  - 3P + 4G ≤ 2772 (13:15) ;
  - branche « c(L) ≥ 4 pour toute droite » fermée (CP-SAT, 16:36) ;
  - registre c3 à 10 052 ouverts ;
  - P ≤ 852 revérifié (L05, L08).
- **19/10** :
  - nuit : familles 5602, K3U, 2K2, P3NB, K2BC, 2K2N + B/C fermées ;
  - registre c3 à 35 ouverts ;
  - dernier message du pont à 07:31 (L08, L10, L11f).
- **20/10** :
  - théorème de réduction du rang 37 (Théorème 6.1) ;
  - énumération de 1,87·10¹¹ classes ;
  - moteur 10 fois plus rapide ;
  - audit R8 ;
  - AWS abandonné ;
  - le soir : **chantier de consolidation** (ce dossier) (L08, L10).

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
