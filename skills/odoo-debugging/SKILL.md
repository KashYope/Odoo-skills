---
name: odoo-debugging
description: "Localiser le défaut dans la bonne couche sans patcher le core. Utiliser pour les tâches Odoo relevant de debugging et appliquer avant toute implémentation correspondante."
---

# odoo-debugging

## Purpose

Localiser le défaut dans la bonne couche sans patcher le core.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Reproduire sur base de test avec version, addons et utilisateur exacts. Lire traceback et premier appel custom.
- Comparer comportement standard versus addon sur même scénario. Vérifier chargement module, données XML, cache assets et accès avant réécriture.
- Réduire le cas; activer logs/debug=assets ou profiler ciblé. Éviter tokens, mots de passe et données sensibles dans logs.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'symbole_traceback|XML_ID|nom_route' addons odoo; rg -n 'log_handler|Profiler' odoo/tools/profiler.py
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

sudo pour faire disparaître une erreur; reset de base comme diagnostic; monkey patch; cache vidé sans preuve.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
Livrer : reproduction minimale / couche fautive / cause vérifiée / delta / test de régression. Si cause incertaine, isoler l’hypothèse au lieu de coder un contournement.
```

## Relevant core files

- [`odoo/tools/profiler.py` · `Profiler`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/tools/profiler.py#L508) — `_format_frame`, `_format_stack`, `get_current_frame`, `_get_stack_trace`, `stack_size`, `make_session`, `force_hook`.
- [`odoo/http.py` · `route`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/http.py#L755) — `get_default_session`, `RegistryError`, `SessionExpiredException`, `content_disposition`, `db_list`, `db_filter`, `dispatch_rpc`.
- [`odoo/tests/common.py` · `TransactionCase`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/tests/common.py#L990) — `__getattr__`, `get_db_name`, `RegistryRLock`, `release_test_lock`, `standalone`, `test_xsd`, `new_test_user`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Chemins de traceback et options changent; corréler avec le SHA réellement exécuté.

## Checklist

Reproduction; utilisateur; module; preuve causale; correctif minimal; régression.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
