---
name: odoo-fields
description: "Éviter les champs redondants et définir des calculs cohérents. Utiliser pour les tâches Odoo relevant de fields et appliquer avant toute implémentation correspondante."
---

# odoo-fields

## Purpose

Éviter les champs redondants et définir des calculs cohérents.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Avant ajout : champ existant → champ lié → simple lecture relationnelle → related si exposition nécessaire → compute si dérivation métier réelle.
- Un related n’est pas obligatoire pour lire une relation. store=True exige un besoin de recherche/tri/performance et un coût de recomputation accepté.
- Déclarer depends et dépendances de contexte pertinentes; affecter tous les records. Prévoir inverse/search seulement si requis.
- Vérifier groups, compute_sudo, company_dependent, check_company et risques de fuite de valeurs dérivées.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'nom_champ|related=|depends\(|compute_sudo|company_dependent' addons/<module>/models odoo/orm
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Copier une valeur dans create/write; store partout; utiliser onchange comme invariant serveur; exposer un champ protégé par un related non protégé.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    # Seulement si l’exposition sur la commande est nécessaire et absente :
    partner_city = fields.Char(related='partner_id.city')
```

## Relevant core files

- [`odoo/orm/fields.py` · `resolve_mro`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/fields.py#L50) — `resolve_mro`, `determine`, `Field`, `Field.create`, `Field.write`.
- [`odoo/orm/fields_relational.py` · `_Relational`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/fields_relational.py#L33) — `_Relational`, `Many2one`, `Many2one.write`, `_RelationalMulti`, `_RelationalMulti.create`, `_RelationalMulti.write`, `One2many`.
- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34) — `SaleOrder`, `SaleOrder.create`, `SaleOrder.write`, `SaleOrder.action_confirm`, `SaleOrder._prepare_confirmation_values`, `SaleOrder._prepare_invoice`, `SaleOrder.message_post`.
- [`addons/purchase/models/purchase_order.py` · `PurchaseOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/models/purchase_order.py#L21) — `PurchaseOrder`, `PurchaseOrder.create`, `PurchaseOrder.message_post`, `PurchaseOrder._prepare_supplier_info`, `PurchaseOrder._prepare_down_payment_section_values`, `PurchaseOrder._prepare_grouped_data`, `PurchaseOrder._prepare_invoice`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

API fields publique relativement stable; company_dependent et détails de stockage doivent être revus entre versions.

## Checklist

Champ recherché; dépendances exactes; tous records affectés; stockage justifié; accès testé.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
