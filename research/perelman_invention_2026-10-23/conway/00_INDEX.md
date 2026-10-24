# Second travail — Conway-99 à partir des mécanismes de Perelman

Rédigé le 24/10/2026 pour la campagne « Perelman, l'invention mathématique et Conway-99 ». Le premier travail
(`../etude_perelman/`) dégage dix schémas (S1–S10) et cinq conditions de transfert (T1–T5). Celui-ci les teste une à
une sur srg(99, 14, 1, 2), construit les objets que la transposition demande, et pousse chacun jusqu'à un résultat ou
un obstacle formulé exactement.

## Fichiers

| fichier | contenu |
|---|---|
| `01_DIAGNOSTIC_ET_QUESTIONS.md` | État de la campagne, correspondance avec le mur de Hamilton, réponses aux cinq questions du mandat |
| `02_COURBURE_ET_DYNAMIQUE.md` | T1, T2. La classe 𝒦_k ; Théorème A (aucune dynamique naturelle ; courbures d'arête ; courbure des non-arêtes et parité d'appariement η) |
| `03_TOPOLOGIE_ET_GEOMETRISATION.md` | T5. Complexe triangles-carrés, π₁ fini, géométrisation par codes parfaits, jauge radiale, classes d'étalement ; π₁ des huit srg(243) connus ; l'obstacle exact |
| `04_RIGIDITE_ET_ENONCE_INTERMEDIAIRE.md` | T3, T4, S10. Intégralité ; la résonance k = 14 ; excès d'entrelacement ; où le mécanisme S1 s'arrête sur ODD-PURE |
| `05_BILAN.md` | Verdicts T1–T5, résultats classés par statut, réponse à la question de fond, prochaines étapes |

Statuts utilisés partout : **[P]** démontré ici · **[L]** littérature · **[E]** calcul reproductible (`../code`,
`../data`) · **[S]** verdict de solveur · **[A]** analogie · **[C]** conjecture · **[O]** ouvert ou obstacle formulé.

## Lecture rapide (une page)

**Le diagnostic.** La campagne a l'architecture de Perelman : un énoncé intermédiaire unique (ODD-PURE et ses
équivalents), et un comptage global (P ≤ 852) qui force son applicabilité. Il lui manque une quantité monotone à cas
d'égalité rigide pour démontrer cet énoncé. C'est le diagnostic de l'équipe du 16/10, redit dans un autre vocabulaire :
il n'apporte rien de nouveau.

**Ce qui est démontré.**
1. **Aucune dynamique naturelle n'existe sur Conway** (Théorème A.1). Toute fonctionnelle spectrale ou 2-locale est
   imposée par les paramètres ; Conway serait « d'Einstein » et point fixe de tout flot de Ricci discret. La seule
   courbure libre est une **parité** η sur les non-arêtes, qui fixe κ₀ à (k + 2)/(2k) ou (k + 1)/(2k) (Théorème A.3).
2. **Géométrisation de la famille** (Théorème 3.4). Un srg(v, k, 1, 2) est un graphe simplement connexe de la classe
   𝒦_k (chaque arête dans un unique triangle, μ = 2) quotienté par un groupe libre dont les orbites sont des 2-codes
   parfaits. π₁ est fini (courbure de Lin–Lu–Yau). Le cas grid-full force v ∈ {9, 243}, et π₁(X(BvLS)) est le code de
   Golay ternaire.
3. **Jauge radiale** (Théorème 3.6). Toute la cohomologie mod p se lit sur les cycles des graphes d'appariement d'une
   seule 2-boule.
4. *Lecture, pas résultat :* le lemme impair de l'équipe est la conclusion « pas de respirateur » de Perelman, et le cas
   ouvert d'ODD-PURE est celui où ce mécanisme ne s'applique pas (Proposition 4.3). Cela n'aide pas à le fermer.

**Ce qui est calculé (exact, reproductible).**
- π₁ des **huit** srg(243, 22, 1, 2) connus : (ℤ/3)⁶ pour BvLS, ℤ/3 pour le jumeau, Γ₃ et Γ₄, et **trivial pour les
  quatre graphes sans étalement Γ₅ à Γ₈**.
- Loi observée : **π₁ ≠ 1 ⟺ étalement régulier**.
- Trois nouveaux graphes simplement connexes à 729 sommets dans 𝒦₂₂, cospectraux et non isomorphes.

**Ce que cela dit de Conway.** Conway n'a pas d'étalement régulier (note 165, déjà connu). La loi observée prédit un
complexe simplement connexe (Conjecture 3.10), et ce type topologique est réalisé par les vrais graphes Γ₅ à Γ₈. **La
topologie ne peut donc pas exclure Conway.** Les conditions de Perelman satisfaites (intégralité, égalités imposées)
sont celles que l'équipe exploite déjà.

**Verdict.** Pas de transfert qui fasse avancer l'exclusion. Ce qui est neuf est peu, et surtout négatif :
- deux routes fermées avec preuve ou exemple : un flot sur le graphe (Théorème A.1), et un min-max topologique
  (π₁ des huit srg(243), Γ₅ à Γ₈ simplement connexes) ;
- un invariant local nouveau sans usage connu (η) ;
- une précision mineure : grid-full ⇒ v ∈ {9, 243}.

Ce qui concerne les étalements réguliers vient de la note 165. La description de « l'ingrédient manquant » (§4.3) est
une reformulation du diagnostic de l'équipe. Le conseil d'utiliser Γ₅ à Γ₈ comme banc d'essai des lois locales est
retiré : l'équipe avait déjà écarté srg(243) pour cet usage (L07 §4.15).

## Reproduire

Voir `../code/README.md`. Tous les calculs tiennent en moins de 15 minutes sur une machine ordinaire, sans solveur SAT.
