---
name: odoo-upgrade-safe-development
description: "Réduire la surface de rupture et préparer les migrations des données. Utiliser pour les tâches Odoo relevant de upgrade-safe-development et appliquer avant toute implémentation correspondante."
---

# odoo-upgrade-safe-development

## Purpose

Réduire la surface de rupture et préparer les migrations des données.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Préférer configuration → réutilisation → héritage → composition → adaptateur → nouveau code, sous contrainte de sécurité et coût total.
- Réduire overrides, routes, JS et dépendances; ne pas sacrifier lisibilité ou règles métier pour économiser des lignes.
- Pour chaque override/hook interne, noter raison, contrat et test qui détectera une rupture. Préserver XML IDs et données utilisateur.
- Distinguer transformation du code, migration de schéma/données et mise à jour du module. Les scripts upgrade_code ne suffisent pas à migrer une base.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'super\(|@.*route|patch\(|cr.execute|sudo\(' my_module; rg -n 'migrate|pre-|post-|end-' odoo/modules/migration.py addons/<module>
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Modifier core; copier méthode/vue; suppressions de champs sans migration; scripts destructifs; compatibilité déclarée sans tests.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
Avant livraison : compter fichiers, lignes custom, dépendances, overrides, routes, patches JS; justifier chaque ajout. Tester installation + mise à jour sur copie de données, puis comparer les invariants métier et droits.
```

## Relevant core files

- [`odoo/modules/migration.py` · `MigrationManager`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/modules/migration.py#L58) — `MigrationManager`, `exec_script`.
- [`odoo/modules/loading.py` · `load_data`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/modules/loading.py#L41) — `load_data`, `load_demo`, `force_demo`, `load_module_graph`, `_check_module_names`, `load_modules`, `reset_modules_state`.
- [`odoo/upgrade_code/18.1-02-route-jsonrpc.py` · `upgrade`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/18.1-02-route-jsonrpc.py#L1) — `upgrade`.
- [`odoo/upgrade_code/18.1-00-sql-constraint.py` · `upgrade`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/18.1-00-sql-constraint.py#L13) — `upgrade`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Aucune garantie future. Le corpus Community ne contient pas l’ensemble des migrations Enterprise ni toutes les migrations de service Odoo.

## Checklist

Surface minimale; données préservées; migration séparée; tests droits/métier; rollback opérationnel préparé.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
