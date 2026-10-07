*Annexe de la note 162 : rapport d’un agent de lecture (07/10/2026), versé tel quel. Les affirmations sur les autres dépôts sont celles du rapport ; voir la note 162 pour la synthèse et les réserves.*

# Inventaire C2 : ce que contiennent les cinq dépôts conway99 (état au 06/10/2026, ~21 h)

J'ai lu les cinq dépôts sans rien modifier. Pour lire `c2_cloud_run.zip` (version v10, sha256 `db8a0e1d…`), je l'ai extrait dans mon espace de travail temporaire. Je n'ai rien exécuté d'autre que des lectures de fichiers JSON.

**Le chiffre « 94/156 au 01/10 » est dépassé.** Selon `conway99-c2-aws/HANDOFF_2026-10-01.md` :
- **142/156** enveloppes sont exclues dans le tracker du labo depuis le 04/10.
- Le 06/10, l'enveloppe 016 a été entièrement calculée sur AWS, mais le résultat n'est pas encore importé au labo.
- 000 (O24), 010 et 004 sont exclues. **001 et 002 restent ouvertes.**

---

## 1. La réduction de C2 à un calcul fini (route C)

### 1.1 La chaîne logique, étape par étape

| # | Énoncé | Comment c'est établi | Où se trouve la preuve |
|---|---|---|---|
| 0 | |Aut Γ| ∈ {1,2,3}. **F0** : toute involution fixe exactement un sommet. Makhnev–Minakova 2004, Th. 1 : « Δ = Fix(g) est un graphe à un sommet et \|g\| = 2 ou 7 ». | Littérature publiée, non re-prouvée ici | Texte russe : `/home/user/conway99-c2-experimental/downloads/profondeur_2409/dm144.txt` ; synthèse : `/home/user/conway99-involution/notes/NOTE_involution_case.md` §1 |
| 1 | **Rigidité.** t retourne chaque bloc de N(x). Aucun sommet extérieur n'est adjacent à son image (a₁(t)=14). χ₃(t)=χ₋₄(t)=0. D(u)=N(u)∩N(σu) est une σ-orbite, donc **D est un couplage parfait des 42 orbites**. | À la main (le retournement est « essentiellement le lemme de Makhnev ») ; relu par deux audits | `NOTE_involution_case.md` §2, `notes/AUDIT_2026-09-22.md` |
| 2 | **Modèle exact sur 42 orbites** : contraintes (R),(D),(I),(P), soit 1722 bits, équivalent à A²+A−12I=2J. Il se décompose en étage Q ∧ étage S ∧ (support de S = {Q=1}). Quotient signé S : S²+S=12I, spectre 3²⁷, (−4)²². | Preuve à la main, plus des contrôles machine : m=2 SAT avec relèvement, m=3 UNSAT, BvLS srg(243,22,1,2) avec 0 violation, CNF m=11 validée au labo le 22/09 | `/home/user/conway99-involution/results/LAB_2026-09-22_summary.md` |
| 3 | **Réseau du repère.** Les 49 vecteurs f_O = √(7/2)·E₋₄(e_x−e_σx) ont pour Gram H = 3I−S, avec H²=7H et rang 22. On a 7 vecteurs h de norme 4 et 42 vecteurs u de norme 3, produits mutuels dans {0,±1}, et un repère serré de constante 7. | Dérivation à la main. `LEMMA_TARGET` §2 avertit : « *reconstructed in this session… check it against the project's own notes* » | `/home/user/conway99-c2-experimental/route_c_29_09/56_PROMPT_ASTRA_ROUTE_C_28_09.md` §1.1 ; `/home/user/conway99-c2-aws/LEMMA_TARGET_2026-10-06.md` §2 |
| 4 | **det N = 7^(22−g), g ∈ {18,20}, discriminant non scindé** (« Théorème B′ » : N = √7·K₋*). | **Donnée d'entrée attribuée à C1 / « structures ». La preuve n'est dans aucun des cinq dépôts.** | Mentionné dans `notes/46_LIGNE_D_ARRIVEE_C2.md` §8 et `UNIFICATION_G18_G20_RANG24.md` §1 |
| 5 | **min N\* ≥ 8/7.** Forme équivalente : aucune fonction propre entière σ-impaire de valeur propre −4 avec Σφ² ≤ 14. Conséquence : Y(α) = (α,y₁)²+(α,y₂)² ≤ 6 pour toute racine. | Preuve à la main par double comptage (m<7 impossible ; m=7 contredit par le sommet fixe) | `/home/user/conway99-c2-experimental/external_inputs/CONWAY_ASTRA_27_09_2026_0836/EXTRAIT/attaque_globale_27_0803/AUDIT_NORME1_ET_METRIQUES.md` |
| 6 | **Enveloppe.** On passe à Nmax (det 49, égal à N si g=20, sur-réseau d'indice 7 si g=18), puis on colle avec J=7I₂. On obtient **U impair unimodulaire de rang 24, avec min U ≥ 2**, qui porte le repère (F) : 7 h ∈ U₀ de norme 4 deux à deux orthogonaux, 42 u ∈ U₂ de norme 3, y₁ ⊥ y₂ ∈ U₂ de norme 7, et Σ f fᵀ = 7I₂₄. | À la main, plus des contrôles exacts en JavaScript ; contre-audit interne Astra ; « relu par structures : tout tient » | `…/attaque_globale_27_0803/UNIFICATION_G18_G20_RANG24.md` |
| 7 | **Classification de Borcherds** : 156 réseaux impairs unimodulaires de rang 24 sans vecteur de norme 1 (id 000 = O24, …, 155). | Externe : données C1 `borcherds_odd24.json`, générateurs « structures » 3eceb4d. Le moteur vérifie à chaque chargement l'unimodularité, la présence de 4096 vecteurs de norme 3 et de r+48 vecteurs d'ombre de norme 2. | `c2_cloud_run.zip` : `external_runs/structures_3eceb4d/U/NNN.json`, `data/finishC/finishC_tracker.json` |
| 8 | **Identités du repère aux « nouvelles racines »** β (vecteurs de norme 2 de l'ombre) : \|(h,β)\| ≤ 1 ; w(β)=Σ_c(h_c,β)² ∈ {1,3} ; w(β)=1 exactement aux points touchés à ±3/2 par un vecteur impair. | Présentées comme « PROVEN » par C1 (notes/140–141). **Preuves absentes des cinq dépôts.** | Brief Astra §1.3 |
| 9 | **Énumération des paires (y₁,y₂)**, complète à Aut(U) × signes près (`y_pairs_gamma.py` de C1 ; repli Γ={I}). Familles Golay : pipeline « structures » et `golay_gen.py`. O24 : 141 classes. | Calcul (une seule implémentation pour la plupart des réseaux) | `c1/code/y_pairs_gamma.py` dans le paquet |
| 10 | **Recherche exacte du repère** (étage 1 : 7 h ; étage 2 : Lemme Z, sommes d'étoiles L7, vérification complète de (F)). | Calcul : `frame_dfs_next.py` (numba). Arithmétique entière, sauf Fincke–Pohst en flottants avec revérification exacte des normes. | `scripts/frame_dfs_next.py`, `scripts/hstage_stream_next.py` |

**Conclusion visée.** Si les 156 enveloppes sont exclues, aucune involution n'existe. Avec C3 (« pas d'ordre 3 », dit prouvé en Lean dans les notes 23 et 41, hors de ces dépôts), on obtient Aut(Γ) = 1.

### 1.2 Formulation, et sens exact d'une exclusion

La ligne d'arrivée du tracker dit : « *C: no odd unimodular rank-24 envelope without norm-1 vectors (Borcherds Table -4) carries the frame (F)* ».

**Le problème de l'étage 1, pour une paire.**
- Les cibles sont t(β)=1 sur les points touchés par y, t(β) ∈ {1,3} (« flex ») là où un u de norme 3 orthogonal à y₁ et y₂ touche β à 3/2, et t(β)=3 ailleurs.
- On cherche 7 h ∈ H deux à deux orthogonaux, avec #{c : (h_c,β) ≠ 0} ∈ t(β) en chaque point.
- On y ajoute le Lemme U+ (cellules Same/Opp), les points de bord et l'étage 2.

**Une enveloppe compte comme exclue de l'une de ces quatre façons :**
1. **Au niveau du réseau** :
   - lemme d'empaquetage de C1 (`envelope_pack.py`) ;
   - budget par composantes de C2 (130, 143) ;
   - critère (E) de C1 (notes/139, appuyé sur les théorèmes thêta de Sol) ;
   - exclusions du dossier Astra « 0836 » : D8³, D_n avec n ≥ 12, E8.
   - C'est le cas de 22 enveloppes dans le tracker du paquet.
2. **Par balayage des paires** : chaque chunk du plan doit être `chunk_ok` (sha256 et nombre de paires égaux à ceux du producteur) et `chunk_done`. Code exact (`hstage_stream_next.py`) :
   `chunk_done = ok and n == #{EXCLUDED*, SWAP-COVERED, TWIN-DEFERRED, TWIN-CANON*}`.
   S'y ajoute, côté labo (`stream_finish.py`, version qui n'est **pas** dans ces dépôts), la condition que toutes les classes jumelles différées soient exclues. D'où la « cascade » de 23 enveloppes le 02/10.
3. **Par LP de repère avec certificats entiers** : O24 (86 classes sur 141), 115, 132.
4. **Par blocs Golay** (`golay_pairs_job.py`) : une paire encore INCOMPLETE est relancée avec 4·10⁹ nœuds.

**Ce qui n'est jamais compté comme exclusion** : `INCOMPLETE` (limite de nœuds atteinte), `INVALID` (y ∉ U, ou assertion non satisfaite), `FRAME FOUND`, et les feuilles non tuées. Aucune « FRAME FOUND » n'a jamais été signalée.

### 1.3 Règles de filtrage du moteur et statut de leurs preuves

| Règle | Énoncé | Statut, et où est la preuve |
|---|---|---|
| Piège caractéristique (FD_CHAR) | z caractéristique de norme 16 ; Σ_f(f,z)²=112 ⇒ (z,y₁)²+(z,y₂)² ≤ 66 | Astra 28/09, « checked by C2 ». Argument court dans la docstring. **Témoin z explicite stocké pour chaque paire** |
| Confinement des extrémités et points de bord (Y_z=58) | Ces z se comportent comme des nouvelles racines non touchées par y | Astra/5.6 du 29/09. Preuve absente |
| Symétrie FD_SYM (28/09) | Réflexions dans les racines orthogonales à y₁, y₂, β₀ ; branchement sur des représentants | Argument donné dans le code (sain : le groupe fixe les vrais repères) |
| FD_SYM2 / FD_SYM3 (01/10) | Brisure de symétrie à toutes les profondeurs ; deux phases avec 10⁴ nœuds | Preuve dans `work/ROUTE_C_SPEEDUPS_2026-10-01.md`, **absent du clone researcher2** |
| Règle d'échange (SWAP) | On saute (y₁,y₂) si I(y₁) > I(y₂), car l'orientation inverse est énumérée | Repose sur la complétude de l'énumération et la symétrie de l'étage 1 |
| Jumeau U⁺ = F(U)+J | Le même repère vit dans U⁺. Si toutes les enveloppes du type de racines de U⁺ sont exclues : EXCLUDED. Si U⁺ est strictement plus riche en racines : DEFERRED | Astra 29/09 §5/7, « checked by C2 ». **Preuve absente**, y compris la complétude de l'énumération des racines de U⁺ (`twin_transfer.py`) |
| TWIN-CANON (01/10) | Si U⁺ ≅ U (type de racines unique) et que la clé intrinsèque k est plus petite, on saute | Preuve dans `ROUTE_C_SPEEDUPS` (absent) |
| Lemme Z, sommes d'étoiles L7 | Σh ∈ 2U ; Σ des 12 mots d'une étoile = 3h_c | C1, preuves externes |
| **FD_MIN97 (v10, 04/10)** | On tue la paire s'il existe x de norme 3 avec (x,y₁)²+(x,y₂)² = 13 (projection de norme 8/7 < 9/7) | Repose sur **min L\* ≥ 9/7**, dans `work/VERIF_CUBE_OBSTRUCTION_2026-10-04.md` et `DOSSIER_WAGNER_2026-10-04` : **ni l'un ni l'autre n'est dans les dépôts**, et `T18_REPORT.md` dit ne pas les avoir trouvés. Témoin x stocké |
| Budget par composantes, budget par paire (ILP), empaquetage, critère (E) | Contraintes de niveau réseau | C2 / C1 ; « run + argument re-read by C2 » |

### 1.4 État d'avancement

**Chronologie du nombre d'enveloppes exclues** :
- 47 le 28/09, 58 le 29/09 ;
- 94 le 01/10 (import des 399 jobs AWS) ;
- 106 le 02/10 vers 02:30, heure de Paris ;
- 107 avec **O24 (000) exclue** le 02/10 vers 01:10 UTC : 86 certificats LP, 8 classes calculées au labo, 47 sur AWS, toutes vides ;
- 108 avec **010 exclue** le 02/10 vers 02:30 UTC ;
- 109 avec 059 ;
- **132** après la cascade du 02/10 vers 14:50 UTC ;
- 133 avec **004** (416 383 classes de paires) ;
- 134 à 139 avec 026, 028, 024, puis 023, 020, 021 ;
- 140 avec 018 le 03/10 ;
- **142** avec 019 et 017 le 03/10 à 23:31 UTC.

**Restent 14 enveloppes** : 001 et 002 (famille Golay), 003, 005, 006, 007, 008, 009, 011, 012, 013, 014, 015, 016.
- 016 est entièrement calculée en v10 (479/479 jobs, aucune paire INCOMPLETE), mais pas encore importée.
- 012 est entièrement balayée ; elle attend 013 à 016 (paires différées vers des jumeaux).
- Le 06/10, 013 en était à 958/999 jobs.

**Coûts.**
- Le 01/10 : 295 heures-machine, environ 91 $ (rapport réel/estimé de 1,30).
- Le 02/10 : 5 500 à 8 000 heures-job. Rapports mesurés : 1,9 pour 011, 2,9 pour 014, 5,5 pour 002, environ 30 pour les blocs de 001.
- Le 03/10 : environ 2 500 heures-job perdues à cause des interruptions Spot.
- Le 06/10, sans nouveau lemme : **5 000 à 9 000 heures-cœur, 60 à 100 $**.
- Facture réelle du premier compte : 76,77 $ en septembre, 120,34 $ en octobre, crédits épuisés.

**Cible de lemme (`LEMMA_TARGET_2026-10-06.md`).**
- Parmi les paires réellement fouillées, Emin=9 (une racine r avec {|(r,y₁)|,|(r,y₂)|}={1,2}) représente 68 à 89 % des paires et 64 à 92 % des nœuds.
- Prouver min L\* ≥ 10/7 (**T18**) supprimerait 64 à 92 % du temps de recherche ; prouver ≥ 11/7 (avec **T20**) en supprimerait 99 à 100 %.
- Où en est T18 :
  - Prouvé à la main : loi de parité e ≡ C(k,2) (mod 2) ; e=1 et e=2 impossibles ; motif (ii) impossible ; **trois graphes B0=K3×K3, B1, B2=C9(1,2)** ; n₃=0 ; profil (4,1,2) exclu.
  - Profil (3,3,1) : exclu par calcul. Une seule implémentation pour B0 et B1 ; pour B2, une seconde implémentation (`t18_VERIF331`) confirme jusqu'à 51 sommets.
  - Profil (2,5,0) :
    - B1 : 4 survivants à 47 vertices (rapport). Le fichier brut `lemma/t18_B2/d_stage_B1check.out` indique « 0 configurations on 55 vertices left » (étage D, seconde implémentation), **mais aucun rapport ne le consigne**.
    - B2 : 0 survivant à 47 sommets, deux implémentations concordantes.
    - **B0 : étage C fait sur 588 des 2 667 représentants seulement : ouvert.**
  - T20 : à peine commencé (cas III : 2 classes survivent au niveau S ; cas IIb : vide ; IIa et I non faits).
- **Mode « report » des paires** (`defer-mode`), qui mettrait de côté les paires que T18/T20 tueraient : conçu, **non déployé**, et ne compte rien comme exclu.

---

## 2. Les autres découvertes

### 2.1 conway99-involution

| Résultat | Type | Statut | Nouveauté (selon les documents) |
|---|---|---|---|
| Couplage D et modèle exact (R),(D),(I),(P) | Théorème et modèle | Prouvé ; code relu ligne à ligne ; validé sur BvLS | « What appears to be new » |
| Rang F₂ : rang(Γ̄+Nb Nbᵀ) = 20 | Théorème | Prouvé. **Conséquence du modèle, pas une obstruction indépendante** (corrigé le 22/09) | — |
| Spectres : S_out = {0⁷,3²⁰,(−4)¹⁵} ; Q_out = {12,(−2)⁶,3²⁰,(−4)¹⁵} ; H de tout Conway-99 enraciné = {12,(−2)⁶,0⁷,3⁴⁰,(−4)³⁰} | Théorèmes | Prouvés (`DEEP_THOUGHT`) ; le dernier « probably known implicitly » | Faible |
| #triangles(Γ₁) = 126 + 4n_sib + 2n_one ; c₄ = 2079 est constant | Identités | Prouvées. L'ancienne « congruence nouvelle » était vide et a été retirée | — |
| **Audit Reimbayev (arXiv:2608.19410)** : 4 coquilles (z₂₁, z₈₀/z₈₄, z₁₇₆). Une fois corrigées, Σz_i = C(n,7) et le recensement ne donne aucune contrainte (0 ≤ n₃ ≤ 4158) | Résultat négatif et erratum | Revérifié hors ligne | Oui (erratum) |
| Remarque bibliographique : le cas Z₇ à un point fixe était déjà fermé en 2009/2011 (Thakkar–Severini le disent « ouvert ») | Littérature | Vérifiée sur les sources | Oui (correction) |
| Découpages sib/one/dis exhaustifs ; cubes 13 (9 distincts) / 149 / 1 164 | Calcul | Exact | — |
| SAT et CP-SAT sur le modèle entier | Calcul | Tous UNKNOWN ; le log `one10` UNSAT est **vide par construction, ne pas citer** | — |

### 2.2 conway99-c2-experimental (notes 00 à 46, entrées Astra)

**Résultats généraux, hors involution.**
- **G1** : dans un srg(99,14,1,2), toute grille 3×3 est un code parfait. Dans la famille srg(n,k,1,2), cela n'arrive que pour k ∈ {4,14}.
  - Type : théorème démontré dans la note.
  - Antériorité : application du lemme de Wilbrink–Brouwer (via Lou–Murin 2014) ; l'énoncé « k ∈ {4,14} » et la lecture en ensemble intrigant sont présentés comme propres au labo.
- Prismes : n₃ < 2079 ⇒ il existe une grille ; n₃ ≥ 2079 − 9N ; P ≥ 6N.
- Parité du 7-rang : rang₇(A−3I) est impair et D₇(N₃) est de type moins. « Antériorité non trouvée (argument classique) ».
- Formule locale de l'invariant d'Arf, vérifiée sur 50 cas sur 50 (note 24).

**Propre à C2, statut DÉRIVÉ, preuves écrites.**
- Lemme S1.
- Théorème 17.1 (allsib impossible, via H¹(M₇;Z₂)=0), revérifié.
- **Lemme des étoiles** : deg Σ ≤ 2 et |Σ| ≤ 4 ; ses 18 ingrédients sont certifiés DRAT.
- Lemme de la queue et Théorème 25.3 (« aucune configuration ancrée »), revérifiés par « structures ».
- Notes 26 à 30 : M1, H = H-β, règle typée.
- Lemme 42.4 ; lemme (★) d'équilibre général.

**Calculs certifiés.**
- Σ ∈ 10 survivants (DRAT vérifié par drat-trim).
- **H-β impossible** : 552 classes sur 552, certificats de Farkas rationnels ; recontrôle par « structures » sur 8 certificats sur 8.
- M1 avec n = 3, 4 et 6 fermés ; AD2 fermé ; tout-tordu exclu (triple vérification) ; famille ancrée des motifs Σ ≠ ∅ morte.
- **La route locale n'est pas fermée.** Restent M1 n=5 (job 10), les mélanges des classes 15, 16 et 18 à 46, et les carrés « dis ». Ligne (A) : 1 507 types et 77 838 cubes, tous INCONNUS à 5 min. **Route suspendue au profit de (C).**

**Résultats négatifs utiles (N01 à N24).**
- Les invariants de genre, de Brown et d'Arf ne fournissent pas d'obstruction (« HEURISTIQUE » après revue).
- Les relaxations de moments de degré 2 et 3 sont réalisables à m=7, même pour allsib.
- Les PL par paires laissent de vrais survivants (note 40).

**Dossier Astra (entrées externes, auditées par Astra, en partie relues par « structures » et C1).**
- Enveloppes D8³ impossibles ; aucun D_n avec n ≥ 11 ; rang des racines ≤ 20 ; pas de E8.
- Dans D6⁴, la strate (6,0) est impossible.
- Théorèmes thêta : #χ₈ = 48+r ; la coque de norme 3 compte 4096 vecteurs.
- Une enveloppe sans racines force le gabarit d'un code [24,12,8].
- **Contre-modèle** : réseau de det 49, minimum 3, sans racines. Il montre que le genre et les minima seuls ne suffisent pas.

### 2.3 conway99-c2-campaign

| Résultat | Type | Statut |
|---|---|---|
| **T4** : pour N complet, L_N est vide ou réduit à un couplage entier unique | Théorème | Preuve écrite ; « blind audit » déclaré, **mais le rapport d'audit n'est pas joint** |
| **Théorème C** : système couplé (Q,N) à 4 états | Reformulation exacte | Prouvé, non audité |
| Lemme de résidu borné (mod 3 + capacités ⇒ équations entières) ; formulation par projecteur ternaire ; exclusion d'une famille particulière ; contre-modèle sur F₃ | Théorèmes et contre-modèle | Vérifiés une fois ; **famille non exhaustive** |
| Cartes de réponse non compressives ; registre des échecs (22 bassins) | Résultats négatifs | Prouvés |

### 2.4 conway99-c2-researcher2

**Résultats R1 à R21** (`work/RESULTS.md`).
- **Redécouvertes de résultats existants** : R1 à R4, G0, E′, R9, P7.
- **Nouveaux selon les documents** :
  - Théorème A : les carrés de type 1 sont rigides ;
  - Lemme CM ;
  - **T1S est faux au rayon 1** : contre-configuration explicite K3, vérifiée par deux programmes ;
  - calcul du « twist » : densité 8/(m−3), loi de capacité de fuite (BvLS extrémal), 7 | τ si K=0 ;
  - fenêtre de fuite (R21).
- Résultats calculés :
  - support des cellules de type 2 : 133 classes, n₂ ≤ 10 ;
  - passe SAT : 102 classes sur 133 exclues, **résultat rapporté par le solveur, sans certificat** ;
  - aucun N invariant pour environ 25 groupes, deux implémentations.
- **Aucune exclusion de branche. EX reste ouvert.**

### 2.5 conway99-c2-aws (hors calcul)

- `LEMMA_TARGET` et le dossier `lemma/` : voir § 1.4.
- **Théorème N3** (n₃ = 0, à la main), dans `lemma/t18/N3_REPORT.md`.
- Certificats de semi-définition positive en entiers : 50 000 sauvegardés et revérifiés ; environ 1,1 M non sauvegardés.
- Mesures de coût v10 : `measures/V10_TIMINGS_2026-10-06.md`. Le poids d'un job suit I(y₁) = Σ_racines (r,y₁)².
- Loi K + E(y₁) + E(y₂) = 3|Φ|/4 + 8 (étude de cascade). **Le fichier source n'est pas dans le dépôt.**
- Outillage d'exploitation : file d'attente atomique, plafond de dépense, interrupteur « homme mort », découpeur `par_consumer.py` validé contre des enregistrements AWS.

---

## 3. Incohérences, erreurs et risques pour la validité du calcul

### A. Preuves absentes ou externes — à archiver avant toute publication

1. **Étape 4** (det N = 7^(22−g), discriminant non scindé, Théorème B′) : aucune preuve dans les cinq dépôts.
2. **Notes 139 à 145 de C1** (identités aux nouvelles racines, Lemme U+, critère (E)) : la chaîne en dépend entièrement, et ces notes sont absentes.
3. **Lemmes Astra du 28/09 et du 29/09** : points de bord et jumeau U⁺, y compris la **complétude de l'énumération des racines de U⁺**. Une racine oubliée donnerait un mauvais type de racines, donc un « EXCLUDED (twin transfer) » faux.
4. **Preuves de FD_SYM2/3 et de TWIN-CANON** : le fichier `ROUTE_C_SPEEDUPS_2026-10-01.md` est absent. La combinaison SWAP, TWIN-CANON et report vers les jumeaux doit être justifiée par un ordre bien fondé écrit explicitement.
5. **Le lemme min L\* ≥ 9/7 est entré dans le moteur v10 le jour même de sa découverte** (04/10). Sa preuve (VERIF_CUBE et DOSSIER_WAGNER) n'est pas archivée, et aucune vérification indépendante n'est consignée. C'est en contradiction avec la règle que le projet s'impose pour T18 : « *Nothing of T18/T20 may enter the engine… until proved and independently checked* ».
   - Les 142 exclusions actuelles précèdent v10.
   - **En revanche, 016 et toutes les exclusions futures (013, 014, 015, 002, …) en dépendent.**
6. **Le script `stream_finish.py` qui résout les reports vers les jumeaux n'est pas dans ces dépôts.** La copie du 29/09 (`route_c_29_09/scripts/`) ne gère pas les jumeaux, et le `hstage_stream.py` de cette date non plus. Cette copie n'est donc pas le moteur qui a produit les exclusions.

### B. Vérification et indépendance

7. **Politique « sweep-first »** (citée dans le tracker) : « *stage (a) done on every pair COUNTS AS EXCLUDED; no re-checks unless they can yield a speed-up lemma* ».
   - Il n'y a ni seconde énumération des paires (b), ni second étage h indépendant (c), sauf sur des échantillons (124 et 126 ; 087, 115 et 132 ont plusieurs lecteurs).
   - Les exclusions par « stage 1 empty » ne portent **aucun certificat** : seuls les verdicts du piège caractéristique et de min97 portent un témoin.
8. **Aucun contrôle positif du moteur complet.** Le brief le reconnaît : « *empirical tests cannot detect an unsound filter* ». La seule mitigation est la relaxation « y₁ seul », qui a des millions de solutions.
9. **Moteur hétérogène.** Les exclusions reposent sur les versions v1 à v10 du moteur et sur des découpages en chunks mélangés (« *accept mixed chunkings by coverage* », alors que la règle initiale l'interdisait). Pour un énoncé 156/156, il faudra soit un audit de chaque version, soit une ré-exécution complète avec un moteur unique.
10. **Dépendances flottantes.**
    - Les matrices Γ dépendent d'une réduction LLL en flottants (« *valid only on the machine that computed it* ») ;
    - Fincke–Pohst fonctionne en flottants avec une marge de 1e-7 ;
    - les nombres de nœuds varient selon le CPU (argsort non stable) ;
    - **une machine ARM a échoué à la calibration (STOP CALIB) et la cause n'a pas été cherchée** ;
    - la calibration ne compare que les verdicts.
11. Les « DRAT VERIFIED » du labo expérimental sont des lignes de journal : `cert_run.sh` **efface les preuves**. La passe SAT de researcher2 n'a aucun certificat.
12. L'audit de T4 est « rapporté », mais les fichiers de l'auditeur ne sont pas joints.

### C. UNKNOWN et UNSAT

- La discipline est bonne : INCOMPLETE et INVALID ne sont jamais comptés comme exclus, `chunk_ok` exige le sha256, et `scan_incomplete` a été ajouté.
- Mais **118 paires INCOMPLETE sont passées inaperçues un temps** (023, 024, 026, 028). Elles ont bloqué ces enveloppes sans fausse exclusion.
- Un résolveur lancé avec un `timeout` trop court a été tué en cours de route.

### D. Incohérences documentaires

- **Compte des enveloppes exclues selon les sources.**
  - Le dépôt campaign donne 91/156 et environ 6 600 heures CPU, en signalant lui-même qu'il faut réconcilier.
  - Le README AWS donne 94/156 et cite le paquet v1 (sha256 `263ab75b`), alors que le zip du dépôt est v10 (sha256 `db8a0e1d`).
  - Le tracker embarqué dans le paquet donne 102 ; le HANDOFF donne 142.
- La section 15 du HANDOFF dit « B1 : 4 configurations » alors que `d_stage_B1check.out` en donne 0. Elle est datée « 21:15 UTC » alors que le commit date de 20:58 UTC.
- Deux instantanés de mesures sur 016 diffèrent : 440 625 paires retirées par le filtre et 258 580 fouillées d'un côté, 511 844 et 343 606 de l'autre.
- researcher2 écrit « *Not found: a primary source for F0* », alors que M–M 2004, Th. 1 est cité et présent dans les fichiers.
- La docstring de `frame_dfs` dit « *only the rigid case is implemented* », ce qui est périmé.
- Les enregistrements fusionnés par `par_consumer.py` portent `"machine": "labpc"` en dur, ce qui fausse la provenance des résultats AWS.

---

## 4. Ce qui est publiable maintenant, et ce qui l'est après la fin du calcul

**Publiable maintenant**, après relecture humaine :
- **Article I — branche involution, structure exacte.** Rigidité, couplage D, modèle exact sur 42 orbites validé sur BvLS, T4, Théorème C, lemme ternaire de résidu borné. Il faut d'abord produire le rapport d'audit de T4 et créditer Makhnev pour le retournement.
- **Article II (court) — les grilles comme codes parfaits.** G1 (k ∈ {4,14}), ensembles intrigants, bornes n₃/N/P. Éventuellement avec la parité du 7-rang. La recherche d'antériorité reste à faire.
- **Note III — erratum Reimbayev.** À communiquer à l'auteur.
- *Optionnel* : un rapport technique sur la combinatoire locale de C2 (allsib, lemme des étoiles, queue, H-β avec certificats). Il est partiel ; sa valeur est surtout méthodologique si la route C aboutit.

**Après la fin du calcul :**
- **Article IV — « Conway's 99-graph has no involution ».** Il contiendrait :
  - la chaîne complète des étapes 1 à 10, avec le Théorème B′, min N\* ≥ 8/7 et l'enveloppe ;
  - les exclusions de niveau réseau (Astra, C1 : D8³, D_n ≥ 12, E8, empaquetage, budget par composantes) ;
  - **toutes les preuves de filtres archivées** (piège caractéristique, points de bord, jumeau, SYM2/3, TWIN-CANON, Y≤6, 9/7) ;
  - min L\* ≥ 10/7 (T18) et, si possible, 11/7 (T20), qui ont aussi un intérêt en soi pour les fonctions propres σ-impaires ;
  - le calcul, publié avec un manifeste vérifiable : les données des 156 réseaux, avec un contrôle par la formule de masse ou d'isomorphisme non documenté ici ; un moteur figé ; une seconde énumération des paires et un second étage h, au moins sur un échantillon stratifié, idéalement complets ; les certificats LP et les témoins.
- Avec C3 (preuve Lean externe à ces dépôts), le corollaire serait **Aut(Γ) = 1**, à présenter dans le même article ou dans un article commun avec C3.

**Avant de pouvoir écrire 156/156**, la liste d'attente est : archiver les preuves A.1 à A.6, faire vérifier indépendamment le lemme 9/7, trouver la cause de l'échec de calibration ARM, et réaliser les lectures (b) et (c) des listes de paires.