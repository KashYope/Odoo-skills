---
name: odoo-views
description: "Étendre une vue avec le plus petit héritage XML robuste. Utiliser pour les tâches Odoo relevant de views et appliquer avant toute implémentation correspondante."
---

# odoo-views

## Purpose

Étendre une vue avec le plus petit héritage XML robuste.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Identifier XML ID et architecture finale combinée, pas uniquement le fichier source. Préférer un ancrage sémantique unique.
- Utiliser inherit_id et un XPath ciblé; modifier attributes plutôt que remplacer un bloc entier.
- Une invisibilité/readonly/groupes de vue ne remplace pas la sécurité serveur. Vérifier les traductions et les autres vues héritées.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'inherit_id|xpath|id=.*view' addons/<module>/views; rg -n 'nom_champ' addons/<module>/views
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Copier la vue entière; XPath par indices de position; ancrage sur libellé traduit; groupes UI comme ACL.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
<record id="sale_order_form_delta" model="ir.ui.view">
  <field name="name">sale.order.form.delta</field>
  <field name="model">sale.order</field>
  <field name="inherit_id" ref="sale.view_order_form"/>
  <field name="arch" type="xml">
    <xpath expr="//field[@name='partner_id']" position="attributes">
      <attribute name="string">Client</attribute>
    </xpath>
  </field>
</record>
```

## Relevant core files

- [`odoo/addons/base/models/ir_ui_view.py` · `IrUiView`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_ui_view.py#L139) — `att_names`, `IrUiViewCustom`, `_hasclass`, `get_view_arch_from_file`, `IrUiView`, `IrUiView.create`, `IrUiView.write`.
- [`addons/sale/views/sale_order_views.xml` · `sale_order_view_activity`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/views/sale_order_views.xml#L1) — `sale_order_view_activity`, `view_sale_order_calendar`, `view_sale_order_graph`, `view_sale_order_pivot`, `view_sale_order_kanban`, `sale_order_kanban_upload`, `sale_order_tree`.
- [`addons/purchase/views/purchase_views.xml` · `menu_purchase_root`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/views/purchase_views.xml#L1) — `menu_purchase_root`, `menu_procurement_management`, `menu_procurement_management_supplier_name`, `menu_purchase_config`, `menu_product_pricelist_action2_purchase`, `menu_product_in_config_purchase`, `menu_product_in_config_purchase`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

17 utilise déjà les expressions directes de modifiers; 18 migre tree vers list. Vérifier XML IDs et ancrages dans chaque branche.

## Checklist

XPath unique; chargement -u réussi; vue finale inspectée; groupes/langues; aucune copie massive.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
