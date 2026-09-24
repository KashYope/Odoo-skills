# Workflow de décision avant code custom

## Porte d’entrée obligatoire

Fixer besoin observable, utilisateur, droits, volumétrie, versions et édition. Sans besoin clair, faire la recherche utile puis demander la seule information qui bloque le choix. Un objectif « moins de code » n’autorise pas de supprimer une exigence métier ou un contrôle d’accès.

| Étape | Question | Si oui | Si non |
|---|---|---|---|
| 1 | Un réglage couvre le besoin ? | Configurer et tester; zéro module | Chercher la fonctionnalité standard |
| 2 | Une primitive couvre le besoin ? | Réutiliser modèle/action/vue/service/route | Chercher une extension |
| 3 | Un hook ou héritage étroit suffit ? | Implémenter delta avec super/heritage XML | Composer les primitives |
| 4 | Une composition reste lisible et sûre ? | Composer sans copier | Étudier petit adaptateur |
| 5 | Un adaptateur résout la différence ? | Limiter sa responsabilité | Justifier une nouvelle abstraction |
| 6 | Nouveau code nécessaire ? | Documenter refus précédents et contrat | Revenir au besoin |
| 7 | Solution correctement testée ? | Livrer avec limites | Corriger ou marquer non validé |

## Séquence de recherche

Requirement → domaine → module standard → modèles/champs/méthodes → routes/contrôleurs → services/widgets/hooks frontend → vues/actions/configuration → extension la plus stable → delta → tests de compatibilité.

## Fiche de décision obligatoire

```text
Besoin et critère d’acceptation :
Version/SHA/édition/modules :
Existant trouvé (chemin, classe/fonction, statut API) :
Deux usages standards ou limite de preuve :
Configuration rejetée parce que :
Réutilisation rejetée parce que :
Extension/composition retenue :
Delta nécessaire :
Sécurité (utilisateur, CRUD/rules/champs/company/tokens) :
Tests à exécuter et résultats :
Risque upgrade et données à migrer :
```

## Comparaison des solutions

À fonctionnalité et sécurité équivalentes, comparer lignes custom, dépendances ajoutées, overrides, routes, JavaScript, duplication et couplage privé. Ce sont des indicateurs, pas un score mécanique : une dépendance massive n’est pas un progrès parce qu’elle retire dix lignes. Ne pas supprimer un test utile pour afficher moins de code.

## Conditions de livraison

- Aucun nouveau modèle/champ/route sans recherche de son équivalent.
- Chaque override conserve contrat, super et test pertinent; chaque XPath est vérifié sur la vue combinée.
- Les droits sont testés hors UI; la configuration multi-société est respectée.
- Installation/update et versions réellement exécutées sont distinguées des vérifications statiques.
- Les inconnues et indisponibilités sont explicites; aucun engagement sur les futures versions.
