---
name: odoo-import-export
description: "Réutiliser import standard, external IDs et export avant un pipeline spécifique. Utiliser pour les tâches Odoo relevant de import-export et appliquer avant toute implémentation correspondante."
---

# odoo-import-export

## Purpose

Réutiliser import standard, external IDs et export avant un pipeline spécifique.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Rechercher base_import.import et load/export_data; différencier upload du fichier et import métier.
- Utiliser external IDs pour des mises à jour reproductibles; valider types, relations, ACL et erreurs par ligne.
- Réserver l’adaptateur custom à la conversion du format externe, en conservant l’ORM pour la persistance.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'def (load|export_data|execute_import)|base_import.import|/web/export' odoo/orm/models.py addons/base_import addons/web/controllers/export.py
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Route CSV maison; SQL insert massif ignorant ORM; recréer les clients à chaque passage; mélanger upload et autorisation.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
Préparer un fichier compatible avec le mapping standard; faire un essai contrôlé sur des données représentatives; vérifier créations, mises à jour et relations avant import complet.
```

## Relevant core files

- [`addons/base_import/models/base_import.py` · `Base_ImportImport`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/base_import/models/base_import.py#L130) — `ImportValidationError`, `Base`, `Base_ImportMapping`, `ResUsers`, `Base_ImportImport`, `Base_ImportImport.execute_import`, `check_patterns`.
- [`addons/base_import/controllers/main.py` · `ImportController`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/base_import/controllers/main.py#L11) — `ImportController`.
- [`addons/web/controllers/export.py` · `ExportFormat.base`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/export.py#L554) — `none_values_filtered`, `allow_empty_iterable`, `GroupsTreeNode`, `ExportXlsxWriter`, `ExportXlsxWriter.write`, `GroupExportXlsxWriter`, `Export`.
- [`odoo/orm/models.py` · `BaseModel`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models.py#L334) — `parse_read_group_spec`, `raise_on_invalid_object_name`, `fix_import_export_id_paths`, `to_record_ids`, `check_company_domain_parent_of`, `check_companies_domain_parent_of`, `MetaModel`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Les assistants et formats d’erreur évoluent; vérifier signature execute_import sur la cible.

## Checklist

Mapping; external IDs; dry-run disponible vérifié; permissions; reprise; volumétrie.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
