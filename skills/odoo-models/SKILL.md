---
name: odoo-models
description: "Choisir le bon modèle Odoo et étendre une responsabilité existante. Utiliser pour les tâches Odoo relevant de models et appliquer avant toute implémentation correspondante."
---

# odoo-models

## Purpose

Choisir le bon modèle Odoo et étendre une responsabilité existante.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Chercher le modèle standard et ses relations avant de créer une table. Utiliser _inherit seul pour étendre en place.
- Créer un nouveau _name uniquement pour une entité réellement distincte; définir alors droits, cycle de vie et suppressions.
- Respecter les recordsets et les environnements utilisateur/société. Ne pas supposer un singleton sans contrat.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n '_name =|_inherit =|_inherits =' addons/<module>/models; rg -n 'res.partner|sale.order' addons
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Recréer res.partner; ajouter _name par habitude; stocker une copie d’une donnée relationnelle existante.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    # Ajouter uniquement le champ ou le hook justifié par la recherche.
```

## Relevant core files

- [`odoo/orm/models.py` · `BaseModel`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models.py#L334) — `parse_read_group_spec`, `raise_on_invalid_object_name`, `fix_import_export_id_paths`, `to_record_ids`, `check_company_domain_parent_of`, `check_companies_domain_parent_of`, `MetaModel`.
- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34) — `SaleOrder`, `SaleOrder.create`, `SaleOrder.write`, `SaleOrder.action_confirm`, `SaleOrder._prepare_confirmation_values`, `SaleOrder._prepare_invoice`, `SaleOrder.message_post`.
- [`addons/purchase/models/purchase_order.py` · `PurchaseOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/models/purchase_order.py#L21) — `PurchaseOrder`, `PurchaseOrder.create`, `PurchaseOrder.message_post`, `PurchaseOrder._prepare_supplier_info`, `PurchaseOrder._prepare_down_payment_section_values`, `PurchaseOrder._prepare_grouped_data`, `PurchaseOrder._prepare_invoice`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Contrat Model/_inherit relativement stable; attributs privés et MRO concret à relire.

## Checklist

Entité existante vérifiée; propriété des données; multi-record; société; ACL.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
