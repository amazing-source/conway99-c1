# 138 — Grille de relecture pour un argument « réseaux × 7 blocs » (préparée avant l'arrivée du document de Sol)

*27/09. C1. Pour relire vite, et sans complaisance, une entrée externe sur le cas involution (partage : C1 = étapes 7-adiques et
réductions globales ; « structures » = correspondance avec le cadre et contrôles numériques ; C2 = intégration).*

## 1. Ce qui est acquis (à citer, pas à redémontrer)
- **Théorème A (C2)** : α = rang₇((A − 3I)|₁⊥) est pair, donc e′ = α + 1 est impair.
- **Théorème B (C2)** : r = rang₇(S − 3I) est pair, donc e = r − 7 est impair.
  - **B′** : N = S − 3I (mod 7) vérifie N² = 0, et la forme xᵀNx sur F₇⁴⁹/ker N est **hyperbolique**, de discriminant
    (−1)^{r/2}.
- **C1 (notes/129–132)** : r = g⁻ ∈ {18, 20} (g⁻ ≠ 16, certifié), donc e ∈ {11, 13}.
  - Par bloc c : g = (18 − t) + 2(t − r₀) + ρ.
  - Witt par bloc : ρ ≥ 2 si 18 − t est pair et la boule réduite non scindée ; ρ ≥ 1 si 18 − t est impair.
  - Tableau des régimes : notes/133 §1.
  - À g = 18, un bloc t = 0 doit être scindé, et ses lignes lointaines sont toutes rigides (T_FF ≡ Z).
- **Côté pair (notes/135)** : g⁺ ≠ 14 (calcul HiGHS, à certifier). Si g⁺ ∉ {14, 16}, alors g⁺ ≥ 18, et k = g⁻ + g⁺ − 14 ≤ 28.
- **(B), le tout-dis** : les 7 blocs sont des étoiles libres. Recensement des 1 787 types par torsion t :
  - t = 0 : 835 non scindés (det carré) et 571 scindés ;
  - t = 1 : 310 ; t = 2 : 65 ; t = 3 : 3 ; t = 4 : 3.
  - À g⁻ = 18, les 835 t = 0 non scindés sont exclus. À g⁻ = 20, tout est permis.

## 2. Les pièges attendus
1. **Recollement des 7 boules.** Elles ne sont pas orthogonales. Elles partagent les 7 coordonnées intérieures, et chaque orbite est
   dans DEUX étoiles. Les classes de Witt locales ne s'additionnent pas naïvement. Il faut exiger une décomposition orthogonale
   explicite, ou un calcul de Schur global.
2. **Torsion non équilibrée (r₀ < t).** Toute étape qui suppose r₀ = t sans le démontrer est un trou, puisque le bloc
   hyperbolique 2(t − r₀) existe.
3. **Scindé contre non scindé, et g⁻ = 18 contre 20.** Le résidu K_c est anisotrope ou hyperbolique selon le det de la boule. Un
   argument qui « oublie » un cas tue trop.
4. **Secteurs.** Le terme J ne vit que dans le secteur pair. Une identité impaire qui fait apparaître J est fausse.
5. **Hypothèse P = 0 implicite** (pas de prisme), sa version d'avant. Chercher partout où elle sert.
6. **Jauge des signes** (représentants des orbites). Tout énoncé doit être invariant par T ↦ DTD.

## 3. Le contrôle décisif : m = 7 doit servir quelque part
Les graphes srg(1 + 2m², 2m, 1, 2) à m = 2 (Paley 9) et m = 11 (BvLS) EXISTENT, avec une involution à un point fixe.
- **Toute étape qui n'utilise pas m = 7 doit être VRAIE sur eux.** « structures » la teste sur BvLS, x ↦ −x.
- **Le premier change avec m.** Les valeurs propres sont (−1 ± t)/2 avec t = √(8m − 7), donc t = 3 (m = 2), t = 7 (m = 7) et
  t = 9 (m = 11). L'analogue de « N = S − 3I mod 7 » est N = S − I mod 3 (Paley 9) et N = S − 4I mod 3 (BvLS) ; dans les deux
  cas N² ≡ 0.
  - BvLS a t = 9 = 3². Un énoncé qui utilise « t premier » peut donc légitimement y échouer. Paley 9 (t = 3) est alors le bon
    témoin.
- Un argument valide doit utiliser quelque chose de propre à m = 7. Par exemple 7 | k, t = 7, ou 2m − 4 = C(m − 2, 2) (qui sert
  dans le Théorème D).
- Sinon, il prouve trop, donc il est faux.

## 4. Ordre de lecture
1. Les hypothèses exactes, en particulier le statut de P = 0.
2. Les énoncés intermédiaires qui sont vérifiables sur BvLS et Paley 9.
3. Les étapes 7-adiques, confrontées au §1 : sont-elles compatibles avec r = g⁻ ∈ {18, 20} et B′ ?
4. L'endroit exact où m = 7 intervient.
5. Ce que l'argument couvre dans notre ligne d'arrivée : (A), (B), ou les deux.
