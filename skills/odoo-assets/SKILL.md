---
name: odoo-assets
description: "Déclarer uniquement les assets nécessaires au bon bundle. Utiliser pour les tâches Odoo relevant de assets et appliquer avant toute implémentation correspondante."
---

# odoo-assets

## Purpose

Déclarer uniquement les assets nécessaires au bon bundle.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Lire __manifest__.py et bundles du module propriétaire. Déclarer backend versus frontend selon l’usage réel.
- Éviter replace/remove globaux; utiliser ordre et dépendances seulement si nécessaires. Vérifier fichiers et templates inclus.
- Déboguer avec debug=assets avant de vider arbitrairement caches/attachments.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'assets|web.assets|before|after|replace' addons/<module>/__manifest__.py addons/web/__manifest__.py
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Inclure bibliothèque déjà fournie; charger tout le backend sur website; remplacer un bundle core.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
# Fragment de manifest, après choix du bundle :
'assets': {'web.assets_backend': ['my_module/static/src/**/*']},
```

## Relevant core files

- [`odoo/addons/base/models/ir_asset.py` · `fs2web`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_asset.py#L28) — `fs2web`, `can_aggregate`, `is_wildcard_glob`, `_glob_static_file`, `IrAsset`, `IrAsset.create`, `IrAsset.write`.
- [`addons/web/controllers/binary.py` · `clean`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/binary.py#L47) — `clean`, `Binary`.
- [`addons/sale/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/__manifest__.py#L1) — .
- [`addons/project/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/project/__manifest__.py#L1) — .

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Les noms usuels persistent mais leur contenu et ordre ne sont pas un contrat stable; vérifier chaque version.

## Checklist

Bundle correct; dépendance explicite; pas de doublon; debug et build normal.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
