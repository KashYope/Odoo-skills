---
name: odoo-mail
description: "Réutiliser chatter, activités, templates et bus. Utiliser pour les tâches Odoo relevant de mail et appliquer avant toute implémentation correspondante."
---

# odoo-mail

## Purpose

Réutiliser chatter, activités, templates et bus.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Vérifier mail.thread/mail.activity.mixin déjà hérités avant d’ajouter des mixins ou modèles.
- Utiliser message_post, activity_schedule et templates pour leurs usages prévus; distinguer message, notification et email sortant.
- Préserver followers, sous-types, droits et échappement du HTML. Ne pas appeler bus directement pour simuler une notification métier complète.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'mail.thread|mail.activity.mixin|message_post|activity_schedule' addons/{mail,sale,crm,project}
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Serveur email maison; table de notifications parallèle; ajout automatique de followers sans besoin; HTML non échappé.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
record.message_post(body='Traitement terminé.')
# Seulement sur un modèle compatible, avec droits et destinataires vérifiés.
```

## Relevant core files

- [`addons/mail/models/mail_thread.py` · `MailThread`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/models/mail_thread.py#L64) — `MailThread`, `MailThread.create`, `MailThread.write`, `MailThread.message_post`.
- [`addons/mail/models/mail_activity_mixin.py` · `MailActivityMixin`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/models/mail_activity_mixin.py#L15) — `MailActivityMixin`, `MailActivityMixin.activity_schedule`.
- [`addons/crm/models/crm_lead.py` · `CrmLead`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/crm/models/crm_lead.py#L84) — `CrmLead`, `CrmLead._prepare_values_from_partner`, `CrmLead._prepare_address_values_from_partner`, `CrmLead._prepare_contact_name_from_partner`, `CrmLead._prepare_partner_name_from_partner`, `CrmLead.create`, `CrmLead.write`.
- [`addons/project/models/project_project.py` · `ProjectProject`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/project/models/project_project.py#L23) — `ProjectProject`, `ProjectProject.create`, `ProjectProject.write`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

Mixins relativement stables; payloads mail/bus, stores frontend et méthodes _notify_* internes sont sensibles.

## Checklist

Mixin existant; destinataires; accès; sous-types; pas de notification en double.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
