---
name: odoo-development
description: "Orchestrer le développement, la maintenance et les upgrades de modules Odoo en recherchant les primitives natives avant tout code. Utiliser pour toute demande Odoo impliquant architecture, modèle, vue, contrôleur, route, frontend, sécurité ou migration."
---

# odoo-development

## Purpose

Ne jamais écrire du code qu’Odoo sait déjà faire. Minimiser le delta custom sous contraintes de sécurité, lisibilité, testabilité et coût total des dépendances.

## When to use

Commencer ici pour toute implémentation ou maintenance Odoo. Charger ensuite uniquement les skills correspondant au changement.

## Core rules

1. Fixer besoin, branche/SHA, édition, hébergement et modules installés; ne pas supposer une fonctionnalité Enterprise disponible dans Community.
2. Appliquer `odoo-search-before-code` avant le premier diff.
3. Comparer configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code. Justifier les options rejetées.
4. Lire contrat + deux usages standards lorsque disponibles; fournir chemin, classe/fonction et version. Une occurrence core ne justifie pas une règle générale.
5. Conserver super, droits, transactions, recordsets, XML IDs et données utilisateur. Ne pas copier le core.
6. Choisir le plus petit ensemble de skills ci-dessous; ne pas charger toute la bibliothèque en contexte.
7. Exécuter les tests pertinents et distinguer « vérifié statiquement » de « compatible testé ». Ne garantir aucune version future.

## Search before coding

Suivre [decision-workflow.md](references/decision-workflow.md). Lire [architecture.md](references/architecture.md) si le module propriétaire est inconnu; [primitives.md](references/primitives.md) et [extension-points.md](references/extension-points.md) pour choisir le mécanisme. Consulter [evidence.md](references/evidence.md) pour les sources et [coverage.json](references/coverage.json) pour le périmètre réel.

Avant toute route, consulter [routes-families.md](references/routes-families.md), puis interroger [routes.jsonl](references/routes.jsonl), sans charger tout l’index dans le contexte :

```sh
# Depuis le dossier de ce skill :
python3 scripts/query_routes.py references/routes.jsonl --query 'attachment' --limit 8
python3 scripts/query_routes.py references/routes.jsonl --module portal --limit 8
# Régénération sur un checkout de la version cible :
python3 scripts/extract_routes.py /chemin/odoo --version VERSION --sha SHA --out /chemin/routes.jsonl
```

L’index porte les déclarations statiques, y compris les overrides sans URL et les routes de test. Il ne résout pas la MRO effective ni les modules installés. Ne jamais en déduire seul une autorisation, une API publique ou une absence de route.

## Routage vers les skills spécialisés

| Travail | Skills à charger |
|---|---|
| Toujours avant code | odoo-search-before-code |
| Architecture et manifest | odoo-architecture, odoo-module-architecture |
| Entité ou héritage | odoo-models, odoo-model-inheritance |
| Données et calculs | odoo-orm, odoo-fields |
| Workflow métier | odoo-business-logic |
| Formulaire, liste, menu, bouton | odoo-views, odoo-actions |
| Droits et exposition | odoo-security |
| HTTP ou intégration | odoo-routes, odoo-controllers, odoo-rpc |
| Site ou espace client | odoo-website, odoo-portal |
| Interface JavaScript | odoo-frontend, odoo-owl, odoo-assets |
| Planification | odoo-cron |
| Email, chatter, activités | odoo-mail |
| Documents et échanges | odoo-reports, odoo-import-export |
| Validation et diagnostic | odoo-testing, odoo-debugging, odoo-performance |
| Upgrade et maintenance | odoo-version-compatibility, odoo-upgrade-safe-development |

Résoudre les skills par leur nom déclaré dans le frontmatter via le catalogue disponible. Leur dossier physique peut changer; ne pas coder de chemin frère fixe. Si un skill manque, signaler la lacune et appliquer les références pertinentes présentes ici.

## Preferred Odoo patterns

`_inherit` pour extension en place; hooks `_prepare_*`/`_get_*` adaptés; ORM batch; related justifié; XML hérité; action standard; service orm; registry/widget; mixins mail/portal; ir.cron; ir.actions.report; import/export natifs.

## Patterns to avoid

Lire [anti-patterns.md](references/anti-patterns.md). Refuser core modifié, monkey patches, méthode/vue recopiée, sudo pour contourner un refus, SQL sans justification, IDs numériques, route CRUD miroir et JS superflu. Le mécanisme officiel `patch` JS reste un dernier recours documenté, pas le choix par défaut.

## Minimal implementation pattern

Produire : besoin vérifiable → sources trouvées → alternatives rejetées → point d’extension et statut → delta → tests et résultats → risque upgrade. Si la configuration suffit, livrer les réglages et aucun code.

## Relevant core files

`odoo/http.py` (`route`, `_generate_routing_rules`); `odoo/orm/models.py` (`BaseModel`); `odoo/modules/loading.py`; `odoo/service/model.py` (`call_kw`, `get_public_method`); `addons/web/controllers/dataset.py` (`DataSet.call_kw`). Liens figés et autres symboles dans [evidence.md](references/evidence.md).

## Relevant standard modules

Comparer notamment sale/purchase, crm/project, auth_signup/website, portal/sale, mail/bus et web/base_import. Une extension interne répandue reste à revérifier sur la version cible.

## Version compatibility notes

Base d’analyse : Odoo 19; comparaison ciblée 17/18. Lire [version-compatibility.md](references/version-compatibility.md). `master` n’est pas une version supportée. Les conventions `json`/`jsonrpc`, authentification, cron, ORM, contraintes et imports frontend changent. Le calendrier de dépréciation des RPC externes doit être revalidé.

## Checklist

- Besoin et version fixés; existant recherché; sources vérifiables.
- Aucune nouvelle abstraction, route, dépendance ou surcharge sans justification.
- Sécurité et métier conservés; delta lisible; données préservées.
- Tests exécutés identifiés; limites et compatibilité non testée explicites.

Pour relire la composition, consulter [skill-set.md](references/skill-set.md). Pour les vérifications, consulter [validation.md](references/validation.md).
