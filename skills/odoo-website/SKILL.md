---
name: odoo-website
description: "Réutiliser pages, QWeb, formulaires et publication website. Utiliser pour les tâches Odoo relevant de website et appliquer avant toute implémentation correspondante."
---

# odoo-website

## Purpose

Réutiliser pages, QWeb, formulaires et publication website.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Chercher page, snippet, formulaire, SEO et modèle publié existants avant un nouveau contrôleur.
- Préserver contexte website, langue, société, publication et droits. Utiliser request.render et templates hérités.
- Séparer accès anonyme et contenu réellement publié; contrôler les paramètres de formulaires et les fichiers.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'website.published|website.seo|request.render|website=True' addons/website addons/website_sale
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Site parallèle dans Odoo; rechercher en sudo puis afficher tous les records; copier tout un template; ignorer multi-website.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
Étendre un template website existant via inherit_id et XPath; ajouter une route uniquement pour une ressource absente des mécanismes natifs.
```

## Relevant core files

- [`addons/website/controllers/main.py` · `QueryURL`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/controllers/main.py#L51) — `QueryURL`, `Website`, `Website.web_login`, `WebsiteSession`, `WebsiteBinary`.
- [`addons/website/models/website.py` · `Website`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/models/website.py#L99) — `Website`, `Website.create`, `Website.write`.
- [`addons/website/models/website_page.py` · `PageCannotBeCached`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/models/website_page.py#L19) — `PageCannotBeCached`, `WebsitePage`, `WebsitePage.write`.
- [`addons/website_sale/controllers/main.py` · `WebsiteSale`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website_sale/controllers/main.py#L133) — `handle_product_params_error`, `TableCompute`, `WebsiteSale`, `WebsiteSale._prepare_product_values`, `WebsiteSale._prepare_breadcrumb_markup_data`, `WebsiteSale._prepare_checkout_page_values`, `WebsiteSale._prepare_address_form_values`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

QWeb/héritage relativement stables; widgets/snippets et interactions website évoluent rapidement. Lire les assets de la version.

## Checklist

Publication; public/portail; langue; website; template réutilisé; formulaire sécurisé.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
