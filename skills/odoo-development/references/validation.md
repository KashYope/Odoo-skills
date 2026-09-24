# Validation de la bibliothèque

## Contrôles exécutés

| Vérification | Résultat | Limite |
|---|---|---|
| Frontmatter et structure | 29 skills validés avec le validateur officiel | Ne prouve pas la justesse métier |
| Sources | Chemins vérifiés dans l’arbre 19; symboles des primitives Python contrôlés par AST | Un symbole existant ne garantit pas sa stabilité |
| Extraction routes | 943 déclarations; 1 000 occurrences de chemins littéraux; aucune erreur de parsing | Les chemins dynamiques et l’héritage effectif restent à résoudre |
| Corpus contrôleurs | Tous les fichiers Python controllers hors __init__ identifiés dans l’arbre 19 sont récupérés | Pas les addons tiers/Enterprise ni tout code dynamique hors corpus |
| Extracteur | Trois tests passent : métadonnées/héritage vide, alias/expression dynamique, erreur de syntaxe | Tests d’indexation, pas d’un serveur Odoo |
| Recherche | Requêtes par module et par besoin exécutées sur JSONL | Recherche lexicale; relire sources/helpers |
| Essai comportemental portail | L’agent réutilise /my/orders avec PDF et contrôle natif; rejette la lecture sudo arbitraire | Aucun PDF rendu; base utilisateur inconnue |
| Essai comportemental upgrade | L’agent distingue aliases dépréciés, absence native en 17 et changement transactionnel du cron | Portage proposé, pas exécuté |

## Essai 1 : téléchargement de devis

Demande : télécharger des devis depuis le portail, avec suggestion d’une route publique utilisant sudo.

Décision produite : réutiliser `/my/orders/<id>?report_type=pdf&download=true`; contrôler le document via le flux standard. Sources retrouvées : `sale.CustomerPortal.portal_order_page`, `portal.CustomerPortal._document_check_access`, `PortalMixin.get_portal_url`; deuxième usage dans purchase. L’agent distingue bien les droits du client d’un jeton de partage valide et propose des tests de refus par changement d’ID/jeton.

## Essai 2 : passage 17 vers 19

Demande : routes `type=json`, cron `_notify_progress`, tableau de bord `read_group`, avec préférence pour une implémentation commune.

Décision produite : logique métier commune possible; adaptations explicites pour décorateur et orchestration cron. L’agent détecte l’absence de `_notify_progress` dans le core 17 analysé et demande d’identifier le backport. Il distingue `done` absolu de `processed` incrémental, ainsi que le commit de `_commit_progress`. Il ne confond pas tuples de `_read_group` et dictionnaires formatés de `read_group`.

La définition serveur de `formatted_read_group` a ensuite été ajoutée au corpus : `addons/web/models/models.py`, `Base.formatted_read_group`. Le format doit toujours être vérifié avant de porter le tableau de bord.

## Non exécuté

- Installation d’un module dans Odoo/PostgreSQL.
- Tests TransactionCase/HttpCase/Owl d’un addon réel.
- Génération PDF, rendu de vues ou migration de base.
- Vérification de tous les addons installés chez l’utilisateur.
- Garantie de fonctionnement sur une prochaine version.

Les skills sont opérationnels comme contraintes et outils de recherche. Leur bibliothèque de références réduit le risque; elle ne remplace pas les tests du module développé.
