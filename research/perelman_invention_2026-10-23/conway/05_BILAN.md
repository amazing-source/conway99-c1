# 5. Bilan : ce que la transposition a donné, ce qu'elle exclut, et la question de fond

Statuts : **[P]** démontré · **[L]** littérature · **[E]** calcul reproductible · **[A]** analogie · **[C]** conjecture ·
**[O]** ouvert.

---

## 5.1 Les cinq conditions de transfert, une à une

| condition (premier travail, partie V) | verdict pour Conway-99 | où |
|---|---|---|
| T1 : évolution canonique non triviale | **échoue sur l'objet, démontré**. Toute fonctionnelle spectrale ou 2-locale est constante, et les flots de Ricci discrets ne font que changer l'échelle | Théorème A.1, §2.2 |
| T2 : notion d'échelle | **absente sur l'objet** (diamètre 2). Présente sur la classe 𝒦₁₄ (diamètre ≤ 9) | §2.5 |
| T3 : substitut de compacité | **satisfaite** : c'est l'intégralité. b₁ = 0 sur ℝ partout, alors que la torsion H¹(𝔽₃) distingue les graphes | §4.1 |
| T4 : rigidité des cas d'égalité | **satisfaite au sens fort** : les égalités en k − 14 sont imposées par les paramètres. Mais aucune monotonie connue n'en fait ses cas d'égalité | §4.2 |
| T5 : invariant topologique | **construit, calculé, et vide pour Conway**. Le type prédit (simplement connexe) est réalisé par les srg(243) sans étalement Γ₅ à Γ₈ | §3.6–3.7 |

Les deux conditions satisfaites sont exactement celles que la campagne exploite déjà. La lecture perelmanienne retrouve la
méta-leçon de l'équipe (arithmétique + positivité + intégralité) ; elle ne la dépasse pas.

---

## 5.2 Résultats, par statut

**Démontrés [P]**
1. *Théorème A.1* : no-go pour toute dynamique naturelle sur un srg(v, k, 1, 2).
2. *Théorème A.3* : courbure d'Ollivier sur les non-arêtes, κ₀ ∈ {(k + 2)/(2k), (k + 1)/(2k)} selon la parité
   d'appariement η. C'est le seul invariant de courbure non fixé par les paramètres.
3. *Corollaire 2.2* : Conway = membre minimal de 𝒦₁₄. Le non-effondrement à l'échelle 3 équivaut au problème.
4. *Lemme 3.1 et Corollaire 3.2* : boucles courtes, revêtements dans 𝒦_k, déplacement ≥ 5.
5. *Théorème 3.3* : π₁(X) fini, |π₁(X(Conway))| ≤ 82 859, et ≤ 22 sous (L).
6. *Théorème 3.4* (géométrisation) : srg(v, k, 1, 2) = modèle de 𝒦_k simplement connexe / groupe libre à orbites 2-codes
   parfaits.
7. *Corollaire 3.5* : grid-full ⇒ v ∈ {9, 243} (avec van Lint–Tietäväinen).
8. π₁(X(BvLS)) ≅ code de Golay ternaire ≅ (ℤ/3)⁶.
9. *Théorème 3.6* (jauge radiale) : H¹ vit sur les cycles des graphes d'appariement d'une seule 2-boule.
10. *Proposition 3.8* : les étalements réguliers donnent des classes non nulles de H¹(X; 𝔽₃).
11. *Proposition 4.1* (excès d'entrelacement) et *Lemme 4.2* (rang saturé) : des réorganisations.
12. *Proposition 4.3* : le lemme impair est la conclusion « pas de respirateur » de S1, et le cas ouvert d'ODD-PURE est
    exactement là où le mécanisme s'arrête.

**Littérature [L]** : κ_LLY = 3/k (Li–Liu 2021) ; diam ≤ ⌊2k/3⌋ (Huang–Liu–Xia 2024) ; Bonnet–Myers de Lin–Lu–Yau ;
van Lint–Tietäväinen ; BvLS = graphe des classes du code de Golay ; Makhnev 1988.

**Calculs reproductibles [E]**
1. π₁ des huit srg(243) connus : (ℤ/3)⁶ pour BvLS ; ℤ/3 pour le jumeau, Γ₃ et Γ₄ ; trivial pour Γ₅ à Γ₈.
2. **Loi « π₁ ≠ 1 ⟺ étalement régulier »** sur les huit graphes ; H¹(𝔽₃) engendré par les classes d'étalement.
3. Trois nouveaux membres simplement connexes de 𝒦₂₂ à 729 sommets, cospectraux, non isomorphes, à spectre de voltage du
   type Hamming 22 − 3j.
4. Distribution de η et des cycles d'appariement sur dix graphes.
5. Réfutation de la loi « A − kI nilpotente mod 3 » par t2 et t3.

**Conjectures [C]**
1. *Conjecture 3.10* : H¹(X(Γ); 𝔽₃) est engendré par les classes d'étalement ; en particulier, X(Conway) est
   simplement connexe.
2. *Propriété (L)* et la borne |V| ≤ 3ⁿ dans 𝒦_{2n}, analogue du théorème de Mulder.

**Analogies [A]**
- Géométrisation de Thurston : H(11, 3) comme espace plat, les codes parfaits comme réseaux.
- La résonance k = 14 comme équation de soliton.
- η comme caractère d'orientation.
- Torsion comme courbure positive, à la Bochner, pour ODD-PURE.

**Ouvert [O]**
- La forme précise de l'ingrédient manquant d'ODD-PURE (§4.3(e)) : une fonctionnelle sur les blocs, invariante par V₄,
  qui contrôle l'asymétrie et contient un terme de torsion nul sur les grilles.

---

## 5.3 La question de fond

> Peut-on comprendre une invention mathématique majeure assez précisément pour en extraire des principes de découverte
> réutilisables, puis les tester sur un autre problème ouvert ?

**Oui pour l'extraction.** Les schémas S1–S10 du premier travail ont des hypothèses vérifiables. Plusieurs ont déjà été
transférés avec succès hors du flot de Ricci : Huisken, Colding–Minicozzi, Andrews, Haslhofer–Kleiner, Brendle–Huisken.
Leur généralité est réelle.

**Le test sur Conway-99 est informatif, et négatif en un sens précis.**
- Chaque hypothèse a pu être vérifiée. Trois échouent avec preuve ou exemple : T1 et T2 sur l'objet, T5 par les
  exemples Γ₅ à Γ₈. Deux tiennent, T3 et T4, et ce sont celles que la campagne utilise déjà.
- Le canal topologique (T5) a été développé jusqu'au bout : revêtements, codes parfaits, jauge radiale, π₁ exact sur les
  huit srg(243) connus. Son résultat est négatif : il ne peut rien exclure.

**Ce que ce travail n'apporte pas.** Le §4.3 décrit l'ingrédient manquant d'ODD-PURE (une fonctionnelle sur les blocs,
invariante par les permutations formelles, nulle sur les grilles). Ce n'est **pas** un progrès : c'est le diagnostic de
l'équipe du 16/10 (« il manque une idée, une mesure »), redit dans le vocabulaire de Perelman. De même, tout ce qui
concerne les étalements réguliers vient de la note 165 ; la Proposition 3.8 n'en est qu'une relecture cohomologique.
Rien dans ce dossier ne rapproche l'exclusion de Conway.

**La limite de la méthode.** Les principes extraits sont structurels et non génératifs. Ils disent quelles hypothèses
une preuve doit satisfaire, pas comment trouver la quantité. Chez Perelman, 𝒲 et Ṽ sont venus d'heuristiques profondes
(l'espace formel plat S8, l'analogie thermodynamique), propres à la géométrie. Je n'ai pas trouvé leur équivalent pour
des configurations finies. Le dire est la conclusion honnête.

---

## 5.4 Ce qui reste ouvert dans ce dossier (sans prétention de levier)

1. **Une identité de Weitzenböck pour ODD-PURE** (§4.3(e)). C'est une reformulation, sans aucun indice qu'elle marche.
   On peut la tester sur les 7 444 côtés sans grille déjà calculés, en quelques heures.
2. *(Retiré.)* J'avais proposé Γ₅ à Γ₈ comme banc d'essai des lois locales. L'équipe avait déjà établi que srg(243) ne
   convient pas pour calibrer ces lois (L07 §4.15, #087 ; CARTE §4.G) : la résonance k = 14 n'existe pas à k = 22.
3. **Conjecture 3.10 sur les configurations partielles.** En jauge radiale, H¹ se lit sur Γ₂(x). On peut chercher une
   preuve que les cycles d'appariement ne portent aucune classe en l'absence d'étalement : c'est vrai sur Γ₅ à Γ₈, et
   le mécanisme (conditions de cocycle intérieures) est explicite. *Levier :* structurel (simple connexité de Conway),
   pas une exclusion.
4. **η comme variable de comptage.** Ajouter le nombre de paires à η = 1 aux recensements locaux (PL de P ≤ 852) et
   regarder s'il crée une facette. *Coût :* faible si l'outillage du recensement le permet. *Statut :* spéculatif.
5. **Propriété (L) en i = 3.** L'obstacle est un 8-cycle à deux cordes croisées. Une preuve donnerait l'analogue de
   Mulder pour 𝒦_{2n}, d'intérêt indépendant, et |π₁(X(Conway))| ≤ 22.
