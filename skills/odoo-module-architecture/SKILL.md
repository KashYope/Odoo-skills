---
name: odoo-module-architecture
description: "Construire un addon petit, déclaratif et correctement dépendant. Utiliser pour les tâches Odoo relevant de module-architecture et appliquer avant toute implémentation correspondante."
---

# odoo-module-architecture

## Purpose

Construire un addon petit, déclaratif et correctement dépendant.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Chercher un module standard et ses options avant de créer un addon. Une dépendance doit correspondre à un modèle/XML ID/service réellement utilisé.
- Séparer fichiers selon leur responsabilité réelle sans générer des dossiers vides. Charger imports, sécurité puis données/vues dans un ordre valide.
- Utiliser XML IDs, traductions, données noupdate à bon escient et migrations pour les changements persistants.
- Éviter les dependencies lourdes juste pour partager un helper; un petit adaptateur peut coûter moins à maintenir.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'depends|data|assets|auto_install|hook' addons/{sale,purchase,project}/__manifest__.py
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Scaffold énorme; dépendances transitives implicites; hook d’installation pour remplacer des données XML simples.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
my_module/__manifest__.py + __init__.py; ajouter models/, views/, security/, tests/ uniquement quand le delta le nécessite. Déclarer le module propriétaire de chaque référence externe.
```

## Relevant core files

- [`addons/sale/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/__manifest__.py#L1) — .
- [`addons/purchase/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/__manifest__.py#L1) — .
- [`addons/project/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/project/__manifest__.py#L1) — .
- [`odoo/modules/loading.py` · `load_data`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/modules/loading.py#L41) — `load_data`, `load_demo`, `force_demo`, `load_module_graph`, `_check_module_names`, `load_modules`, `reset_modules_state`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Version manifest et migration par majeure; options d’hébergement/édition à vérifier avant de proposer un addon Python.

## Checklist

Minimum de fichiers; imports; depends justifiés; ordre data; XML IDs; installation/update.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
