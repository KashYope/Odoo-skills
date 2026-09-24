---
name: odoo-version-compatibility
description: "Distinguer contrat public, usage répandu et détail interne lors d’un changement de version. Utiliser pour les tâches Odoo relevant de version-compatibility et appliquer avant toute implémentation correspondante."
---

# odoo-version-compatibility

## Purpose

Distinguer contrat public, usage répandu et détail interne lors d’un changement de version.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Fixer une matrice de versions supportées. Classer chaque dépendance : public relativement stable, hook interne répandu, interne fragile, déprécié/remplacé ou non vérifié.
- Comparer signatures, décorateurs, XML IDs, schémas de champs et imports JS sur les SHAs exacts. L’existence du même nom ne prouve pas un contrat identique.
- Maintenir des branches de modules par majeure si cela évite des contorsions; ne pas ajouter une forêt de hasattr/try-except masquant les incompatibilités.
- Consulter version-compatibility.md du skill central; relire les sources actuelles avant décision.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
git diff <sha_old> <sha_new> -- odoo/http.py odoo/orm addons/<module>; rg -n 'deprecated|deprecation' <fichiers_cibles>
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Promettre compatibilité future; traiter master comme release; généraliser un hook privé; figer calendrier de dépréciation.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
Table obligatoire : symbole / version source / version cible / changement / adaptation minimale / test. Marquer non testé plutôt que compatible si aucun environnement n’a été exécuté.
```

## Relevant core files

- [`odoo/http.py` · `route`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/http.py#L755) — `get_default_session`, `RegistryError`, `SessionExpiredException`, `content_disposition`, `db_list`, `db_filter`, `dispatch_rpc`.
- [`odoo/upgrade_code/18.1-02-route-jsonrpc.py` · `upgrade`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/18.1-02-route-jsonrpc.py#L1) — `upgrade`.
- [`odoo/upgrade_code/17.5-01-tree-to-list.py` · `upgrade`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/17.5-01-tree-to-list.py#L4) — `upgrade`.
- [`odoo/addons/base/models/ir_cron.py` · `BadVersion`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_cron.py#L44) — `BadVersion`, `BadModuleState`, `CompletionStatus`, `ListLogHandler`, `IrCron`, `IrCron.create`, `IrCron.write`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

17/18/19 comparés statiquement; master uniquement signal exploratoire sauf preuve explicitement ajoutée.

## Checklist

Matrice; SHAs; statut API; migration des données; tests distincts; inconnues visibles.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
