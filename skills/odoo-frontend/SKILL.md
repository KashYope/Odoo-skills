---
name: odoo-frontend
description: "Privilégier les services, widgets et registries du web client. Utiliser pour les tâches Odoo relevant de frontend et appliquer avant toute implémentation correspondante."
---

# odoo-frontend

## Purpose

Privilégier les services, widgets et registries du web client.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Rechercher vue/action/widget existant avant du JavaScript. Utiliser registry et useService plutôt que des singletons ou accès DOM globaux.
- Employer orm pour modèles, action pour navigation, notification/dialog pour UI; inspecter les noms et signatures réels de la branche.
- Évaluer extension/composition avant patch; un patch officiel reste un couplage et exige un test ciblé.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'registry.category|useService|dependencies:' addons/web/static/src addons/<module>/static/src
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

fetch CRUD manuel; notification maison; dépendance à env interne; patch global d’un renderer pour un seul champ.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
setup() {
    this.orm = useService('orm');
    this.notification = useService('notification');
}
```

## Relevant core files

- [`addons/web/static/src/core/registry.js` · `KeyNotFoundError`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/registry.js#L6) — `KeyNotFoundError`, `DuplicatedKeyError`, `is`, `this`, `Registry`, `registry`.
- [`addons/web/static/src/core/orm_service.js` · `x2ManyCommands`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/orm_service.js#L1) — `x2ManyCommands`, `UPDATE_METHODS`, `ORM`, `ormService`.
- [`addons/web/static/src/core/utils/hooks.js` · `useAutofocus`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/utils/hooks.js#L38) — `useAutofocus`, `useBus`, `useServiceProtectMethodHandling`, `SERVICES_METADATA`, `useService`, `useSpellCheck`, `useChildRef`.
- [`addons/web/static/src/views/fields/char/char_field.js` · `CharField`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/views/fields/char/char_field.js#L12) — `CharField`, `charField`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Registries/services sont les points publics à privilégier; imports et implémentations de composants changent. Le client rpc de 17/18 diffère.

## Checklist

Widget recherché; service officiel; assets déclarés; lifecycle; tests frontend.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
