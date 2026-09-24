# Architecture utile au développement de modules

## Lecture rapide

Un addon ajoute des modèles, données, vues ou contrôleurs à une base dont les modules installés déterminent le comportement final. Le dépôt seul ne suffit donc pas à connaître ce comportement.

| Couche | Emplacement 19 | Responsabilité | Décision pour un addon |
|---|---|---|---|
| Entrée HTTP | odoo/http.py | Session, dispatchers, paramètres, transactions et routes | Réutiliser route/contrôleur; ne pas remplacer le dispatcher |
| Chargement | odoo/modules/ | Graph des dépendances, données, registry, migrations | Manifest minimal; imports et ordre de données corrects |
| ORM | odoo/orm/ | Recordsets, champs, domaines, accès, cache et persistence | Imports publics depuis odoo; aucune dépendance à l’organisation interne |
| Services serveur | odoo/service/ | Appels modèles et gestion serveur | Méthode métier; ne pas copier call_kw/retrying |
| Base | odoo/addons/base/ | Utilisateurs, groupes, actions, vues, fichiers, cron | Chercher une primitive avant nouvelle abstraction |
| Web | addons/web/ | Client, routes dataset/actions/fichiers/rapports, composants | Vue/action/widget/service avant JS custom |
| Domaine métier | addons/sale, purchase, stock, account, crm, project | États métier, workflows, calculs, hooks | Étendre le modèle propriétaire et son hook étroit |
| Communication | addons/mail, bus | Chatter, activités, notifications | Mixins et services existants |
| Exposition client | addons/portal, website, website_sale | Partage, pages publiées, commerce | Conserver contrôles d’accès et contexte website |
| API externe | addons/rpc | JSON-2 et RPC historiques | Choisir selon version et contrat du client |
| Tests | odoo/tests + addons/*/tests + static/tests | Fixtures, ORM, HTTP et frontend | Tester le delta et les refus, par version |
| Upgrade | odoo/modules/migration.py, odoo/upgrade_code | Migration de données et transformations de code distinctes | Préserver données et XML IDs; ne pas confondre outils |

## Trois registries/concepts à ne pas mélanger

- Registry serveur : classes de modèles assemblées pour la base et ses modules; il porte le MRO effectif.
- Registry frontend : catégories d’extension pour fields/views/actions/services.
- Routage HTTP : classes de contrôleurs combinées en fonction des modules; ce n’est pas une simple liste de décorateurs.

## Séparation des responsabilités

Un formulaire ou un composant collecte des données; le modèle applique les invariants sous les droits courants. Le contrôleur valide le transport et délègue. Une action choisit une présentation. Une vue décrit cette présentation. Une règle de record sécurise l’accès indépendamment de la vue.

Le code standard contient des exceptions de framework (SQL, sudo, commits, API privées). Leur présence ne suffit pas à les recommander aux addons : vérifier pourquoi l’exception est nécessaire et quelles garanties l’entourent.

## Méthode de lecture

1. Manifest et imports : disponibilité, dépendances, données, assets.
2. Modèle et relations : propriété de la donnée, mixins, méthodes, champs existants.
3. Au moins deux usages pertinents : vente/achat pour workflows; vente/projet/CRM pour mixins; signup/website pour héritage contrôleur.
4. Sécurité : ACL, règles, champs protégés, company, méthodes publiques et jetons.
5. Présentation/transport : action, vue, service, route, template.
6. Tests et upgrade : invariants observables, effets de bord, données persistantes.

## Limites

Le corpus est Community officiel. Il n’établit ni disponibilité Enterprise ni conditions d’hébergement. Les arbres sont inventoriés entièrement mais le contenu est analysé par sélection; le registre de preuves décrit les fichiers réellement récupérés. Aucun serveur Odoo/PostgreSQL n’a été exécuté pour cette étude.

## Points d’entrée vérifiables

- [`odoo/http.py` · `_generate_routing_rules`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/http.py#L849)
- [`odoo/orm/models.py` · `BaseModel`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/orm/models.py#L334)
- [`odoo/modules/loading.py` · `load_modules`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/modules/loading.py#L340)
- [`addons/web/static/src/core/registry.js` · `Registry`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/web/static/src/core/registry.js#L64)
- [`addons/sale/models/sale_order.py` · `SaleOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/sale/models/sale_order.py#L34)
- [`addons/purchase/models/purchase_order.py` · `PurchaseOrder`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/purchase/models/purchase_order.py#L21)
