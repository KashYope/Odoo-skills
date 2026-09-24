# Compatibilité et zones sensibles

## Statuts

- **Relativement stable** : API publique ou convention établie, pas garantie pour la prochaine majeure.
- **Interne répandu** : hook utilisé par les addons standards; bonne option locale si aucun contrat public meilleur, à tester à chaque upgrade.
- **Interne fragile** : cache/registry/dispatchers, stores mail, structures internes web; éviter couplage direct.
- **Déprécié/remplacé** : avertissement explicite dans le code ou documentation; adopter le remplacement sur les versions qui le fournissent.
- **Non vérifié** : hors corpus ou non exécuté; ne pas annoncer compatible.

## Différences vérifiées

| Sujet | 17.0 | 18.0 | 19.0 | Conséquence |
|---|---|---|---|---|
| Implémentation ORM | odoo/models.py, fields.py, api.py | mêmes chemins principaux | odoo/orm/*; façades odoo/models, fields, api | Importer depuis odoo; rechercher les définitions dans la bonne arborescence |
| Type route JSON-RPC | json | json | jsonrpc; json alias déprécié | Adapter décorateur; ne pas confondre changement de nom et remplacement du protocole |
| Session.authenticate interne | dbname, login, password | dbname, credential | env, credential | Ne pas copier une authentification provenant d’une autre majeure |
| Cron progression | Pas des deux API observées dans les branches suivantes | _notify_progress(done=, remaining=) | _commit_progress(processed, remaining=); _notify_progress déprécié | Adapter le lot et les commits au contrat, pas seulement renommer |
| Appel RPC frontend | core/network/rpc_service.js | core/network/rpc.js | core/network/rpc.js | Vérifier import; utiliser orm pour le modèle |
| Vues liste | tree | migration tree → list | list | Vérifier tags, view_mode et XPath; script de transformation fourni |
| Contraintes SQL déclaratives | _sql_constraints historique | historique | outil 18.1-00-sql-constraint et objets de contraintes | Lire API cible et migration avant copie d’une ancienne déclaration |
| API externe | RPC historique | RPC historique | addons/rpc/json2 et RPC historiques dépréciés | JSON-2 à étudier pour nouvelles intégrations 19 |

## Autres dépréciations détectées dans le code

- `BaseModel.read_group` : déprécié en 19; le décorateur recommande `_read_group` pour backend ou `formatted_read_group` pour résultat formaté. La définition serveur est dans addons/web/models/models.py, Base.formatted_read_group; vérifier les modules chargés et la forme du résultat. Ce cas interdit la règle simpliste « toute API préfixée _ doit être rejetée ».
- `check_access_rights` et `check_access_rule` : dépréciés depuis 18 dans le corpus; utiliser `check_access` sur 18/19, conserver le contrat historique si 17 est supporté.
- Sources : `odoo/orm/models.py`, `BaseModel.read_group`, `BaseModel.check_access_rights`, `BaseModel.check_access_rule`; comparaison avec `odoo/models.py` 17/18.

## Calendrier RPC

La documentation officielle consultée annonce le retrait des endpoints externes `/xmlrpc`, `/xmlrpc/2`, `/jsonrpc` en Odoo 22 / Online 21.1. Ce calendrier a changé : le revalider au moment du développement. Les autres contrôleurs `type='jsonrpc'` ne sont pas visés par cette annonce. Références : https://www.odoo.com/documentation/19.0/developer/reference/external_api.html et https://www.odoo.com/documentation/19.0/developer/reference/external_rpc_api.html. Vérification web au cours de l’étude; ne pas traiter une date de cache comme preuve de disponibilité dans une instance.

## Sensibilités sans promesse de compatibilité

| Surface | Risque | Mesure imposée |
|---|---|---|
| CRUD/fields/_inherit publics | Relativement stable | Tester recordsets, droits, calculs et opérations batch |
| _prepare_*, _get_* métier | Interne répandu | Comparer signature, retour et chaîne super sur addons installés |
| XML IDs / XPath | Mécanisme stable relatif; cibles modifiables | Charger vues sur chaque majeure et vérifier rendu final |
| Contrôleurs web/portail | Interne évolutif | Lire héritage, paramètres, helpers et réponse; HttpCase négatif |
| Routes dataset | Client web interne | Service orm; éviter contrat d’intégration externe construit sur ses détails |
| Mail/bus/stores | Fragile | Préférer message_post/activités/services; tester permissions et destinataires |
| Owl/services/registries | Points documentés préférables | Vérifier imports, props et harness de tests de la branche |
| SQL / cache / registry Python | Interne fragile | Supprimer couplage; sinon preuve de nécessité et test spécifique |
| Migration schéma/données | Risque de perte métier | Copie de base, sauvegarde, scripts et vérification des invariants |

## Vérification d’une montée de version

1. Figer SHAs et versions des dépendances; établir la liste d’APIs utilisées.
2. Comparer signatures, décorateurs et données XML; isoler chaque changement.
3. Migrer code puis schéma/données selon les procédures adaptées; ne pas lancer une ancienne base directement sur une nouvelle majeure.
4. Tester installation neuve et mise à jour de l’addon sur une base correctement migrée.
5. Exécuter métier, droits, HTTP, frontend et performances pour les surfaces modifiées.
6. Enregistrer compatible testé / adapté non testé / bloqué par dépendance.

`master` est inventorié comme signal exploratoire, pas analysé comme une version supportée et pas couvert par une garantie. Les fichiers upgrade_code ne sont pas un service complet de migration de base. Le dossier odoo/upgrade du corpus ne contient pas l’ensemble des scripts de migration d’Odoo.

## Preuves code

- [`odoo/http.py` · `Session.authenticate`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/http.py#L1228)
- [`odoo/addons/base/models/ir_cron.py` · `IrCron._commit_progress`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_cron.py#L846)
- [`odoo/upgrade_code/18.1-02-route-jsonrpc.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/18.1-02-route-jsonrpc.py#L1)
- [`odoo/upgrade_code/17.5-01-tree-to-list.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/17.5-01-tree-to-list.py#L1)
- [`odoo/upgrade_code/18.1-00-sql-constraint.py` · `module`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/upgrade_code/18.1-00-sql-constraint.py#L1)
- [`addons/rpc/controllers/json2.py` · `WebJson2Controller.web_json_2_rpc`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/rpc/controllers/json2.py#L57)

## Précisions qui changent l’adaptation

- `_notify_progress` n’existe pas dans le fichier ir.cron natif 17 analysé. S’il est présent dans un addon annoncé 17, identifier le backport ou la dépendance.
- `_notify_progress(done=...)` reçoit un avancement absolu; `_commit_progress(processed=...)` ajoute un avancement et commit. Ne pas faire un simple remplacement de nom.
- `_read_group` présente la même signature observée sur 17 et 19 et retourne des tuples, avec des recordsets pour certains groupements. Cela peut servir à partager du code backend, sans garantir les autres détails ni remplacer automatiquement un résultat read_group formaté.
- `check_access` est marqué `@api.private` en 19 : appel serveur autorisé, pas méthode RPC publique. `has_access` est le booléen public; les deux ne remplacent pas les invariants métier.
