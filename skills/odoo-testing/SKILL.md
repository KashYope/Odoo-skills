---
name: odoo-testing
description: "Tester le delta métier, les accès et les contrats sensibles. Utiliser pour les tâches Odoo relevant de testing et appliquer avant toute implémentation correspondante."
---

# odoo-testing

## Purpose

Tester le delta métier, les accès et les contrats sensibles.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Utiliser les classes et helpers du framework présent : TransactionCase pour métier, HttpCase pour HTTP/browser, Form lorsque l’UI onchange importe.
- Tester au minimum chemin nominal et refus pertinent; cibler portail/public, multi-société, batch ou réessai selon le changement.
- Tester installation neuve et -u avec données existantes. Une compilation Python ne prouve pas qu’un module Odoo fonctionne.
- Frontend : utiliser le harness de la branche; vérifier les exemples standards plutôt que mélanger HOOT et QUnit.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'TransactionCase|HttpCase|Form\(|tagged|hoot|QUnit' odoo/tests addons/<module>/tests addons/web/static/tests
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Tester seulement admin; assertions reflétant le code sans invariant; annoncer compatibilité sans exécuter Odoo/PostgreSQL.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
./odoo-bin -d test_db -i my_module --test-enable --stop-after-init --test-tags /my_module
# Sur une base de test existante, répéter avec -u my_module pour l’upgrade.
```

## Relevant core files

- [`odoo/tests/common.py` · `TransactionCase`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/tests/common.py#L990) — `__getattr__`, `get_db_name`, `RegistryRLock`, `release_test_lock`, `standalone`, `test_xsd`, `new_test_user`.
- [`addons/sale/tests/test_sale_order.py` · `TestSaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/tests/test_sale_order.py#L19) — `TestSaleOrder`, `TestSaleOrderInvoicing`, `TestSalesTeam`, `TestSaleMailComposerUI`.
- [`addons/purchase/tests/test_purchase.py` · `TestPurchase`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/tests/test_purchase.py#L18) — `TestPurchase`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Classes et harness frontend à relire. Exécuter séparément chaque version supportée; master n’est qu’une alerte.

## Checklist

Nominal; refus; batch; installation/update; versions; résultats et limites explicites.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
