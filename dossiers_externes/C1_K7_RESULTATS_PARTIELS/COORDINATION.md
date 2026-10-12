# Coordination / entrée de registre

Source : notes 171–173 de `amazing-source/conway99-c1`, branche
`claude/v7-simultaneous`, SHA `fd7a1f1c90410b3514b2ce1974ef64f1370c5305`.

## Contraintes utilisables

- **DEMONTRÉ / universel sous α=22 :** Γ_c ∪ M_c est connexe, pour tout c.
  Q_W=6I−3M−G est un laplacien. Une composante propre S aurait Qu=0,
  Yu pair, mais le sommet z_ab pour a∈S,b∉S donnerait (Qu)_z impair.
- **DEMONTRÉ / corollaire :** rang_R Q_W=13 ; complément de Schur sur les
  63 autres blocs de rang 9.
- **DEMONTRÉ / conditionnel :** si 1_Z∈ker_F3 Yᵀ, |Z|=15, les sept c∉Z ont
  n≤3, avec la table mixte/pure exacte de PREUVES §3. Ne pas l'appliquer aux
  quinze c∈Z ni aux autres types ternaires sans preuve supplémentaire.

## Ne pas promouvoir

- K7 : OUVERTE. Motifs (i) et (ii) : OUVERTS en général.
- L'exemple local du dossier n'est PAS un contre-exemple à K7. Le design Y
  complet et l'adjacence D complète y sont indéterminés.
- La traduction en normes 4,6,8 ne démontre pas leur impossibilité. Ne pas
  demander l'absence de tous les vecteurs de norme 6 : il en existe déjà dans
  le repère. La collection visée est celle des 21 sommes marquées de deux
  vecteurs-mates, pour un c fixé.

## Usage de la recherche antérieure

Le mot ternaire indicateur de 15 points donne une seconde coclique se coupant
en 15 points avec C : c'est le lemme antérieur, réutilisé et non redécouvert.
Les observations BvLS, les échecs SAT forcés (i)/(ii), et les 2 141 classes sous
K7 ne sont pas relancés. Aucune statistique aléatoire n'est utilisée comme preuve.

## Limites de certification

Les preuves sont écrites à la main. Le vérificateur court contrôle les données
finies et les identités du fixture. Il ne constitue ni une preuve Lean ni un
certificat couvrant le système SRG complet. Aucun verdict de solveur n'intervient
comme prémisse des théorèmes 1 et 2.
