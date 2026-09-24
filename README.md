# Odoo Skills

Français · [English](README.en.md)

29 skills opérationnels pour guider les agents IA dans le développement, la maintenance et les upgrades de modules Odoo. Cette bibliothèque s’appuie sur le [code source officiel](https://github.com/odoo/odoo) et ses modules standards. Elle fournit des instructions, des références et des outils de recherche ; ce n’est pas un addon Odoo.

> **Ne jamais écrire du code qu’Odoo sait déjà faire.**

## Politique : rester au plus près du code source

Avant toute implémentation, rechercher les modèles, champs, méthodes, mixins, contrôleurs, routes, services, composants, vues, actions, configurations et mécanismes de sécurité déjà disponibles dans la version cible.

L’ordre de préférence est obligatoire :

1. Configuration Odoo existante.
2. Réutilisation d’une fonctionnalité native.
3. Héritage ou extension ciblée.
4. Composition de primitives existantes.
5. Petit adaptateur.
6. Nouveau code uniquement en dernier recours.

Si un réglage suffit, livrer les étapes de configuration et **aucun code**. À fonctionnalité équivalente, minimiser les dépendances, surcharges, routes, JavaScript et duplications. La sécurité, la lisibilité et la testabilité restent des contraintes : moins de lignes ne justifie jamais de contourner les droits.

Rester proche du source signifie comprendre et utiliser ses contrats et points d’extension, sans copier ses méthodes ni modifier le core. Chaque choix important doit citer la version ou le SHA, le chemin du fichier et la classe ou fonction concernée, avec plusieurs usages standards lorsque disponibles. Une API interne couramment utilisée reste à revérifier lors d’un upgrade.

## Fonctionnement

Le point d’entrée est [odoo-development](skills/odoo-development/SKILL.md). Il impose [odoo-search-before-code](skills/odoo-search-before-code/SKILL.md), puis oriente vers les seuls skills spécialisés nécessaires. Ne pas charger toute la bibliothèque ou tout l’index des routes dans le contexte de l’agent.

Le workflow est : besoin vérifiable → domaine Odoo → module standard → modèles/champs/méthodes → routes/contrôleurs → services frontend → vues/actions/configuration → point d’extension le plus stable → delta minimal → tests et vérification de version.

Avant de coder, l’agent doit fournir :

- La version, l’édition et les modules installés pertinents.
- Les fonctionnalités existantes trouvées et leurs références source.
- L’approche retenue et les raisons d’écarter les solutions plus natives.
- Le delta réellement nécessaire, les tests à exécuter et les risques d’upgrade.

Les patterns privilégiés sont `_inherit`, `super()` coopératif, hooks étroits, ORM par lots, héritage XML ciblé, services/registries/widgets et primitives natives de mail, cron, reporting et import/export. Éviter les méthodes ou vues copiées, les routes CRUD redondantes, les IDs numériques, le SQL lorsque l’ORM convient et `sudo()` utilisé pour contourner un refus d’accès.

## Utilisation avec un agent

1. Cloner ce dépôt et donner à l’agent accès au checkout de la version Odoo réellement ciblée.
2. Installer les dossiers complets de `skills/` dans le répertoire de skills pris en charge par l’agent, en conservant `references/`, `scripts/`, `agents/` et `assets/`.
3. Si l’agent ne gère pas l’installation de skills, lui demander de lire `skills/odoo-development/SKILL.md`, puis les fichiers spécialisés indiqués.
4. Préciser le besoin, la version, l’édition et les modules disponibles. Les mécanismes exacts de découverte dépendent de l’agent.

Exemple de consigne :

```text
Applique odoo-development et odoo-search-before-code.
Projet : Odoo 19 Community, modules sale et portal installés.
Besoin : permettre au client de télécharger son devis en PDF.
Recherche d’abord le parcours natif, ses routes et ses contrôles d’accès.
Justifie tout code supplémentaire avec des références au checkout cible.
Si Odoo couvre le besoin, fournis seulement la configuration nécessaire.
```

Les skills et références sont rédigés en français ; les deux README expliquent le même fonctionnement en français et en anglais.

## Contenu

| Domaine / Domain | Skills |
|---|---|
| Pilotage / Coordination | [odoo-development](skills/odoo-development/SKILL.md), [odoo-search-before-code](skills/odoo-search-before-code/SKILL.md), [odoo-architecture](skills/odoo-architecture/SKILL.md), [odoo-module-architecture](skills/odoo-module-architecture/SKILL.md) |
| Données et métier / Data and business logic | [odoo-models](skills/odoo-models/SKILL.md), [odoo-orm](skills/odoo-orm/SKILL.md), [odoo-fields](skills/odoo-fields/SKILL.md), [odoo-model-inheritance](skills/odoo-model-inheritance/SKILL.md), [odoo-business-logic](skills/odoo-business-logic/SKILL.md) |
| Interface / UI | [odoo-views](skills/odoo-views/SKILL.md), [odoo-actions](skills/odoo-actions/SKILL.md), [odoo-frontend](skills/odoo-frontend/SKILL.md), [odoo-owl](skills/odoo-owl/SKILL.md), [odoo-assets](skills/odoo-assets/SKILL.md) |
| Web et accès / Web and access | [odoo-security](skills/odoo-security/SKILL.md), [odoo-controllers](skills/odoo-controllers/SKILL.md), [odoo-routes](skills/odoo-routes/SKILL.md), [odoo-rpc](skills/odoo-rpc/SKILL.md), [odoo-website](skills/odoo-website/SKILL.md), [odoo-portal](skills/odoo-portal/SKILL.md) |
| Services fonctionnels / Functional services | [odoo-cron](skills/odoo-cron/SKILL.md), [odoo-mail](skills/odoo-mail/SKILL.md), [odoo-reports](skills/odoo-reports/SKILL.md), [odoo-import-export](skills/odoo-import-export/SKILL.md) |
| Qualité et évolution / Quality and upgrades | [odoo-testing](skills/odoo-testing/SKILL.md), [odoo-debugging](skills/odoo-debugging/SKILL.md), [odoo-performance](skills/odoo-performance/SKILL.md), [odoo-version-compatibility](skills/odoo-version-compatibility/SKILL.md), [odoo-upgrade-safe-development](skills/odoo-upgrade-safe-development/SKILL.md) |

- [Architecture](skills/odoo-development/references/architecture.md)
- [Workflow de décision / Decision workflow](skills/odoo-development/references/decision-workflow.md)
- [Primitives](skills/odoo-development/references/primitives.md)
- [Points d’extension / Extension points](skills/odoo-development/references/extension-points.md)
- [Anti-patterns](skills/odoo-development/references/anti-patterns.md)
- [Familles de routes / Route families](skills/odoo-development/references/routes-families.md)
- [Index des routes / Route index](skills/odoo-development/references/routes-index.md)
- [Compatibilité / Compatibility](skills/odoo-development/references/version-compatibility.md)
- [Sources](skills/odoo-development/references/evidence.md)
- [Périmètre du corpus / Corpus coverage](skills/odoo-development/references/coverage.json)
- [Organisation des skills / Skill organization](skills/odoo-development/references/skill-set.md)
- [Validation](skills/odoo-development/references/validation.md)

Le corpus contient 53 primitives, 17 points d’extension, 21 anti-patterns et 39 fiches détaillées de routes. L’index JSONL contient 943 déclarations statiques et 1 000 occurrences de chemins littéraux, dont des routes de test. Ces nombres ne représentent pas des endpoints uniques actifs.

## Rechercher et actualiser les routes

Depuis la racine du dépôt, avec Python 3 et sa bibliothèque standard :

```sh
python3 skills/odoo-development/scripts/query_routes.py \
  skills/odoo-development/references/routes.jsonl --query attachment --limit 8

python3 skills/odoo-development/scripts/query_routes.py \
  skills/odoo-development/references/routes.jsonl --module portal --limit 8

python3 skills/odoo-development/scripts/extract_routes.py /path/to/odoo \
  --version 19.0 --sha "$(git -C /path/to/odoo rev-parse HEAD)" \
  --out /path/to/routes.jsonl

python3 skills/odoo-development/scripts/test_extract_routes.py
```

L’extracteur analyse l’AST sans exécuter Odoo. Il conserve les métadonnées déclarées, les overrides `@route()` et les expressions non résolues. Il ne résout ni l’héritage effectif des contrôleurs ni les modules installés. Un paramètre `auth` ou `csrf` absent peut être hérité ou recevoir une valeur par défaut. `auth='public'` ne signifie pas que les données sont publiques. L’absence de résultat dans l’index ne prouve pas l’absence d’une fonctionnalité.

## Sources, versions et limites

Analyse principale : Odoo **19.0**, avec 792 fichiers récupérés, dont les 318 fichiers Python `controllers/` hors `__init__.py` identifiés dans l’arbre. Comparaisons ciblées : 12 fichiers pour **17.0** et 12 pour **18.0**. `master` a fait l’objet d’un inventaire d’arbre seulement. Il ne s’agit pas d’un audit exhaustif de toutes les implémentations.

| Branche / Branch | Commit analysé / Analyzed commit |
|---|---|
| 19.0 | `2e2acfd6d2725d1a4a95b1a6056334e1ac34163f` |
| 18.0 | `c270965ec11c95e5e2866b30f8fa2c90287c6e8a` |
| 17.0 | `b4c6b344a7a6cef93db339c56edb4feb5b222435` |
| master — inventaire / inventory | `8365a19519cf12321270abc500116d26f2f188e2` |

Les références signalent les contrats publics, usages relativement stables, détails internes et remplacements récents. Les zones sensibles incluent `json`/`jsonrpc`, la progression et les transactions des crons, `read_group` et ses formats de remplacement, ainsi que les imports frontend. Toujours relire le source de la version cible ; une référence figée n’est pas une garantie pour les versions futures.

Validation effectuée : structure des 29 skills, trois tests de l’extracteur et deux essais d’utilisation par agent (portail et upgrade). Aucun test sur une instance Odoo/PostgreSQL, rendu PDF réel ou migration de base n’a été exécuté. Les addons Enterprise et tiers ne sont pas couverts par ce corpus.

## Contribuer

Rechercher d’abord dans le source Odoo et les skills existants. Proposer le plus petit changement utile, citer les chemins/symboles et commits, vérifier plusieurs usages standards et préciser la stabilité. Actualiser les références et l’index si le périmètre change, puis exécuter les tests pertinents. Ne pas ajouter de skill, dépendance ou abstraction qui fait doublon.

## Licence et attribution

Voir la [licence Apache 2.0 du dépôt](LICENSE). Les sources Odoo référencées restent soumises à leurs propres licences. Ce projet indépendant n’est pas une publication officielle d’Odoo.
