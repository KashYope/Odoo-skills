---
name: odoo-controllers
description: "Réutiliser ou étendre un contrôleur sans dupliquer le métier. Utiliser pour les tâches Odoo relevant de controllers et appliquer avant toute implémentation correspondante."
---

# odoo-controllers

## Purpose

Réutiliser ou étendre un contrôleur sans dupliquer le métier.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Avant nouvelle route, lire odoo-routes et vérifier si ORM/RPC ou une action existante suffit.
- Pour étendre, hériter du contrôleur propriétaire et redécorer la méthode avec @http.route() afin de conserver sa publication.
- Conserver les paramètres hérités sauf modification délibérée; un décorateur vide ne signifie pas absence d’authentification.
- Limiter le contrôleur à validation d’entrée, autorisation, appel métier et sérialisation. Ne pas désactiver CSRF pour faire fonctionner un formulaire.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n '@(http\.)?route|class .*Controller|def nom_handler' addons/<module>/controllers
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Remplacer le login; supprimer la décoration dans un override; exposer une méthode privée; route CRUD miroir.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
from odoo import http
from odoo.addons.web.controllers.home import Home

class HomeDelta(Home):
    @http.route()
    def web_login(self, *args, **kw):
        response = super().web_login(*args, **kw)
        # Delta de présentation justifié uniquement.
        return response
```

## Relevant core files

- [`odoo/http.py` · `route`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/http.py#L755) — `get_default_session`, `RegistryError`, `SessionExpiredException`, `content_disposition`, `db_list`, `db_filter`, `dispatch_rpc`.
- [`addons/auth_signup/controllers/main.py` · `AuthSignupHome`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/auth_signup/controllers/main.py#L23) — `AuthSignupHome`, `AuthSignupHome.web_login`, `AuthSignupHome._prepare_signup_values`, `AuthBaseSetup`.
- [`addons/website/controllers/main.py` · `QueryURL`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/website/controllers/main.py#L51) — `QueryURL`, `Website`, `Website.web_login`, `WebsiteSession`, `WebsiteBinary`.
- [`addons/web/controllers/home.py` · `Home`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/home.py#L34) — `Home`, `Home.web_login`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

json sur 17/18; jsonrpc sur 19. Les signatures de session changent : ne pas réimplémenter authenticate.

## Checklist

Route existante recherchée; décorateurs hérités; CSRF; droits; méthode HTTP; test HttpCase.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
