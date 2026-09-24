---
name: odoo-rpc
description: "Choisir le transport natif adapté au client et à la version. Utiliser pour les tâches Odoo relevant de rpc et appliquer avant toute implémentation correspondante."
---

# odoo-rpc

## Purpose

Choisir le transport natif adapté au client et à la version.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Dans le web client, utiliser le service orm pour un appel modèle et le client rpc de la branche pour un contrôleur.
- Pour intégration externe 19, étudier JSON-2 et ses clés API; ne pas construire une API REST miroir du modèle.
- Distinguer XML/JSON-RPC externes historiques des contrôleurs type=jsonrpc. Leur calendrier de dépréciation n’est pas commun.
- Ne pas confondre méthode Python publique et méthode exposable par RPC : vérifier aussi @api.private/get_public_method.
- Garder une opération métier atomique dans un seul appel modèle lorsque plusieurs écritures doivent être transactionnelles; protéger explicitement sa méthode publique.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'get_public_method|call_kw|json/2|jsonrpc|xmlrpc' addons/rpc addons/web/controllers odoo/service
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Copier la session du web client comme contrat externe; exposer une méthode privée; multiplier les appels non atomiques; confondre JSON-2 et JSON-RPC.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
// Dans setup() d’un composant Odoo, sur la branche compatible :
this.orm = useService('orm');
// Depuis un événement :
const rows = await this.orm.searchRead('res.partner', domain, ['name'], { limit: 20 });
```

## Relevant core files

- [`addons/rpc/controllers/json2.py` · `WebJson2Controller`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/rpc/controllers/json2.py#L22) — `WebJson2Controller`.
- [`addons/rpc/controllers/jsonrpc.py` · `JSONRPC`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/rpc/controllers/jsonrpc.py#L10) — `JSONRPC`.
- [`addons/web/controllers/dataset.py` · `DataSet`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/controllers/dataset.py#L13) — `DataSet`, `DataSet.call_kw`.
- [`odoo/service/model.py` · `Params`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/service/model.py#L33) — `Params`, `get_public_method`, `call_kw`, `dispatch`, `execute_cr`, `retrying`, `_traverse_containers`.
- [`addons/web/static/src/core/orm_service.js` · `x2ManyCommands`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/orm_service.js#L1) — `x2ManyCommands`, `UPDATE_METHODS`, `ORM`, `ormService`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

JSON-2 nouveau en 19. XML/JSON-RPC externes dépréciés; vérifier l’échéance dans la documentation officielle actuelle plutôt que la figer.

## Checklist

Client interne/externe identifié; transport de branche; droits; transaction; erreurs et retries.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
