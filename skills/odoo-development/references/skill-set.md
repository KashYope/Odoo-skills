# Architecture du set de skills

## Chargement progressif

`odoo-development` orchestre; `odoo-search-before-code` impose la recherche. Charger ensuite les seuls domaines touchés, puis sécurité/tests/compatibilité selon le risque. Les 28 noms demandés sont conservés pour faciliter le déclenchement; aucune fusion ne masque un domaine.

Les références volumineuses et les deux scripts sont centralisés dans odoo-development. Les skills spécialisés contiennent règles, recherche, exemple minimal, liens figés, notes de version et checklist. Ils se résolvent par frontmatter, pas par dossier physique.

| Skill | Responsabilité |
|---|---|
| odoo-development | Orientation, recherche obligatoire, références et outils communs |
| odoo-architecture | Identifier les couches, modules et contrats Odoo avant toute modification. |
| odoo-search-before-code | Imposer une recherche documentée de l’existant avant de produire du code Odoo. |
| odoo-models | Choisir le bon modèle Odoo et étendre une responsabilité existante. |
| odoo-orm | Utiliser les recordsets, transactions et APIs ORM sans contourner Odoo. |
| odoo-fields | Éviter les champs redondants et définir des calculs cohérents. |
| odoo-model-inheritance | Choisir entre extension en place, héritage classique et délégation. |
| odoo-business-logic | Insérer uniquement le delta métier dans le hook le plus étroit. |
| odoo-views | Étendre une vue avec le plus petit héritage XML robuste. |
| odoo-actions | Réutiliser actions fenêtre, rapports et actions serveur avant une UI ou route spécifique. |
| odoo-security | Préserver ACL, record rules, droits champs et isolation multi-société. |
| odoo-controllers | Réutiliser ou étendre un contrôleur sans dupliquer le métier. |
| odoo-routes | Trouver une route Odoo existante et vérifier son contrat avant réutilisation. |
| odoo-rpc | Choisir le transport natif adapté au client et à la version. |
| odoo-website | Réutiliser pages, QWeb, formulaires et publication website. |
| odoo-portal | Étendre le portail en réutilisant ses compteurs, accès documents et pagination. |
| odoo-frontend | Privilégier les services, widgets et registries du web client. |
| odoo-owl | Composer des composants Owl compatibles avec les conventions Odoo. |
| odoo-assets | Déclarer uniquement les assets nécessaires au bon bundle. |
| odoo-cron | Réutiliser ir.cron et ses traitements batch. |
| odoo-mail | Réutiliser chatter, activités, templates et bus. |
| odoo-reports | Réutiliser ir.actions.report et QWeb pour les documents. |
| odoo-import-export | Réutiliser import standard, external IDs et export avant un pipeline spécifique. |
| odoo-testing | Tester le delta métier, les accès et les contrats sensibles. |
| odoo-debugging | Localiser le défaut dans la bonne couche sans patcher le core. |
| odoo-performance | Optimiser après mesure tout en conservant les garanties ORM. |
| odoo-module-architecture | Construire un addon petit, déclaratif et correctement dépendant. |
| odoo-version-compatibility | Distinguer contrat public, usage répandu et détail interne lors d’un changement de version. |
| odoo-upgrade-safe-development | Réduire la surface de rupture et préparer les migrations des données. |

## Ressources communes

architecture.md; routes-families.md; routes-index.md; routes.jsonl; primitives.md; extension-points.md; anti-patterns.md; version-compatibility.md; decision-workflow.md; evidence.md; coverage.json; validation.md.

Scripts : extract_routes.py (AST sans dépendance Odoo) et query_routes.py (recherche JSONL). Aucun script ne modifie un serveur Odoo.
