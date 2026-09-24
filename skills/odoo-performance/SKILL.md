---
name: odoo-performance
description: "Optimiser après mesure tout en conservant les garanties ORM. Utiliser pour les tâches Odoo relevant de performance et appliquer avant toute implémentation correspondante."
---

# odoo-performance

## Purpose

Optimiser après mesure tout en conservant les garanties ORM.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Mesurer requêtes, temps et volume sur cas représentatif avant optimisation. Identifier N+1, calculs stockés excessifs et payloads inutiles.
- Privilégier batch, préchargement, domaines et agrégations adaptées; limiter champs et pagination.
- Un index supplémentaire et store=True ont un coût d’écriture; justifier leur usage. Ne pas inventer un cache sans politique d’invalidation.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'search_count|search_read|read_group|fetch|prefetch' addons/<module>/models odoo/orm/models.py
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

SQL prématuré; search([]) puis filtrage Python massif; cache global multi-utilisateur; lecture de tous les champs.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
Remplacer une recherche par record par une recherche/agrégation sur tout le recordset, puis associer les résultats en mémoire. Mesurer avant/après et conserver les mêmes droits/domaines.
```

## Relevant core files

- [`odoo/orm/models.py` · `BaseModel`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models.py#L334) — `parse_read_group_spec`, `raise_on_invalid_object_name`, `fix_import_export_id_paths`, `to_record_ids`, `check_company_domain_parent_of`, `check_companies_domain_parent_of`, `MetaModel`.
- [`odoo/tools/profiler.py` · `Profiler`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/tools/profiler.py#L508) — `_format_frame`, `_format_stack`, `get_current_frame`, `_get_stack_trace`, `stack_size`, `make_session`, `force_hook`.
- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34) — `SaleOrder`, `SaleOrder.create`, `SaleOrder.write`, `SaleOrder.action_confirm`, `SaleOrder._prepare_confirmation_values`, `SaleOrder._prepare_invoice`, `SaleOrder.message_post`.
- [`addons/project/models/project_project.py` · `ProjectProject`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/project/models/project_project.py#L23) — `ProjectProject`, `ProjectProject.create`, `ProjectProject.write`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

API publique search/read stable relative; détails prefetch/cache et _read_group internes sensibles.

## Checklist

Mesure; batch; limites; résultats identiques; droits; bénéfice confirmé.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
