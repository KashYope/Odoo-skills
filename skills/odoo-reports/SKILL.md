---
name: odoo-reports
description: "Réutiliser ir.actions.report et QWeb pour les documents. Utiliser pour les tâches Odoo relevant de reports et appliquer avant toute implémentation correspondante."
---

# odoo-reports

## Purpose

Réutiliser ir.actions.report et QWeb pour les documents.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Chercher action et template de rapport existants; hériter le template plutôt que refaire le PDF.
- Utiliser report_action pour déclencher; garder le rendu serveur natif. Vérifier droits sur records, langue, société et assets rapport.
- N’ajouter un modèle report.* que si les données requises ne sont pas disponibles dans le contexte normal.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'ir.actions.report|report_action|_get_report_values|report_name' addons/<module>
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Route PDF ad hoc; générateur PDF externe pour une facture native; template complet copié; sudo sur tous les documents.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
return self.env.ref('sale.action_report_saleorder').report_action(self)
```

## Relevant core files

- [`odoo/addons/base/models/ir_actions_report.py` · `IrActionsReport`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_actions_report.py#L158) — `_run_wkhtmltopdf`, `_split_table`, `WkhtmlInfo`, `_wkhtml`, `IrActionsReport`, `IrActionsReport._prepare_html`, `IrActionsReport._prepare_pdf_report_attachment_vals_list`.
- [`addons/web/controllers/report.py` · `ReportController`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/report.py#L18) — `ReportController`.
- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34) — `SaleOrder`, `SaleOrder.create`, `SaleOrder.write`, `SaleOrder.action_confirm`, `SaleOrder._prepare_confirmation_values`, `SaleOrder._prepare_invoice`, `SaleOrder.message_post`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Action/QWeb relativement stables; signatures de rendu privées et outils PDF à vérifier.

## Checklist

Rapport existant; héritage; droits; rendu HTML/PDF; langue/société; pagination réelle.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
