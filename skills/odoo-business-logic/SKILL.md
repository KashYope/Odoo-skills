---
name: odoo-business-logic
description: "Insérer uniquement le delta métier dans le hook le plus étroit. Utiliser pour les tâches Odoo relevant de business-logic et appliquer avant toute implémentation correspondante."
---

# odoo-business-logic

## Purpose

Insérer uniquement le delta métier dans le hook le plus étroit.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Rechercher les _prepare_*, _get_* et méthodes action_* avant d’étendre create/write ou une confirmation complète.
- Conserver super(), signature, retour, batch et gestion des erreurs. Copier un dictionnaire seulement quand son ownership impose de ne pas le muter.
- Placer les invariants dans contraintes/méthodes serveur et rendre les opérations réessayables quand transactions/jobs le nécessitent.
- Une méthode publique est potentiellement appelable par RPC : contrôler paramètres et préconditions, pas seulement l’UI.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'def (_prepare_|_get_|action_confirm)|super\(' addons/{sale,purchase,stock}/models
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Copier action_confirm; logique seulement dans onchange; validation seulement côté JavaScript; changer le type de retour.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
def _prepare_invoice(self):
    vals = super()._prepare_invoice()
    # Ajouter uniquement un champ réellement défini sur account.move.
    return vals
```

## Relevant core files

- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34) — `SaleOrder`, `SaleOrder.create`, `SaleOrder.write`, `SaleOrder.action_confirm`, `SaleOrder._prepare_confirmation_values`, `SaleOrder._prepare_invoice`, `SaleOrder.message_post`.
- [`addons/purchase/models/purchase_order.py` · `PurchaseOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/models/purchase_order.py#L21) — `PurchaseOrder`, `PurchaseOrder.create`, `PurchaseOrder.message_post`, `PurchaseOrder._prepare_supplier_info`, `PurchaseOrder._prepare_down_payment_section_values`, `PurchaseOrder._prepare_grouped_data`, `PurchaseOrder._prepare_invoice`.
- [`addons/stock/models/stock_move.py` · `StockMove`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/stock/models/stock_move.py#L18) — `StockMove`, `StockMove.create`, `StockMove.write`, `StockMove._prepare_merge_moves_distinct_fields`, `StockMove._prepare_merge_negative_moves_excluded_distinct_fields`, `StockMove._prepare_procurement_origin`, `StockMove._prepare_procurement_qty`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Les hooks préfixés _ restent internes même s’ils sont largement utilisés. Comparer corps, signature et usages lors de chaque upgrade.

## Checklist

Hook étroit; deux usages recherchés; super; contraintes serveur; transitions et réessais testés.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
