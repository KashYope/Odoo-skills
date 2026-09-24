---
name: odoo-search-before-code
description: "Imposer une recherche documentée de l’existant avant de produire du code Odoo. Utiliser pour les tâches Odoo relevant de search-before-code et appliquer avant toute implémentation correspondante."
---

# odoo-search-before-code

## Purpose

Imposer une recherche documentée de l’existant avant de produire du code Odoo.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Exécuter la séquence Requirement → domaine → module standard → modèles/champs/méthodes → routes/contrôleurs → services frontend → vues/actions/configuration → point d’extension → delta minimal.
- Pour chaque piste, noter chemin, symbole, pertinence et raison de rejet. Un résultat absent du corpus partiel ne prouve pas l’absence dans Odoo.
- Comparer configuration, réutilisation, héritage, composition, adaptateur et nouveau code dans cet ordre. Arrêter dès qu’une solution respecte fonction, sécurité et maintenance.
- Pour une règle structurante, lire le contrat et au moins deux usages standards lorsque disponibles; signaler l’exception sinon.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'mot_metier|nom_technique' addons odoo/addons; rg -n '@(http\.)?route|registry.category|useService|inherit_id' addons/<module>
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Coder puis chercher; créer une route pour un CRUD déjà accessible par ORM; installer un gros module seulement pour éviter cinq lignes lisibles.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
Produire avant le diff : Besoin / Existant trouvé / Sources / Options rejetées / Extension choisie / Fichiers ajoutés / Tests / Risque de version. Si configuration suffisante, livrer les réglages et aucun module.
```

## Relevant core files

- [`addons/web/controllers/dataset.py` · `DataSet`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/dataset.py#L13) — `DataSet`, `DataSet.call_kw`.
- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34) — `SaleOrder`, `SaleOrder.create`, `SaleOrder.write`, `SaleOrder.action_confirm`, `SaleOrder._prepare_confirmation_values`, `SaleOrder._prepare_invoice`, `SaleOrder.message_post`.
- [`addons/purchase/models/purchase_order.py` · `PurchaseOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/models/purchase_order.py#L21) — `PurchaseOrder`, `PurchaseOrder.create`, `PurchaseOrder.message_post`, `PurchaseOrder._prepare_supplier_info`, `PurchaseOrder._prepare_down_payment_section_values`, `PurchaseOrder._prepare_grouped_data`, `PurchaseOrder._prepare_invoice`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Refaire la recherche sur la branche cible. Les résultats 19 ne sont pas une spécification pour 17/18.

## Checklist

Recherche traçable; alternatives classées; besoin couvert; coût total et sécurité conservés.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
