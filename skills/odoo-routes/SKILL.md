---
name: odoo-routes
description: "Trouver une route Odoo existante et vérifier son contrat avant réutilisation. Utiliser pour les tâches Odoo relevant de routes et appliquer avant toute implémentation correspondante."
---

# odoo-routes

## Purpose

Trouver une route Odoo existante et vérifier son contrat avant réutilisation.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Consulter routes.jsonl et routes-families.md du skill central odoo-development; filtrer domaine, URL, modèle, backend_calls et module.
- Lire le handler complet, ses helpers et ses classes parentes. Vérifier dépendances et modules réellement installés.
- Relever type, methods, auth, csrf, readonly, signature, format, ACL/jetons et réponse d’erreur. Un paramètre absent est hérité ou défini par le framework, pas False.
- Ne pas confondre auth=public et données publiques. Ne pas qualifier une route interne web de contrat API externe stable.
- Si aucune route ne convient, vérifier une méthode modèle accessible via le service ORM avant tout nouveau contrôleur.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
# Depuis le dossier du skill central odoo-development :
python3 scripts/query_routes.py references/routes.jsonl --query 'attachment'; rg -n '@(http\.)?route' addons/<module>/controllers
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Considérer l’index statique comme la table effective; interpréter auth absent comme public; ignorer @route() sans chemin; utiliser une route d’un module absent.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
Besoin téléchargement → rechercher /web/content → lire Binary.content_common et ir.binary._find_record → vérifier droit/jeton et champ → réutiliser URL si contrat satisfait → tester accès interdit.
```

## Relevant core files

- [`addons/web/controllers/binary.py` · `clean`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/binary.py#L47) — `clean`, `Binary`.
- [`addons/web/controllers/dataset.py` · `DataSet`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/dataset.py#L13) — `DataSet`, `DataSet.call_kw`.
- [`addons/portal/controllers/portal.py` · `pager`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/portal/controllers/portal.py#L22) — `pager`, `get_records_pager`, `_build_url_w_params`, `CustomerPortal`, `CustomerPortal._prepare_portal_layout_values`, `CustomerPortal._prepare_home_portal_values`, `CustomerPortal._prepare_my_account_rendering_values`.
- [`odoo/http.py` · `route`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/http.py#L755) — `get_default_session`, `RegistryError`, `SessionExpiredException`, `content_disposition`, `db_list`, `db_filter`, `dispatch_rpc`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Index fondé sur un SHA 19; régénérer sur la cible. Les routes et signatures changent même si le chemin reste identique.

## Checklist

Existant recherché; héritage résolu; module disponible; entrée/sortie vérifiées; sécurité négative testée.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
