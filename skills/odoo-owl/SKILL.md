---
name: odoo-owl
description: "Composer des composants Owl compatibles avec les conventions Odoo. Utiliser pour les tâches Odoo relevant de owl et appliquer avant toute implémentation correspondante."
---

# odoo-owl

## Purpose

Composer des composants Owl compatibles avec les conventions Odoo.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Rechercher composant et hook existants; préférer props, slots et composition au patch du prototype.
- Utiliser setup et hooks avec lifecycle; ne pas redéfinir le constructeur. Nommer les templates module.Component.
- Séparer données/services et rendu; gérer erreurs async et destruction; conserver traduction et accessibilité.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'extends Component|useService|useState|static template|supportedTypes' addons/web/static/src/views/fields
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Copier un renderer complet; modifier props; constructeur custom; patch sans preuve d’absence d’extension.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
// Exemple structurel : compléter imports, template et enregistrement selon la cible.
class DeltaWidget extends Component {
    static template = 'my_module.DeltaWidget';
    setup() { this.orm = useService('orm'); }
}
```

## Relevant core files

- [`addons/web/static/src/views/fields/char/char_field.js` · `CharField`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/views/fields/char/char_field.js#L12) — `CharField`, `charField`.
- [`addons/web/static/src/core/utils/hooks.js` · `useAutofocus`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/utils/hooks.js#L38) — `useAutofocus`, `useBus`, `useServiceProtectMethodHandling`, `SERVICES_METADATA`, `useService`, `useSpellCheck`, `useChildRef`.
- [`addons/web/static/src/core/utils/patch.js` · `A`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/utils/patch.js#L33) — `A`, `patch`, `A`, `prototype`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Ne pas déduire l’API de la seule version Owl; Odoo fournit son environnement, ses services et son pipeline.

## Checklist

Composition recherchée; props; lifecycle; template; traduction; test interactif.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
