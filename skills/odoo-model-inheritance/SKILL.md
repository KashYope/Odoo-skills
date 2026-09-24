---
name: odoo-model-inheritance
description: "Choisir entre extension en place, héritage classique et délégation. Utiliser pour les tâches Odoo relevant de model-inheritance et appliquer avant toute implémentation correspondante."
---

# odoo-model-inheritance

## Purpose

Choisir entre extension en place, héritage classique et délégation.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Utiliser _inherit sans _name pour enrichir le modèle existant. _name avec _inherit crée un autre modèle : justifier ce choix.
- Utiliser _inherits uniquement si la délégation et le cycle de vie des records parents sont voulus; elle ne délègue pas automatiquement les méthodes métier.
- Respecter les mixins et l’ordre de super(); lire les autres extensions du même hook. Ne pas contourner la chaîne MRO.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n '_inherit.*sale.order|_inherits|def nom_hook' addons odoo/addons
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Appeler directement une classe parent pour sauter des extensions; fusionner des responsabilités sans relation métier.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    # Extension en place; ne pas ajouter _name.
```

## Relevant core files

- [`odoo/orm/models.py` · `BaseModel`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models.py#L334) — `parse_read_group_spec`, `raise_on_invalid_object_name`, `fix_import_export_id_paths`, `to_record_ids`, `check_company_domain_parent_of`, `check_companies_domain_parent_of`, `MetaModel`.
- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34) — `SaleOrder`, `SaleOrder.create`, `SaleOrder.write`, `SaleOrder.action_confirm`, `SaleOrder._prepare_confirmation_values`, `SaleOrder._prepare_invoice`, `SaleOrder.message_post`.
- [`addons/project/models/project_project.py` · `ProjectProject`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/project/models/project_project.py#L23) — `ProjectProject`, `ProjectProject.create`, `ProjectProject.write`.
- [`addons/crm/models/crm_lead.py` · `CrmLead`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/crm/models/crm_lead.py#L84) — `CrmLead`, `CrmLead._prepare_values_from_partner`, `CrmLead._prepare_address_values_from_partner`, `CrmLead._prepare_contact_name_from_partner`, `CrmLead._prepare_partner_name_from_partner`, `CrmLead.create`, `CrmLead.write`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Mécanisme relativement stable; ordre concret dépendant des addons installés.

## Checklist

Type d’héritage explicite; super coopératif; dépendances manifest; test avec addons coexistants.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
