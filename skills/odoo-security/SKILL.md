---
name: odoo-security
description: "Préserver ACL, record rules, droits champs et isolation multi-société. Utiliser pour les tâches Odoo relevant de security et appliquer avant toute implémentation correspondante."
---

# odoo-security

## Purpose

Préserver ACL, record rules, droits champs et isolation multi-société.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Tester les permissions CRUD du modèle puis les règles sur les records. Les ACL sont additives. Les règles globales s’intersectent (AND); les règles de groupes applicables s’unissent (OR), puis se combinent avec les globales. Sans règle applicable, l’ACL reste déterminante : l’absence de règle ne signifie pas refus.
- Traiter ids, context, domaines, noms de méthodes et jetons comme non fiables. Vérifier les invariants des méthodes publiques.
- Réserver sudo à une opération bornée et documentée après autorisation; ne jamais s’en servir comme correctif à AccessError.
- Tester utilisateur interne limité, portail, public et multi-société; inclure l’accès direct RPC/HTTP et les lectures relationnelles.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'ir.model.access|ir.rule|groups=|sudo\(|check_access|check_company' addons/<module> odoo/addons/base/models
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

ACL accordée à tous sans besoin; sudo().browse(id_utilisateur).write(payload); champ caché considéré sécurisé; SQL sans garanties équivalentes.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
# Pour une opération portant sur des enregistrements, sous l’utilisateur courant :
records.check_access('write')  # Serveur 18/19; api.private en 19, pas appel RPC.
# Valider ensuite état métier et paramètres; laisser write appliquer ses contrôles.
records.write(allowed_values)
```

## Relevant core files

- [`odoo/addons/base/models/ir_model.py` · `IrModelAccess`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_model.py#L2080) — `make_compute`, `mark_modified`, `model_xmlid`, `field_xmlid`, `selection_xmlid`, `query_insert`, `query_update`.
- [`odoo/addons/base/models/ir_rule.py` · `IrRule`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_rule.py#L15) — `IrRule`, `IrRule.create`, `IrRule.write`.
- [`odoo/orm/models.py` · `BaseModel`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models.py#L334) — `parse_read_group_spec`, `raise_on_invalid_object_name`, `fix_import_export_id_paths`, `to_record_ids`, `check_company_domain_parent_of`, `check_companies_domain_parent_of`, `MetaModel`.
- [`addons/portal/controllers/portal.py` · `pager`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/controllers/portal.py#L22) — `pager`, `get_records_pager`, `_build_url_w_params`, `CustomerPortal`, `CustomerPortal._prepare_portal_layout_values`, `CustomerPortal._prepare_home_portal_values`, `CustomerPortal._prepare_my_account_rendering_values`.
- [`addons/sale/security/ir.model.access.csv` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/security/ir.model.access.csv#L1) — .

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

18/19 proposent check_access; vérifier APIs historiques check_access_rights/check_access_rule sur 17. Ne pas choisir une API d’après le seul nom.

## Checklist

Refus testés; champs protégés; sociétés; jetons; aucune escalade implicite.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
