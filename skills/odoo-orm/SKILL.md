---
name: odoo-orm
description: "Utiliser les recordsets, transactions et APIs ORM sans contourner Odoo. Utiliser pour les tâches Odoo relevant de orm et appliquer avant toute implémentation correspondante."
---

# odoo-orm

## Purpose

Utiliser les recordsets, transactions et APIs ORM sans contourner Odoo.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Préférer search/search_read, browse et opérations batch. Pour agrégations 19, read_group est déprécié : étudier _read_group backend ou formatted_read_group selon la forme attendue et lire leur contrat. browse ne vérifie ni existence ni droits.
- Utiliser fields.Command pour les relations; conserver contexte, utilisateur et sociétés autorisées.
- Utiliser @api.model_create_multi et super() pour create. Ne pas commit manuellement dans une opération métier ordinaire.
- SQL seulement après mesure et justification; paramétrer, respecter flush/invalidation et reproduire explicitement les garanties de sécurité nécessaires.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'def (create|write|search|read_group)|model_create_multi|Command\.' odoo/orm addons/<module>/models
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

search dans une boucle; sudo global; commit manuel; SQL pour contourner une règle; override vide en production.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
from odoo import api, models

class Partner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        # Delta batch uniquement si un besoin le justifie.
        return records
```

## Relevant core files

- [`odoo/orm/models.py` · `BaseModel`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models.py#L334) — `parse_read_group_spec`, `raise_on_invalid_object_name`, `fix_import_export_id_paths`, `to_record_ids`, `check_company_domain_parent_of`, `check_companies_domain_parent_of`, `MetaModel`.
- [`odoo/orm/commands.py` · `Command`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/commands.py#L11) — `Command`, `Command.create`.
- [`odoo/orm/decorators.py` · `model_create_multi`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/decorators.py#L357) — `attrsetter`, `constrains`, `constrains`, `constrains`, `ondelete`, `onchange`, `depends`.
- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34) — `SaleOrder`, `SaleOrder.create`, `SaleOrder.write`, `SaleOrder.action_confirm`, `SaleOrder._prepare_confirmation_values`, `SaleOrder._prepare_invoice`, `SaleOrder.message_post`.
- [`addons/purchase/models/purchase_order.py` · `PurchaseOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/models/purchase_order.py#L21) — `PurchaseOrder`, `PurchaseOrder.create`, `PurchaseOrder.message_post`, `PurchaseOrder._prepare_supplier_info`, `PurchaseOrder._prepare_down_payment_section_values`, `PurchaseOrder._prepare_grouped_data`, `PurchaseOrder._prepare_invoice`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

CRUD public relativement stable; read_group déprécié en 19. _read_group est recommandé par le core pour le backend mais sa signature et son retour doivent être vérifiés. Ne pas importer les implémentations odoo.orm dans un addon.

## Checklist

Batch; ACL/rules; transactions; retour super conservé; aucune requête N+1.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
