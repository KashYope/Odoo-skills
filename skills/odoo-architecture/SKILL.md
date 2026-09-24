---
name: odoo-architecture
description: "Identifier les couches, modules et contrats Odoo avant toute modification. Utiliser pour les tâches Odoo relevant de architecture et appliquer avant toute implémentation correspondante."
---

# odoo-architecture

## Purpose

Identifier les couches, modules et contrats Odoo avant toute modification.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Fixer branche, SHA, édition, modules installés et mode de déploiement. Distinguer le registry Python par base du registry JavaScript.
- Suivre le flux requête → contrôleur → environnement/ORM → métier → données/vues. Placer les invariants dans le modèle, pas dans le contrôleur.
- Lire le manifest et les imports avant de conclure qu’une classe est chargée. Une arborescence ne prouve pas la disponibilité dans une base.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'depends|auto_install|assets|data' addons/<module>/__manifest__.py; rg -n '_name|_inherit' addons/<module>/models
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Modifier le core; faire dépendre un module métier de détails du dispatcher; supposer que Community contient Enterprise.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
Décrire l’opération, le module propriétaire, le modèle, le mécanisme natif et le seul delta requis. Commencer par une configuration si elle suffit.
```

## Relevant core files

- [`odoo/modules/loading.py` · `load_data`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/modules/loading.py#L41) — `load_data`, `load_demo`, `force_demo`, `load_module_graph`, `_check_module_names`, `load_modules`, `reset_modules_state`.
- [`odoo/orm/registry.py` · `_unaccent`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/registry.py#L77) — `_unaccent`, `Registry`, `DummyRLock`, `TriggerTree`.
- [`odoo/http.py` · `route`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/http.py#L755) — `get_default_session`, `RegistryError`, `SessionExpiredException`, `content_disposition`, `db_list`, `db_filter`, `dispatch_rpc`.
- [`addons/sale/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/__manifest__.py#L1) — .
- [`addons/purchase/__manifest__.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/__manifest__.py#L1) — .

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

17/18 utilisent notamment odoo/models.py; 19 déplace l’implémentation dans odoo/orm/. Conserver les imports publics depuis odoo.

## Checklist

Version figée; dépendances connues; couche correcte; zéro modification core.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
