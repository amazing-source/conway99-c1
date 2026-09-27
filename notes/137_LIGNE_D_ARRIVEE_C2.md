# 137 — Ligne d'arrivée du cas involution : un bloc lourd en toute configuration, une instance locale par type

*27/09, matin. C1, sur directive de l'utilisateur (toutes les ressources sur C2, jusqu'à la fin). ADOPTÉE par C2 (pilote) comme
ligne d'arrivée de C2. DÉRIVÉ = preuve écrite. À relire formellement par « structures » (§2).*

## 0. Énoncés
| énoncé | statut |
|---|---|
| Σ_c (2#piv_c + d_c) = 84 + 4\|Σ\|, donc un bloc a w_c := 2#piv_c + d_c ≥ 12 | DÉRIVÉ, relu par C2 |
| Lemme 1 par étiquette : v ∈ Φ(z) ∩ Φ(σz) ⟺ {z, σz} = D(O_v) | DÉRIVÉ |
| SEC / SEC-dis selon le type du carré de O_v | DÉRIVÉ |
| Instances I(τ) toutes UNSAT (3 308 classes) ⟹ aucune involution | DÉRIVÉ (complétude, §3) |

## 1. Le comptage
- **Notations.** Chaque orbite O, sur la paire {i,j}, a une étiquette en i (le sommet de j de son représentant) et une en j.
  Elle est **pivot en i** ssi D(O) ∈ étoile(i) (notes/136 §1), c'est-à-dire ssi son carré est frère ou « un bloc » via i.
- **Bouts pivots.**
  - Un carré frère a 2 bouts pivots, un carré « un bloc » en a 1, un carré dis n'en a aucun.
  - Donc Σ_c #piv_c = 2·2|Σ| + (42 − 2|Σ| − 2n_dis) = 42 + 2|Σ| − 2n_dis.
- **Étiquettes dis.** On note d_c le nombre d'étiquettes de c dont l'orbite est dis. Une orbite dis en compte une à chacun de ses
  deux bouts, donc Σ_c d_c = 2·(2n_dis) = 4n_dis.
- **Conclusion.** Σ_c (2#piv_c + d_c) = 84 + 4|Σ| ≥ 84 = 7·12. **Un bloc au moins a w_c ≥ 12.**

## 2. Lemme 1 par étiquette, SEC et SEC-dis
Soit v une étiquette de c, avec b = bloc(v), et O_v l'orbite de u = (c+, v) (σu = (c−, πv)). On a Φ(z) = {x : (c+, x) ~ z}.
- **Lemme.** Pour z lointaine : v ∈ Φ(z) ∩ Φ(σz) ⟺ z ∈ N(u) ∩ N(σu) ⟺ {z, σz} = D(O_v).
  - *Preuve.* v ∈ Φ(z) ⟺ u ~ z, et v ∈ Φ(σz) ⟺ u ~ σz ⟺ σu ~ z. Par le Lemme 1 du carnet de C2, N(u) ∩ N(σu) est
    l'orbite partenaire D(O_v). ∎
- **Contrôle.** Il y a 2 telles z si D(O_v) est lointaine (v non pivot), 0 sinon. C'est exactement K3[v,v] = 2 − 2[v pivot].
- **Sécante.** Pour v non pivot, la σ-paire du quadruplet sécant Q_v est D(O_v). Une orbite non pivot en c n'est jamais frère.
  - **SEC** : si le carré de O_v est « un bloc », il l'est via b. D(O_v) est alors sur {b, k}, et **la σ-paire de Q_v contient b**.
    Avec L1 (a = v), on a en plus πv ∉ Q_v.
  - **SEC-dis** : si le carré est dis, D(O_v) est sur une paire disjointe de {c, b}, et **la σ-paire de Q_v évite b**.

## 3. L'instance I(τ) et la complétude
- **Instance.** Pour un type τ (classe à Aut(X_c, π) près), I(τ) contient :
  - le système local (i)–(iii) et L1/S1/S2 ;
  - les lemmes généraux (--cuts, --digon, --path, --twist, --ident : tous déduits de (i)–(iii)) ;
  - une variable β_v par étiquette non pivot (β_v = 1 si dis), avec β_v = 0 ⟹ SEC_v et β_v = 1 ⟹ SEC-dis_v ;
  - la cardinalité 2#piv(τ) + Σ_v β_v ≥ 12.
- **Cas particuliers.**
  - À ≥ 6 pivots, la cardinalité est automatique.
  - Aux étoiles libres, β ≡ 1 (SEC-dis partout).
  - À 2 pivots, il faut β = 1 sur au moins 8 des 10 non pivots ; à 4 pivots, sur au moins 4 des 8.
- **Complétude.** Dans une configuration, on prend c avec w_c ≥ 12 (§1). Le vrai Φ en c, avec les vrais β, satisfait I(τ_c)
  (§2). Donc **si toutes les I(τ) sont UNSAT, il n'y a pas d'involution.**
  - Cela couvre Σ ≠ ∅, les carrés dis, les mélanges et T = K₇ non simple, sans arbre de familles.
  - Les contraintes sont invariantes par Aut(X_c, π), donc le représentant suffit pour chaque classe.
- **Métrique** : certifiés (sans lex-leader, DRAT VERIFIED) sur 3 308. Répartition : 1 787 (0 pivot), 958 (2), 407 (4), 106 (6),
  39 (8), 11 (12).
- **Héritage.**
  - Un certificat SANS SEC d'un type τ vaut pour I(τ), puisque I(τ) a plus de contraintes.
  - Les certificats AVEC SEC partout ne prouvent que l'étage n_dis = 0. Ils sont à refaire sous la forme β.

## 3 bis. Raffinements (27/09, fin de matinée ; vérifiés par C2 et « structures »)
- **Bris d'égalité.** On prend pour bloc lourd l'argmax de (w_c, #piv_c) dans l'ordre lexicographique. Si c'est une étoile libre,
  la configuration est TOUT-DIS : n_dis = 21, Σ = ∅, et les 7 blocs sont des étoiles libres à d = 12.
  - *Preuve.* Tous les w sont ≤ 12, et Σw = 84 + 4|Σ| ≥ 84 force w ≡ 12 et |Σ| = 0. Un bloc à pivots aurait alors w = 12 avec plus
    de pivots, et il gagnerait le bris d'égalité. ∎
- **La ligne d'arrivée devient :**
  - **(A)** les I(τ) des types à pivots ;
  - **(B)** la seule famille globale tout-dis : D est un 2-facteur de KG(7,2), avec SEC-dis partout.
  - Les 1 787 instances d'étoiles libres ne sont plus nécessaires une par une.
- **Réduction de (A) par Σ.** Avec Σ ≠ ∅, seuls 9 motifs survivent (K₂, P₃, 2K₂, K₃, P₄, P₃+K₂, 3K₂, P₅, 2P₃), tous de degré ≤ 2.
  Les 14 types à ≥ 3 paires frères au bloc sortent donc de (A), dont le tout-frère μ = τ = π. Celui-ci est inconnu à 240 s et
  probablement SAT : c'est la structure de BvLS.
  - Dépendances : notes 18–19 de C2 (RSF, relaxations exactes, DRAT) et carnet §7, §11–§13. C1 a relu et confirmé qu'ils traitent
    les carrés dis explicitement.
  - **(A) = 1 507 types.**
- **(B) en cours.** PL d'orbites symétrisé par G = S₇ ⋉ Z₂⁷ (transitif sur les 42 orbites) : faisable ⟺ solution invariante.
  Secours : sat_whole.py (« structures »), avec les adjacences en variables, λ/μ exacts, le type du bloc 0 fixé et des clauses
  tout-dis.
- **Unités π-arête ⟹ dis** : une étiquette non pivot v avec μv = πv ou τv = πv a β_v = β_{πv} = 1. C'est le 39.3 de C2,
  localisé.

## 4. Risque et mesure
- Étoile libre + SEC-dis sur les 12 étiquettes : inconnu à 40 s (glucose, portable), sur 2 types.
- Mesure décidée au PC du labo : environ 20 étoiles libres en tout-SEC-dis, à 1 h chacune, dès que --beta est codé.
