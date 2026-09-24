# Odoo Skills

[Français](README.md) · English

29 operational skills guiding AI agents through Odoo module development, maintenance and upgrades. This library is grounded in the [official source code](https://github.com/odoo/odoo) and standard addons. It contains instructions, references and search tools; it is not an Odoo addon.

> **Never write code that Odoo already provides.**

## Policy: stay close to upstream source

Before implementing anything, search the target version for existing models, fields, methods, mixins, controllers, routes, services, components, views, actions, configuration and security mechanisms.

Use this mandatory order of preference:

1. Existing Odoo configuration.
2. Reuse of native functionality.
3. Focused inheritance or extension.
4. Composition of existing primitives.
5. A small adapter.
6. New code only as a last resort.

When configuration is sufficient, deliver the configuration steps and **no code**. For equivalent functionality, minimize dependencies, overrides, routes, JavaScript and duplication. Security, readability and testability remain requirements: fewer lines never justify bypassing access controls.

Staying close to source means understanding and using its contracts and extension points, without copying methods or modifying core. Support each major decision with the version or SHA, repository path and class/function, plus multiple standard usages where available. Widely used internal APIs still require upgrade checks.

## How it works

Start with [odoo-development](skills/odoo-development/SKILL.md). It requires [odoo-search-before-code](skills/odoo-search-before-code/SKILL.md), then selects only the relevant specialist skills. Do not load the entire library or route index into the agent’s context.

The workflow is: verifiable requirement → Odoo domain → standard addon → models/fields/methods → routes/controllers → frontend services → views/actions/configuration → most stable extension point → minimal delta → tests and version checks.

Before coding, the agent must provide:

- The relevant version, edition and installed modules.
- Existing capabilities found and their source references.
- The selected approach and reasons for rejecting more native alternatives.
- The necessary delta, tests to run and upgrade risks.

Prefer `_inherit`, cooperative `super()`, narrow hooks, batch ORM operations, focused XML inheritance, services/registries/widgets, and native mail, cron, reporting and import/export primitives. Avoid copied methods or views, redundant CRUD routes, numeric IDs, SQL when the ORM suffices, and `sudo()` used to bypass denied access.

## Using the library with an agent

1. Clone this repository and give the agent access to a checkout of the actual target Odoo version.
2. Install complete folders from `skills/` into the agent’s supported skills directory, preserving `references/`, `scripts/`, `agents/` and `assets/`.
3. If the agent does not support skill installation, ask it to read `skills/odoo-development/SKILL.md`, then the selected specialist files.
4. Specify the requirement, version, edition and available modules. Discovery mechanisms depend on the agent.

Example instruction:

```text
Apply odoo-development and odoo-search-before-code.
Project: Odoo 19 Community with sale and portal installed.
Requirement: let customers download their quotation as a PDF.
First search for the native flow, its routes and access checks.
Justify any additional code with references to the target checkout.
If Odoo covers the requirement, provide only the necessary configuration.
```

Skills and references are written in French; the two READMEs explain the same workflow in French and English.

## Contents

| Domaine / Domain | Skills |
|---|---|
| Pilotage / Coordination | [odoo-development](skills/odoo-development/SKILL.md), [odoo-search-before-code](skills/odoo-search-before-code/SKILL.md), [odoo-architecture](skills/odoo-architecture/SKILL.md), [odoo-module-architecture](skills/odoo-module-architecture/SKILL.md) |
| Données et métier / Data and business logic | [odoo-models](skills/odoo-models/SKILL.md), [odoo-orm](skills/odoo-orm/SKILL.md), [odoo-fields](skills/odoo-fields/SKILL.md), [odoo-model-inheritance](skills/odoo-model-inheritance/SKILL.md), [odoo-business-logic](skills/odoo-business-logic/SKILL.md) |
| Interface / UI | [odoo-views](skills/odoo-views/SKILL.md), [odoo-actions](skills/odoo-actions/SKILL.md), [odoo-frontend](skills/odoo-frontend/SKILL.md), [odoo-owl](skills/odoo-owl/SKILL.md), [odoo-assets](skills/odoo-assets/SKILL.md) |
| Web et accès / Web and access | [odoo-security](skills/odoo-security/SKILL.md), [odoo-controllers](skills/odoo-controllers/SKILL.md), [odoo-routes](skills/odoo-routes/SKILL.md), [odoo-rpc](skills/odoo-rpc/SKILL.md), [odoo-website](skills/odoo-website/SKILL.md), [odoo-portal](skills/odoo-portal/SKILL.md) |
| Services fonctionnels / Functional services | [odoo-cron](skills/odoo-cron/SKILL.md), [odoo-mail](skills/odoo-mail/SKILL.md), [odoo-reports](skills/odoo-reports/SKILL.md), [odoo-import-export](skills/odoo-import-export/SKILL.md) |
| Qualité et évolution / Quality and upgrades | [odoo-testing](skills/odoo-testing/SKILL.md), [odoo-debugging](skills/odoo-debugging/SKILL.md), [odoo-performance](skills/odoo-performance/SKILL.md), [odoo-version-compatibility](skills/odoo-version-compatibility/SKILL.md), [odoo-upgrade-safe-development](skills/odoo-upgrade-safe-development/SKILL.md) |

- [Architecture](skills/odoo-development/references/architecture.md)
- [Workflow de décision / Decision workflow](skills/odoo-development/references/decision-workflow.md)
- [Primitives](skills/odoo-development/references/primitives.md)
- [Points d’extension / Extension points](skills/odoo-development/references/extension-points.md)
- [Anti-patterns](skills/odoo-development/references/anti-patterns.md)
- [Familles de routes / Route families](skills/odoo-development/references/routes-families.md)
- [Index des routes / Route index](skills/odoo-development/references/routes-index.md)
- [Compatibilité / Compatibility](skills/odoo-development/references/version-compatibility.md)
- [Sources](skills/odoo-development/references/evidence.md)
- [Périmètre du corpus / Corpus coverage](skills/odoo-development/references/coverage.json)
- [Organisation des skills / Skill organization](skills/odoo-development/references/skill-set.md)
- [Validation](skills/odoo-development/references/validation.md)

The corpus contains 53 primitives, 17 extension points, 21 anti-patterns and 39 detailed route profiles. The JSONL index contains 943 static declarations and 1,000 literal path occurrences, including test routes. These counts do not represent unique active endpoints.

## Searching and refreshing routes

From the repository root, using Python 3 and its standard library:

```sh
python3 skills/odoo-development/scripts/query_routes.py \
  skills/odoo-development/references/routes.jsonl --query attachment --limit 8

python3 skills/odoo-development/scripts/query_routes.py \
  skills/odoo-development/references/routes.jsonl --module portal --limit 8

python3 skills/odoo-development/scripts/extract_routes.py /path/to/odoo \
  --version 19.0 --sha "$(git -C /path/to/odoo rev-parse HEAD)" \
  --out /path/to/routes.jsonl

python3 skills/odoo-development/scripts/test_extract_routes.py
```

The extractor parses AST without executing Odoo. It preserves declared metadata, `@route()` overrides and unresolved expressions. It does not resolve effective controller inheritance or installed modules. Omitted `auth` or `csrf` values may be inherited or defaulted. `auth='public'` does not mean the data is public. No index match is not proof that a capability is absent.

## Sources, versions and limitations

Primary analysis: Odoo **19.0**, with 792 retrieved files, including all 318 non-`__init__.py` Python `controllers/` files identified in its tree. Targeted comparisons: 12 files for **17.0** and 12 for **18.0**. `master` received a tree inventory only. This is not an exhaustive audit of every implementation.

| Branche / Branch | Commit analysé / Analyzed commit |
|---|---|
| 19.0 | `2e2acfd6d2725d1a4a95b1a6056334e1ac34163f` |
| 18.0 | `c270965ec11c95e5e2866b30f8fa2c90287c6e8a` |
| 17.0 | `b4c6b344a7a6cef93db339c56edb4feb5b222435` |
| master — inventaire / inventory | `8365a19519cf12321270abc500116d26f2f188e2` |

References distinguish public contracts, relatively stable usages, internal details and recent replacements. Sensitive areas include `json`/`jsonrpc`, cron progress and transactions, `read_group` and replacement output formats, and frontend imports. Always inspect the target version’s source; pinned evidence does not guarantee future compatibility.

Validation performed: structure of all 29 skills, three extractor tests and two agent usage exercises (portal and upgrade). No Odoo/PostgreSQL instance tests, actual PDF rendering or database migration were executed. Enterprise and third-party addons are outside this corpus.

## Contributing

Search Odoo source and existing skills first. Propose the smallest useful change, cite paths/symbols and commits, verify multiple standard usages and identify stability. Update references and the index when scope changes, then run relevant tests. Do not add duplicate skills, dependencies or abstractions.

## License and attribution

See the repository’s [Apache 2.0 license](LICENSE). Referenced Odoo sources remain subject to their own licenses. This independent project is not an official Odoo publication.
