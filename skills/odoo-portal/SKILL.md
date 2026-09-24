---
name: odoo-portal
description: "Étendre le portail en réutilisant ses compteurs, accès documents et pagination. Utiliser pour les tâches Odoo relevant de portal et appliquer avant toute implémentation correspondante."
---

# odoo-portal

## Purpose

Étendre le portail en réutilisant ses compteurs, accès documents et pagination.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Étendre CustomerPortal et ses _prepare_*; réutiliser pager et portal.mixin si la sémantique correspond.
- Pour un document partagé, suivre _document_check_access avant tout sudo. Un token valide est une capacité limitée, pas un accès global.
- Aligner domaines de liste, compteurs et liens; tester un utilisateur accédant au document d’un autre client.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n '_prepare_home_portal_values|_document_check_access|pager|portal.mixin' addons/{portal,sale,purchase,account}
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

sudo pour toute la liste; token ignoré; page portail doublant /my existant; compter des documents inaccessibles.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
def _prepare_home_portal_values(self, counters):
    values = super()._prepare_home_portal_values(counters)
    # Ajouter un compteur demandé, calculé sous les droits appropriés.
    return values
```

## Relevant core files

- [`addons/portal/controllers/portal.py` · `pager`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/controllers/portal.py#L22) — `pager`, `get_records_pager`, `_build_url_w_params`, `CustomerPortal`, `CustomerPortal._prepare_portal_layout_values`, `CustomerPortal._prepare_home_portal_values`, `CustomerPortal._prepare_my_account_rendering_values`.
- [`addons/portal/models/portal_mixin.py` · `PortalMixin`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/models/portal_mixin.py#L9) — `PortalMixin`.
- [`addons/sale/controllers/portal.py` · `CustomerPortal`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/controllers/portal.py#L15) — `CustomerPortal`, `CustomerPortal._prepare_home_portal_values`, `CustomerPortal._prepare_quotations_domain`, `CustomerPortal._prepare_orders_domain`, `CustomerPortal._prepare_sale_portal_rendering_values`, `PaymentPortal`.
- [`addons/purchase/controllers/portal.py` · `CustomerPortal`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/controllers/portal.py#L16) — `CustomerPortal`, `CustomerPortal._prepare_home_portal_values`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Hooks portail internes mais fréquemment étendus; vérifier paramètres, qcontext et pagination à chaque upgrade.

## Checklist

Liste et compteur cohérents; token borné; droits négatifs; pagination; aucun leak de métadonnées.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
