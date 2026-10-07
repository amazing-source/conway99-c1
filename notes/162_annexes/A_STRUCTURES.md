*Annexe de la note 162 : rapport d’un agent de lecture (07/10/2026), versé tel quel. Les affirmations sur les autres dépôts sont celles du rapport ; voir la note 162 pour la synthèse et les réserves.*

# Inventaire du dépôt conway99-structures-lab

Racine : `/home/user/conway99-structures-lab`. Les chemins ci-dessous sont relatifs à cette racine.

## 0. Portée et avertissements

- **Instantané** : un seul commit (3e9690b, 27/09/2026 15:44). Le JOURNAL couvre la période du 25/09 au 27/09 vers 15 h 30.
- **Rôle du dépôt** : c'est le labo « structures ». Il vérifie de façon indépendante le travail de C1 (cas général, 7-adique) et de C2 (involution), généralise leurs lemmes et balaie les tables.
  - C3 (ordre 3, preuve « vérifiée en Lean ») n'est que cité.
  - Astra est un « autre modèle » ; Sol est ChatGPT. Leurs rapports sont relayés par l'utilisateur et partiellement relus ici.
- **Pas de second srg(243,22,1,2) dans ce dépôt.** Le dépôt dit l'inverse :
  - « L'unicité du graphe à 243 sommets est OUVERTE » (NOTE_S25 §7) ;
  - « un srg(243,22,1,2) sans (*) serait un nouveau graphe » (famille/REVUE_LITTERATURE_9_243.md).
  - Le résultat « second 243 tordu / réfutation de Reimbayev » vient donc d'un autre dépôt ou d'une date postérieure.
- **Aucun résultat ici ne tranche srg(99,14,1,2), ni même le cas involution.**
- J'ai fait quelques contrôles moi-même, tous en lecture seule et dans le scratchpad. Ils sont signalés par **[contrôle de ma part]**.

---

## 1. Résultats hors 99 : tables de Brouwer et familles srg

### R1. S5 : critère 2-adique de non-existence (discriminant mod 4 des réseaux propres)

**Énoncé** (NOTE_S5 §1) :
« Soit Γ un srg(v,k,λ,μ) à valeurs propres entières k > r > s, et d = r − s. Pour θ ∈ {r,s}, notons θ′ l'autre valeur propre, m_θ la multiplicité de θ et Λ_θ = ℤ^v ∩ ker(A − θI). Supposons d impair et v₂(k − θ′) ≥ v₂(v). Alors :
1. m_θ est pair ;
2. (−1)^{m_θ/2}·det Λ_θ ≡ 1 (mod 4) ;
3. det Λ_θ = ∏_{q|d} q^{c_q}·P_θ, avec P_θ = ∏ q^{v_q(v)} sur les premiers q | v, q ∤ d, v_q(k − θ′) < v_q(v). »

- **Corollaire A** : si tout premier de d est ≡ 1 (mod 4), alors (−1)^{m_θ/2} P_θ ≡ 1 (mod 4).
- **Corollaire B** : « Si tout premier divisant n est ≡ 1 (mod 4) et si e est impair, il n'existe pas de graphe NL_e(n) = srg(n², e(n+1), −n+e²+3e, e²+e). »
- **Corollaire C** : si v est impair, que tout premier de v divise r − s et que tout premier de r − s est ≡ 1 (mod 4), alors f ≡ g ≡ 0 (mod 4).

**Type.** Théorème avec une preuve courte, plus un balayage calculatoire.
- v ≤ 1300 : 36 exclusions, soit 35 « ? » et (289,54,1,12) déjà connu.
- v ≤ 5000 : 185 exclusions, dont 63 de type NL_e(n) avec e impair et 122 sporadiques.

**Vérification documentée.**
- Contrôles exacts sur de vrais graphes : Petersen, T(7)…T(21), Paley(25), Paley(169), LS₃(5), LS₃(13), LS₄(13). Résultat « ALL CONSISTENT ».
- Relecture de C2 (§6) : mécanisme refait ; (289,54,1,12) et la famille NL recalculés à la main.
- Audit adverse d'Astra (NOTE_S5 « §5 » bis ; astra/RAPPORT_ASTRA_SUIVI4_ET_AUDIT_S5.md, message 2) :
  - « DÉMONTRÉ : le critère proposé tient » ;
  - réseaux saturés recalculés (Petersen det 162 et 405 ; T(7) det 109 375 et 46 875) ;
  - balayage indépendant en Python et en JavaScript : 4 538 lignes, 1 183 existantes, **0 existante exclue**, mêmes 35 « ? », 0 manquant, 0 en trop.
- Scripts reproductibles : scripts/disc4_scan.py, disc4_validate.py, brouwer_crosscheck.py, genus_scan.py.

**Nouveauté (telle que documentée).**
- Le lemme de réseau est **classique** : J. Martinet, *On parity classes* (2003), cor. 6.4.
- (289,54,1,12) est **déjà connu** (Bondarenko–Radchenko, JCTB 2013).
- Koyama 1991 et Bagchi (arXiv:2102.05576) sont proches mais différents.
- Verdict d'Astra : « la nouveauté du critère paramétrique et du corollaire NL_e(n) reste INDÉCISE … À ne pas présenter comme nouveau sans l'avis d'un expert. »

**Pertinence.**
- Directement les tables de Brouwer.
- Pour 99 (d = 7 ≡ 3 mod 4), le critère ne redonne que « k pair » (L2 de C1) : « rien de neuf pour 99 ».

**Fichiers.** NOTE_S5_DISCRIMINANT_MOD4.md, logs/disc4_scan_1300.log, logs/disc4_scan_5000.log, logs/brouwer_crosscheck.log, logs/disc4_validate.log, logs/brouwer/ (26 pages HTML de la table, v ≤ 1300).

### R2. S1 : genre des réseaux propres (formule d'oddité), « plafonds » de p-rang

**Énoncé** (docstring de scripts/genus_scan.py). Dans la « classe propre » (d impair, chaque q | d avec v_q(d) = 1 et q ∤ v), le scan contraint les rangs de recollement α_q et les signes. Il en sort :
- **12 ensembles sans α admissible**. Ils sont tous parmi les 35 de S5 ; NOTE_S5 §5 dit que le niveau mod 8 « n'ajoute aucune exclusion ».
- **44 ensembles où le plafond α = min(f,g) est exclu** (« type L22 »).
  - Ils incluent 99, où α₇ est pair et ≠ 44, ce qui est exactement L22 de C1.
  - Ils incluent aussi srg(57,14,1,4).

**Type.** Dérivé et observé.

**Vérification.**
- Contrôles sur Petersen et T(7)…T(21) (genus_validate.log) : cohérents.
- T(5) est « INCONSISTENT » dans le log ; le JOURNAL l'attribue au harnais (complément mal apparié), qui n'a pas été corrigé.
- Pas d'audit externe.

**[contrôle de ma part]** Trois des 44 ensembles existent dans la table : (176,45,18,9), (209,100,45,50) et (1116,245,70,49). Le scan y prédit, entre autres, α₃ impair et ≠ 32 pour (176,45,18,9). Sur 5 graphes-blocs de STS(33) (1 construit par Bose, 4 tirés au hasard) :
- rang₃(A − 12I) = 31 : impair, sous le plafond ;
- rang₅(A − 12I) = 33, soit α₅ = 32 : c'est le plafond, que le scan autorise pour q = 5.
- Tout est cohérent.

**Pertinence.** Prédictions de p-rangs pour des ensembles de la table ; pas d'exclusion nouvelle.

**Fichiers.** logs/genus_scan_1300.log, logs/genus_validate.log.

### R3. S2 : « exactement un de E_r, E_s est q-entier » (q ∤ d, q | v)

- **Statut au registre** : « DÉRIVÉ : jamais violé par un ensemble réalisable (conséquence des multiplicités entières ?) ». Le log donne 0 violation.
- En fait, la preuve directe figure dans NOTE_S5 §6 (relecture de C2) et dans l'audit d'Astra : (k − r)(k − s) = μv et (k − s) − (k − r) = d.
- Le statut « observé » est donc sous-évalué.

### R4. S3 et S6 : lemmes de C1 et C2 rejoués sur de vrais graphes

- **L21** (rang local d'une boule de droite) : 891/891 droites de BvLS et 6/6 de srg(9). Le contrôle négatif échoue à 100 %, comme attendu.
- **L23** (signe) : 4/4 sur T(n). Le contrôle négatif « ne discrimine pas » (c'est dit).
- **Équilibre de C2** BBᵀ1_C = (k − 14)1_C + (5/3)|C|1_N : 8 910/8 910 composantes sur BvLS, contrôle négatif 891/891.
- **Fichiers** : logs/s3_lemmas_real.log, logs/c2_balance_check.log.

### R5. Famille srg(2m²+1, 2m, 1, 2) (NOTE_S25, famille/)

**(a) Arithmétique.**
- t² = 8m − 7 et t | 63, d'où m ∈ {2, 7, 11, 56, 497}, soit v ∈ {9, 99, 243, 6 273, 494 019}.
- « Les membres qui existent ont t ∈ {3, 9} … Les trois cas ouverts ont t ∈ {7, 21, 63}, c'est-à-dire exactement 7 | t. »
- Pour p | t, on a p | v ⟺ p = 3.
- Type : dérivé élémentaire. La note n'affirme pas de nouveauté.

**(b) Lemme de Godsil–McKay** (NOTE_S25 §5, présenté comme « Nouveau ») : « Soit Γ = srg(v,k,1,2) avec k ≥ 8. Γ n'a aucun ensemble de commutation de Godsil–McKay non trivial. »
- Preuve à la main : comptage, puis borne spectrale e(C,C̄) ≥ (k − r)|C||C̄|/v.
- Aucune relecture externe ni recherche bibliographique documentée. J'ai relu la preuve ; elle me paraît correcte.
- Portée annoncée : on ne fabrique ni un autre srg(243,22,1,2) ni un srg(99,14,1,2) par commutation de Godsil–McKay à une classe. « Ce n'est pas une preuve d'unicité. »

**(c) Invariants de H(2,3) et de BvLS** (family_invariants.py). Holonomie triviale, P = P_max (6 et 8 910), 100 % de points de Hamming, rang₃ = 4 et 67, forme de Smith 3-adique 1⁶⁷3³⁴9¹⁰0¹³². Le 67 retrouve Brouwer–van Eijl.

**(d) Contrôle positif de C1 notes/125** (Σ_L c₄(G(L)) = S + 3P, Σ_L c₃ = 2P). H(2,3) : 12 = 2P et 18 = 3P. BvLS : 17 820 et 26 730.

**(e) Revue de littérature** (faite par un agent, à partir des sources primaires) :
- l'unicité de 243 est ouverte ; la table de Brouwer porte « + » et non « ! » ;
- Makhnev 1988, Th. 2 : aucun srg(99,14,1,2) ne vérifie (*) ;
- (*) ⟺ P = P_max ⟺ n₃ = 0 (Reimbayev) ;
- Aut ∈ {1, Z₂, Z₃} est une « combinaison faite par l'agent » ;
- « Vérification de l'agent (non publiée) » : chaque classe de parallélisme de BvLS est srg(81,20,1,6). L'analogue srg((2m²+1)/3, 2m − 2, 1, 6) n'a des multiplicités entières que pour m ∈ {2, 11}.

**Fichiers.** NOTE_S25_FAMILLE_9_243.md, famille/*.

---

## 2. Conway-99, cas involution (C2) : apports de « structures »

Cadre : σ involution, Fix σ = {x}, 7 blocs, 42 orbites.

**R6. Tout-tordu, au moins 3 triangles, et deux triangles disjoints : exclus à la main** (NOTE_S8).
- S8.1 : le type (3⁵,6) est impossible, avec une borne de 48 > 42.
- S8.2 : lemme de l'« orbite morte » (−4 = 0).
- S8.4 : lemme du complément CL, φ(ab) = 3 − N_ab.
- S8.5 : « deux triangles disjoints ⇒ impossible ».
- Familles sans chaîne traitées à la main ; le triangle de triangles donne ≥ 43 > 42.
- Vérification : relu par C2 (« TIENT », inscrit à son §26) ; solveur indépendant au niveau des étiquettes, 670/670 clés d'accord ; verify_pasch_hand.py sur 1 340 clés.

**R7. S11 : deux triangles sécants, à la main.** 27 720 décompositions étiquetées, 8 classes.
- Outils : PPE (« exactement 2 orbites ont φ = 2, 12 ont 1, 6 ont 0 »), couplage E[P][Q] = E[Q][P], lemme T, lemme A.
- PPE est relu par C2. Les étapes locales sont vérifiées par solveur exact (verify_two_sharing_hand.py).

**R8. S17 : un triangle.** 15 classes, 41 790 décompositions, **84 certificats entiers** (Farkas + arbres de branchement).
- Revérifiés par un code séparé (verify_core_certs.py), couverture complète. Contrôle négatif : 4 corruptions sur 5 rejetées.
- Type : preuve assistée par ordinateur avec certificats (logs/core_certs/).

**R9. S19 : sans triangle.**
- L'identité d'orbites Q² + Q = 12I + 4J − Sh est **celle de C2** (son carnet §0), redémontrée ici et contrôlée exactement sur BvLS : Q² + Q = 20I + 4J − Sh.
- Elle sert dans un modèle de colonnes-orbites (352 800 colonnes par classe) : **14 certificats à la racine**.
- Vérifiés par un code séparé (verify_orbit_certs.py, couverture 30 360) **et par le code de C2** (14/14).

**R10. S31, ERRATUM, trouvé par « structures » et confirmé par C1 et C2.** R6 à R9 ne valent que pour les structures D à circuits **simples** (121 215 sur 15⁷ systèmes de transitions). « La simplicité n'est démontrée nulle part » : le cas non simple reste **OUVERT**.

**R11. S33 : deux blocs couplés (T = K₇, non simple).**
- Couplage systématique, dont 80 équivalences « partagée × lointain-lointain » oubliées par la spécification initiale.
- CROSS : 200 équations exactes.
- 60 instances SAT. Seul le recollement identité est UNSAT (20 s) ; le reste est inconnu.
- Contrôles : BvLS (dégénéré) et un monde synthétique.

**R12. S28 : AD (Σ = ∅, paires ancrées ou dd).**
- **Lemme T⁺** (démontré) : |S| ≥ 3 + [j ∈ S] + |Π|.
- Les **14 survivants AD2 meurent à la main**, relus par C1.
- Balayage des 26 524 classes : tout meurt pour n_dd ≤ 6 (verdicts PLNE scipy, voir §6).
- Résidus à n_dd = 7 à 9 : tous ont un bloc A, donc g⁻ = 20.

**R13. Outils relus ou démontrés** (NOTE_S23, LEMMA_SCOPES).
- 𝒫 = 6I − 2Q − Sh + J avec **𝒫² = 14𝒫** : outil d'Astra, revérifié à la main.
- **3h ≤ 2n_dis** : théorème d'Astra §7, refait.
- Réduction de D(A) à 5 supports : certificats entiers, recoupée en fractions exactes.
- Lemme (★) de C2 : redérivé.
- Portées des lemmes SAT : **SEC est faux en présence de carrés dis**, valide si n_dis = 0.
- « Lemme décomposable » (S37) : preuve générale de « structures », adoptée par C1.

**R14. S27 : genre 7-adique sous involution.**
- **g⁻ = rang₇(S − 3I) est pair, g⁻ ≠ 22 ; g⁺ est pair et ≠ 0 ; 88 ≤ M ≤ 173.**
- Vecteurs propres exacts z_c (valeur 3, norme 21) et w_c (valeur −4, norme 28).
- Signe local −1 forcé à g⁻ = 18.
- Contrôles d'oddité exacts sur H(2,3) et BvLS. Relu par C1 (« tout tient »).

**R15. Bilan g⁻.** On a g⁻ ∈ {18, 20}, par la combinaison de trois apports :
- Astra (dossier 6, relu) : min Λ₋₄⁻ ≥ 8, det L_T = 2¹²7^{g⁻−7}, Blichfeldt donc g⁻ ≥ 12, réduction à un réseau de déterminant 49 ;
- C1, recoupé ici (blockline_exhaustive.py) : g⁻ ≠ 14 ;
- C1 notes/132 (lemme de Witt), relu ici : g⁻ ≠ 16.

S'y ajoute : un bloc plein force g⁻ = 20.

**R16. S29 : bloc plein.** Faits de base démontrés : h = π∘m, pas d'annulation, critère de rigidité des orbites ancrées, équations linéaires exactes (E1) et (E2).
- **spec T_FF = 3⁹(−4)⁴(−1)⁵(−2)⁶1⁶**, |r_f|² = (14 + y − 3x)/15.
- Une affirmation de « ligne exacte » réelle a été retirée (corrigée dans la note).
- Système local (i)–(iii) : heuristique ≈ 10⁻¹⁰ solution par type, présentée comme heuristique.

**R17. S34 et sweep79 : les 79 types clés.**
- 25/79 UNSAT au tri (glucose).
- **C2 rapporte 25/25, puis 33/79 « VERIFIED » en DRAT.** Ces certificats DRAT ne sont pas dans ce dépôt.
- Identité générale de C1 testée sur BvLS : 1 200/1 200.
- spec_local.py : la spécification compile octet pour octet (18/18). Invariance sous Stab : 12/12.

**R18. Route (C) : S35, S36, S37.**
- **156 réseaux unimodulaires impairs de dim 24 et min ≥ 2 (Borcherds) construits explicitement dans ℚ²⁴** par voisins de Kneser, et revérifiés 156/156 (verify_all.json).
- « Correction » de l'id 150 (2ᵉ voisin = E₈³) : c'est une **correction de transcription du fichier JSON de C1** (build156.py : « Transcription fixes to data/borcherds_odd24.json »).
- O₂₄ : 141 classes, dont **86 exclues** par PL de classe entière avec certificat entier, selon le registre ; la classe 1 a un certificat à un seul vecteur.
- **132 (d₆⁴)** : exclu par trois voies ; le fichier montre 294/304 au PL. **115** : 1 470/1 472 au PL, plus la DFS de C2.
- La « coupe de parité » de Sol est vide.
- Suivi : 19/156, plus 132 et 115.

**R19. Rapports de Sol (ChatGPT), relus partiellement.**
- « Supports courts » §1–2 relus et justes : norme ≤ 10 dans L_T donne des coefficients ±1 ; norme 8 donne cube ou Wagner.
- Le cube force un prisme, donc il n'est exclu qu'à P = 0.
- Lemme « six ou sept blocs » relu. Les 25 certificats à six blocs sont « plausibles mais non refaits ».
- « La cible est dépassée » (g⁻ = 12 était déjà exclu).

## 3. Conway-99, cas général et Fano tendu (C1) : vérifications

| id | contenu | statut |
|---|---|---|
| S12 | notes/116 de C1 : (P2), critère lointain, Fano tendu | TIENT ; **erreur trouvée** : diagonale = 16 − 2e(R), et non 16 ; corrigée par C1 (b9fb15e, d02ac18) |
| S18, S20 | certificats X19 et « cellules » de C1 | 19/19 cellules + 2/2 paire × bloc VALIDES, Farkas identiques ; code propre |
| S21, S22 | Ψ_R annule les comptes permis ; lemme P-Ψ | démontrés à la main ; contrôle 168/168 |
| — | obstruction de rang cellcross ; noyau universel | recalculés, identiques à C1 |
| NOTE_ASTRA_CERTIFICAT | certificat de Rayleigh d'Astra (branche d'un témoin) | wᵀCw = −2, qᵀAq − 3‖q‖² = 16 ; « ni une non-existence » |
| S24 | Astra dossier 5 : une boule exclue à k = 22 ; R = 0 ⇒ SRG ; MR = 0 et rang ≤ 2 ⇒ SRG | TIENT ; ajout : MR = 0 est automatique, donc k = 24 est un problème de construction complet |
| S26 | famille cyclique exclue à k = 22 ; \|J_bad\| ≥ 8 ; 66 composantes 4+4+4 | TIENT ; un point de signe délégué à C1 |
| — | étoile complète morte sur 42/42 boules ; espérance ≈ 10⁻¹⁵ | **heuristique**, dite telle ; « pas une preuve » |

## 4. Éléments sur les tables de Brouwer

Fichier principal : `/home/user/conway99-structures-lab/NOTE_S5_DISCRIMINANT_MOD4.md`. Données : `/home/user/conway99-structures-lab/logs/brouwer/`, instantané de la table pour v ≤ 1300.

**1. Les 35 ensembles « ? » exclus par S5** (lignes principales, compléments exclus aussi) :
- **Famille NL_e(n), e impair** :
  - (169,42,5,12), (169,70,27,30) ;
  - (289,90,23,30), (289,126,53,56) ;
  - (625,130,15,30), (625,182,45,56), (625,234,83,90), (625,286,129,132) ;
  - (841,150,11,30), (841,210,41,56), (841,270,79,90), (841,330,125,132), (841,390,179,182).
- **Sporadiques** :
  - (209,52,15,12), (235,52,9,12), (375,154,53,70), (375,170,85,70), (391,140,39,56), (430,39,8,3), (441,190,89,76), (494,85,12,15), (507,44,1,4) ;
  - (616,205,90,57), (630,68,1,8), (690,318,121,168), (721,220,69,66), (750,210,55,60), (750,214,63,60), (780,369,158,189) ;
  - (871,348,137,140), (875,184,33,40), (931,180,29,36), (1026,451,212,187), (1148,481,210,195), (1248,203,22,35).
- **Statut** : preuve relue par C2, audit d'Astra (deux implémentations), 0 graphe existant exclu sur 1 183. Nouveauté « INDÉCISE ».
- Le dépôt prévoit : « Avant toute annonce : audit indépendant (Astra), puis avis d'expert (A. E. Brouwer tient la table) ». L'audit est fait ; **aucun contact avec Brouwer ni texte de commentaire rédigé** n'est documenté.

**2. Inexistants déjà connus retrouvés.**
- (289,54,1,12) : Bondarenko–Radchenko, « tombe en cinq lignes ».
- (154,51,8,21) : trouvé par Astra seulement. **[contrôle de ma part]** C'est « Krein2 » dans la table ; le filtre de faisabilité du dépôt l'écarte avant le test, d'où « 1 » chez nous et « 2 » chez Astra.

**3. (750,210,55,60).** La table porte « pg(14,14,4)? ».
- **[ma lecture, non écrite dans le dépôt]** Le graphe de points d'une pg(14,14,4) a exactement ces paramètres. Si S5 est correct, pg(14,14,4) n'existe pas.

**4. Corollaire NL_e(n) au-delà de la table.** 185 exclusions pour v ≤ 5000, dont 63 NL (n = 13, 17, 25, 29, 37, 41, 53, 61, 65).
- « Test décisif » : à v = 625, **[contrôle de ma part]** e = 4, 6, 8, 10, 12 existent et e = 5, 7, 9, 11 sont « ? ».
- À v = 841, seul Paley (e = 14) est connu ; les e pairs de 6 à 12 sont aussi « ? ». L'argument y est donc faible.

**5. S1 : 44 « plafonds » de p-rang.**
- Ils incluent 99, (57,14,1,4), (85,14,3,2) et (266,45,0,9), ces trois derniers inexistants selon la table.
- Ils incluent aussi 3 ensembles existants : (176,45,18,9), (209,100,45,50), (1116,245,70,49).
- Aucune exclusion nouvelle. Ce sont des contraintes de rang mod q, que j'ai trouvées cohérentes sur STS(33).

**6. Entrée 243 dans la table.** « + » et non « ! » : l'unicité est ouverte. Le lemme de Godsil–McKay exclut un second 243 obtenu par commutation à une classe.

**7. Littérature.**
- Brouwer–van Eijl : rk₃ = 67 pour BvLS, retrouvé.
- Pour 99 : « rk₇(A − 3I) ≤ 45 ».

**8. Hors table de Brouwer.**
- id 150 de la liste de Borcherds : transcription du fichier de C1, pas une erreur de la table publiée.
- Dans le carnet de C2 (logs/c2_programme.md) : Thakkar–Severini (arXiv 2608.11211 v2) décrit à tort le cas Z₇ à un point fixe comme ouvert (Behbahani–Lam).

**Aucune correction d'une entrée existante de la table de Brouwer** n'est revendiquée. « (Makhnev is wrong) » dans srgtab751-800.html est un commentaire de Brouwer lui-même.

## 5. Les plus publiables, par ordre

1. **S5** : critère 2-adique, 35 « ? » de la table, famille infinie NL_e(n) et 185 exclusions jusqu'à 5000. Preuve courte, audité, reproductible. Il faut d'abord un avis d'expert sur la nouveauté et citer Martinet.
2. **Contraintes de réseau sur une involution de srg(99,14,1,2)** : g⁻ pair et ∈ {18,20}, réduction au déterminant 49, plongement dans les réseaux de Borcherds. La rédaction dépend de notes de C1 absentes d'ici.
3. **Rigidité de Godsil–McKay** pour srg(v,k,1,2), k ≥ 8 : courte et autonome, nouveauté non vérifiée.
4. **Méthode certifiée** (identité d'orbites, Farkas entiers, vérificateur indépendant) et exclusion du tout-tordu à circuits simples. Seulement dans un article qui ferme l'involution.
5. **S1** : table de plafonds de p-rang (44 ensembles), en annexe de 1.
6. **Les 156 réseaux de Borcherds explicites** : jeu de données. Le dépôt n'examine pas leur nouveauté.
7. **Synthèse « famille »** (7 | t ⟺ cas ouvert ; (*) ⟺ P = P_max ; Reimbayev) : surtout expositoire.

## 6. Incohérences, erreurs et surventes relevées

1. **Survente corrigée seulement en partie (S31).**
   - Des bandeaux d'erratum figurent dans NOTE_S8, S11 et S17.
   - Mais le REGISTRE (lignes S10, S11, S17, S19) dit encore « EXCLU » ou « tout-tordu pur entièrement exclu ».
   - NOTE_S17 garde l'en-tête « ENTIÈREMENT EXCLU » sous l'erratum. Le JOURNAL du 26/09 dit « Tout tordu fermé ».
2. **Statut de g⁻ non mis à jour.** NOTE_S27 §8 et astra/PROBLEMES_OUVERTS_INVOLUTION.md disent « Démontré… g⁻ ∈ {16,18,20} » et proposent « exclure g⁻ = 16 ». La conclusion postérieure est {18,20} (NOTE_S29 §5).
3. **Erreur de compte.** JOURNAL l. 737 : « Tout est mort pour n_dd ≤ 6 (6 079 classes) ». Les fichiers donnent 1 385 + 4 594 = **5 979**. 6 079 est un compte intermédiaire à n_dd = 8 dans ad/relaxed69.log.
4. **« Démontré, par calcul exact certifiable : AD pour n_dd ≤ 6 »** (NOTE_S28 §6). run_relaxed.py n'enregistre que des verdicts scipy.milp ; aucun certificat n'est stocké pour ces classes.
5. **Ce qui n'est pas reproductible depuis ce dépôt.**
   - « 86/141 » pour O₂₄ : o24_globallp_results.json ne contient que 31 classes (24 exclues, 7 PL-faisables).
   - Les DRAT 33/79 et les contre-vérifications de C2 sont ailleurs.
   - build156.py et verify_frame_cert.py pointent vers `C:/Users/RESEARCHER/Desktop/c1_recherche/data/borcherds_odd24.json`, absent du dépôt.
6. **« Correction PROUVÉE de la table de C1 (id 150) »** : à présenter comme une correction de transcription d'un fichier de données, pas d'une table publiée.
7. **REGISTRE.** L'identifiant S3 est en double, S18 est absent, S2 est « observé » alors qu'une preuve existe dans NOTE_S5 §6. NOTE_S5 a deux sections numérotées « 5 ».
8. **Famille.** Dans « multiplicités entières seulement pour m ∈ {2, 11} », m = 2 donne srg(3,2,1,6), qui est dégénéré (K₃).
9. **Nuances de lecture.**
   - L'avance « test décisif » à 841 est faible : seul Paley est connu.
   - genus_validate.log garde T(5) « INCONSISTENT », non résolu.
   - Les heuristiques (≈ 10⁻¹⁰ ou 10⁻¹⁵ solution, « k = 22 presque sûrement impossible ») ne sont pas des preuves ; le dépôt le dit, mais le langage du JOURNAL peut être surlu.
10. **Erreurs documentées et corrigées en chemin.**
    - Théorème A de C2 (« e′ pair » → impair), trouvée par Astra.
    - « torsion maximale ⇒ e(R) = 0 », dans notes/116 de C1.
    - 83 → 84 certificats ; « quadrilatère » → « étoile + transversale » ; bornes P2o non doublées ; remarque sur Π_K ; « ligne exacte » de NOTE_S29.
11. **Divers.**
    - logs/srgw.txt contient le texte intégral du livre de Brouwer–Van Maldeghem : question de droits si le dépôt devient public.
    - Je n'ai pas vérifié les références arXiv 2026 citées : Ishida 2606.29183, Keramatipour 2604.23037, Thakkar–Severini 2608.11211.