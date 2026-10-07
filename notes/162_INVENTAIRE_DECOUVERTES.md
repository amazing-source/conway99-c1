# 162 — Inventaire des découvertes des 12 dépôts Conway (07/10)

*Demande de l'utilisateur : regarder en détail tous les dépôts Conway, dont les éléments sur les tables de Brouwer du
dépôt structures. Cinq agents de lecture ont lu les 12 dépôts : c1, c2-aws, c2-experimental, c2-campaign,
c2-researcher2, involution, c3, c3-experimental, conway-C7, structures-lab, rank17 et lab-archive. Leurs rapports
complets sont dans `162_annexes/` (A à E). Cette note donne la synthèse, mes vérifications propres et les réserves.
Rien n'a été modifié dans les autres dépôts.*

## 1. Les résultats forts (nouveaux, ou nouveaux par la méthode)

| # | Résultat | Statut de vérification | Nouveauté | Où |
|---|---|---|---|---|
| 1 | **Pas d'automorphisme d'ordre 3** dans srg(99,14,1,2) (C3) | Preuve **sans ordinateur** par obstruction de discriminants (Z₃[C₃], norme 33 = 3·11 qui injecte 11, non carré mod 3). **Lean 4 complet** : 3 754 lignes, aucun `sorry`, axiomes standard, `comparator --paranoid` sous bac à sable GitHub Actions (run 35880776817, succès confirmé par l'API). Scripts relancés par l'agent. | **Nouveau** : la littérature s'arrêtait à Aut ∈ {1, Z₂, Z₃}. Aucune relecture humaine. | c3-experimental (`c3formal/`, `pdf/preuve_c3.tex`) ; annexe B |
| 2 | **Pas d'automorphisme d'ordre 7, sans ordinateur** (C7) | Article de 14 pages. Lean par recensement fini (`decide +kernel`, 29 blocs), pas par l'analyse à la main des §§ 6–8. Comparateur seulement sans bac à sable. L'agent a refait indépendamment la recherche 12×12 : 0 solution, contrôle positif OK. | **Nouveau par la méthode** : Behbahani–Lam 2011 l'excluaient par ordinateur, et Cesarz–Woldar 2025 s'arrêtaient à G = Z₇ sans ordinateur. | conway-C7 ; annexe B |
| 3 | **Second srg(243,22,1,2)**, tordu (n₃ = 19 440), qui réfute la conjecture des hexagones de Reimbayev et la conjecture F2-SRG / F20 (« tout PQ(2,t,2) SRG est grid-full ») | Vérificateur autonome, nauty, comptage direct d'hexagones | Nouveau (unicité de BvLS ouverte ; table de Brouwer : un seul graphe) | c1 notes 158–160, `data/srg243/` |
| 4 | **Critère 2-adique S5** : si d = r − s est impair et E_θ 2-entier, Λ_θ est pair de déterminant impair, d'où (−1)^{m_θ/2}·det Λ_θ ≡ 1 (mod 4) et det Λ_θ = ∏_{q\|d} q^{c_q}·P_θ. Il **exclut 35 jeux de paramètres marqués « ? » dans la table de Brouwer** (v ≤ 1300), la famille infinie **NL_e(n), e impair, tous les premiers de n ≡ 1 (mod 4)**, et 185 jeux jusqu'à v = 5000 | Preuve relue **par moi ligne à ligne : correcte**. Relue par C2 et auditée par Astra (deux implémentations). 0 graphe existant exclu sur 1 183. Redonne (289,54,1,12) = NL₃(17) en 5 lignes : c'est exactement le membre inexistant de la famille de Bondarenko–Radchenko 2013 ; les membres 81 et 729 passent. | Lemme de réseau classique (Martinet 2003). **Ma recherche bibliographique ne trouve pas le critère ni ces exclusions.** Avis d'expert nécessaire. | structures `NOTE_S5_DISCRIMINANT_MOD4.md` ; annexe A |

**Corollaire possible de 4** (ma lecture, non écrite dans le dépôt). (750,210,55,60) a pour valeurs propres 10 et −15,
donc d = 25, et pour multiplicités 441 et 308. Pour θ = −15, P_θ = 3 et (−1)^{154}·3 ≡ 3 (mod 4) : le critère
l'exclut. Or le graphe des points d'une pg(14,14,4) a exactement ces paramètres (« pg(14,14,4)? » dans la table) :
**pas de géométrie partielle pg(14,14,4)**, si S5 est confirmé.

**Énoncé combiné sans ordinateur (1 + 2)** : |Aut Γ| ∈ {1, 2, 11}, et même {1, 2} si l'exclusion de l'ordre 11 par
Wilbrink 1984 est confirmée à la source comme sans ordinateur. Avec Behbahani–Lam : |Aut Γ| ∈ {1, 2}. **Cet énoncé
n'est écrit nulle part** : le Cor 8 de C3 ignore C7, et le Cor 1.2 de C7 ignore C3.

## 2. Résultats solides de second rang (publiables après mise en forme)

**C1, arithmétique et torsion** (annexe D).
- **25 ≤ rang₇(A − 3I) ≤ 43, impair.** La borne connue était 45 (van Eijl, Brouwer–van Eijl). Lemmes utilisés :
  - L22 et L20 bis, à la main ;
  - L20 ter, assisté par ordinateur et petit ;
  - L21 et L23.
- **L16 : P ≤ 1151** (Krein cubique sur les droites). **L18** : la seconde variable libre de Reimbayev est S. « Mur L16 »
  jusqu'à l'ordre 8.
- **L8 : aucun point de Hamming** (squelette de Fano). Aussi L7 et g(x) ≤ 17.
- **L25** : tissu de 11 grilles ⟺ plan projectif d'ordre 10 avec polarité, exclu par Lam.

**C2, involution** (annexes C et E).
- Rigidité et couplage D, modèle exact à 42 orbites, g⁻ ∈ {18, 20}.
- Réduction rang 17 (A1–A8), théorème caractéristique (228 classes fermées), min N* ≥ 8/7.
- **Route C : 142/156 enveloppes exclues** (handoff du 04/10). 016 est calculée mais pas importée ; 001, 002 et 003–015 restent.

**Famille λ = 1, μ = 2.**
- **Rigidité de Godsil–McKay** : srg(v,k,1,2) avec k ≥ 8 n'a aucun ensemble de commutation GM non trivial. Le second
  243 n'est donc pas un switching GM, et notre bascule de triangle est d'une autre nature.
- **G1** : toute grille 3×3 d'un srg(99,14,1,2) est un code parfait, et dans la famille seulement pour k ∈ {4, 14}.

**Autres jeux de paramètres** (annexe B). Critère p = 3 de C3-experimental : il exclut une action libre d'ordre 3 pour
plusieurs « ? » de la table, par exemple (105,52,21,30) et (714,248,97,80). **Le théorème général reste à écrire.**

**Notes mineures.**
- Erratum de Reimbayev, arXiv:2608.19410 : 4 coquilles. Une fois corrigé, la liste ne donne aucune contrainte. C'est
  à envoyer à l'auteur plutôt qu'à publier.
- Géométries tordues non SRG (familles tri-incidence, 42 sommets).

## 3. Réserves qui conditionnent toute publication

1. **Aucune relecture humaine nulle part.** Les audits sont faits par des modèles (Claude, Astra, Sol, ChatGPT). Les
   preuves Lean de C3 sont la meilleure garantie disponible ; pour tout le reste, il faut un relecteur humain.
2. **Paternité.** L'article C7 nomme « ChatGPT and Claude » comme auteurs, ce qui est incompatible avec les politiques
   d'arXiv et des revues. Il faut un auteur humain responsable et une déclaration d'usage de l'IA.
3. **La route C n'est pas encore publiable comme 156/156.** Plusieurs preuves dont dépend le moteur ne sont archivées
   dans aucun dépôt :
   - le Théorème B′ ;
   - les notes 139–145 de C1 ;
   - le jumeau U⁺ d'Astra ;
   - SYM2/3 et TWIN-CANON (fichier `ROUTE_C_SPEEDUPS` absent) ;
   - `stream_finish.py`.

   S'y ajoutent d'autres fragilités :
   - **le lemme min L* ≥ 9/7 est entré dans le moteur v10 le jour même, sans vérification indépendante**, alors que 016
     et toutes les exclusions futures en dépendent ;
   - les versions du moteur sont hétérogènes (v1–v10) et la plupart des exclusions n'ont pas de certificat ;
   - un échec de calibration sur ARM n'a pas été expliqué.
4. **Ordre 7 : incohérence documentaire, tranchée.** Behbahani–Lam excluent l'ordre 7 **par ordinateur**, et
   Cesarz–Woldar n'obtiennent que G = Z₇ **sans** ordinateur. Il n'y a donc aucune contradiction, et la preuve C7
   comble exactement ce manque. Les notes de C1 qui écrivent « |Aut| ∈ {1, 2} » s'appuient sur Behbahani–Lam.
5. **Documents périmés.**
   - Le README de conway99-c3 dit encore « Rien n'est encore décidé ».
   - Le README et le rapport de c1 s'arrêtent au 25/09.
   - Le REGISTRE de structures dit encore « EXCLU » pour des cas rouverts par l'erratum S31.
   - Plusieurs anciennes notes de c1 tiennent F20 ou « unicité de BvLS ouverte », que le second 243 rend fausses.
6. **Hygiène avant de rendre des dépôts publics.**
   - `structures/logs/srgw.txt` contient le texte intégral du livre de Brouwer–Van Maldeghem (droits d'auteur).
   - c3-experimental redistribue des données tierces (texte d'Ishida, pages de la table) et des binaires.
   - conway-C7, c2-campaign et c2-researcher2 sont **déjà publics**.

## 4. Découpage en articles (révisé)

| Article | Contenu | Préalables |
|---|---|---|
| **A. Automorphismes** | C3 (nouveau, Lean) + C7 sans ordinateur + énoncé combiné \|Aut\| ∈ {1, 2, 11}, ou {1, 2} | relecture humaine ; paternité ; vérifier Wilbrink 1984 |
| **B. Second srg(243,22,1,2)** | graphe, bascule de triangle, torsion, réfutations de Reimbayev et de F20, lien avec la rigidité GM | prêt (vérifiable par ordinateur) |
| **C. Critère 2-adique** | S5 : 35 « ? » de la table de Brouwer, famille NL_e(n), 185 jeux ≤ 5000, (289,54,1,12) en 5 lignes, corollaire pg(14,14,4) | avis d'expert sur la nouveauté (Brouwer) ; citer Martinet |
| **D. Arithmétique 7-adique et torsion de Γ₉₉** | 25 ≤ rang₇ ≤ 43, L16, L18, L8, L25 | rédaction ; DRAT pour L20 ter |
| **E. Pas d'involution** (plus tard) | route C complète | archiver les preuves listées au point 3, vérifier 9/7, moteur unique, seconde lecture |

Avec A + E : **tout graphe de Conway a un groupe d'automorphismes trivial.**
