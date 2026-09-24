---
name: odoo-actions
description: "Réutiliser actions fenêtre, rapports et actions serveur avant une UI ou route spécifique. Utiliser pour les tâches Odoo relevant de actions et appliquer avant toute implémentation correspondante."
---

# odoo-actions

## Purpose

Réutiliser actions fenêtre, rapports et actions serveur avant une UI ou route spécifique.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Chercher ir.actions.act_window/report/server/client et bindings existants. Préférer un menu/action avec domain/context à un écran JavaScript.
- Réserver les actions serveur configurées aux petites automatisations; ne pas enfouir un métier complexe non testable dans safe_eval.
- Renvoyer le dictionnaire d’action attendu; utiliser un XML ID plutôt qu’un ID numérique.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'ir.actions.|binding_model_id|report_action|_for_xml_id' addons/<module> odoo/addons/base/models/ir_actions.py
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Créer un client action pour une simple liste filtrée; coder des IDs; action serveur avec privilèges excessifs.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
action = self.env.ref('sale.action_orders').read()[0]
# Ajouter un domain ciblé seulement si nécessaire, sans neutraliser les droits.
return action
```

## Relevant core files

- [`odoo/addons/base/models/ir_actions.py` · `IrActionsServer`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_actions.py#L567) — `LoggerProxy`, `IrActionsActions`, `IrActionsActions.create`, `IrActionsActions.write`, `IrActionsAct_Window`, `IrActionsAct_Window.create`, `IrActionsAct_WindowView`.
- [`addons/web/controllers/action.py` · `MissingActionError`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/action.py#L11) — `MissingActionError`, `Action`.
- [`addons/sale/views/sale_order_views.xml` · `sale_order_view_activity`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/views/sale_order_views.xml#L1) — `sale_order_view_activity`, `view_sale_order_calendar`, `view_sale_order_graph`, `view_sale_order_pivot`, `view_sale_order_kanban`, `sale_order_kanban_upload`, `sale_order_tree`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Types d’action relativement stables; clefs et services client à contrôler sur la cible.

## Checklist

Action existante recherchée; XML ID; contexte/domain; droits; aucun JS superflu.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
