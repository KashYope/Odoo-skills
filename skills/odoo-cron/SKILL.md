---
name: odoo-cron
description: "Réutiliser ir.cron et ses traitements batch. Utiliser pour les tâches Odoo relevant de cron et appliquer avant toute implémentation correspondante."
---

# odoo-cron

## Purpose

Réutiliser ir.cron et ses traitements batch.

## When to use

Appliquer à la responsabilité indiquée; commencer par `odoo-search-before-code`. Fixer la version cible avant de copier un exemple.

## Core rules

- Chercher une tâche/automatisation existante. Configurer ir.cron pour une méthode modèle plutôt qu’un scheduler externe.
- Traiter des lots bornés, documenter idempotence et utilisateur d’exécution. Prévoir interruptions et relances sans doublon métier.
- Utiliser l’API de progression de la version. L’exception transactionnelle du framework cron n’autorise pas les commits dans les autres méthodes.

## Search before coding

Depuis la racine du dépôt Odoo cible, adapter les marqueurs entre chevrons :

```sh
rg -n 'ir.cron|_cron_|_commit_progress|_notify_progress' addons/<module> odoo/addons/base/models/ir_cron.py
```

## Preferred Odoo patterns

Configuration → réutilisation → héritage → composition → petit adaptateur → nouveau code justifié.

## Patterns to avoid

Boucle infinie; sleep; cron doublonné; rescheduling manuel sans nécessité; utilisateur superadmin par défaut.

## Minimal implementation pattern

Exemple structurel ou procédure; supprimer toute surcharge sans delta réel. Compléter imports/dépendances seulement si nécessaire.

```
19 : traiter un lot borné puis appeler env['ir.cron']._commit_progress(processed, remaining=remaining) selon le contrat lu; arrêter si le temps restant retourné est nul. Ne pas copier cet appel sur 17/18.
```

## Relevant core files

- [`odoo/addons/base/models/ir_cron.py` · `BadVersion`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/odoo/addons/base/models/ir_cron.py#L44) — `BadVersion`, `BadModuleState`, `CompletionStatus`, `ListLogHandler`, `IrCron`, `IrCron.create`, `IrCron.write`.
- [`addons/mail/models/mail_thread.py` · `MailThread`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/mail/models/mail_thread.py#L64) — `MailThread`, `MailThread.create`, `MailThread.write`, `MailThread.message_post`.
- [`addons/base_automation/models/base_automation.py` · `_get_domain_fields`](https://github.com/odoo/odoo/blob/2e2acfd6d2725d1a4a95b1a6056334e1ac34163f/addons/base_automation/models/base_automation.py#L31) — `_get_domain_fields`, `_domain_fields_differences`, `_keep_to_compute`, `get_webhook_request_payload`, `BaseAutomation`, `BaseAutomation.create`, `BaseAutomation.write`.

## Relevant standard modules

Étudier les usages dans les modules des chemins ci-dessus; ne pas confondre preuve d’usage et API publique garantie.

## Version compatibility notes

17 natif analysé : aucune de ces deux méthodes; identifier tout backport. 18 : _notify_progress (done absolu). 19 : _commit_progress (processed incrémental + commit); l’ancien est déprécié. Ne pas renommer mécaniquement.

## Checklist

Lots; relance; droits; budget; supervision; API de version vérifiée.

Avant livraison, fournir sources chemin + classe/fonction, choix rejetés, delta et tests exécutés. Ne pas annoncer une compatibilité non testée.
