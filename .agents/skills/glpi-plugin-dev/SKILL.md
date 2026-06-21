---
name: glpi-plugin-dev
description: Develop, review, and guide GLPI plugin work for GLPI 10.x and 11.x, especially for users who administer GLPI and know basic PHP but are new to plugin development. Use when creating plugin structures, setup.php/hook.php, migrations, CommonDBTM objects, front files, controllers, hooks, menus, tabs, dropdowns, search options, CronTasks, Massive Actions, notifications, JavaScript, tests, or when reviewing whether a GLPI customization can be implemented safely inside a plugin without changing GLPI core.
---

# GLPI Plugin Dev

## Core Rules

- Respond to the user in Portuguese (PT-BR).
- Follow the active repository instructions for generated code. If `AGENTS.md` says code comments must be English, keep comments in generated code in English.
- Never edit GLPI core, `vendor/`, global configuration, another plugin, or any path outside the target plugin directory.
- Only edit the target plugin directory, normally `glpi/plugins/{pluginkey}/` or `glpi/marketplace/{pluginkey}/`.
- Read GLPI core and installed plugins when needed, but treat them as read-only reference material.
- Always inspect the local GLPI source before deciding an implementation path. If no local GLPI source is available, stop and ask the user to provide one or to work inside a GLPI checkout.
- Keep implementation guidance aligned one-to-one with the latest official documentation available through `curl`; if `curl` fails, request network access or stop and ask the user for the current documentation instead of relying on stale memory.
- Always prefer GLPI core APIs, classes, helpers, hooks, migrations, search engine, dropdowns, rights, and UI patterns over custom utilities.
- If no official or local reusable GLPI API/hook/helper is clear, stop before generating code. Explain the gap, propose plugin-only alternatives, and ask the user to choose.
- Do not invent fallback behavior unless the user explicitly asks for it.
- Keep code production-oriented: simple responsibilities, strict types where compatible with GLPI/PHP version, no broad catch blocks, no silent failures, no unnecessary abstractions.
- Preserve GLPI method signatures exactly when overriding/extending GLPI classes, even if active repository preferences would normally avoid default parameters or weaker types. Framework compatibility wins.

## Required Workflow

1. Identify the target GLPI root and target plugin directory.
2. Run the Version Detection Gate before choosing GLPI 10.x or 11.x patterns.
3. Confirm the plugin key is alphanumeric only. GLPI plugin directory names must not contain hyphens, underscores, accents, or other characters.
4. Read active `AGENTS.md` files and the local plugin/core files relevant to the request.
5. Validate current official documentation with `curl` before implementing or answering detailed API questions. Prefer official pages under `https://glpi-developer-documentation.readthedocs.io/en/master/`.
6. If the official `pluginsGLPI/example` plugin is available locally, inspect it as a pattern catalog, but never copy version-incompatible code without checking the target GLPI version.
7. Compare the request against local GLPI source to find existing APIs, hooks, examples, and naming conventions.
8. Map the requested feature through `references/architecture.md` before creating files or custom helpers.
9. Choose the smallest plugin-only implementation that uses GLPI mechanisms for the detected/confirmed GLPI version.
10. Generate or edit only files under the target plugin directory.
11. Validate with the repository's existing commands when available, such as PHP lint, coding standards, plugin checks, or GLPI test commands.
12. In the final answer, state the detected GLPI version evidence, what was changed, what was validated, and any docs/core facts that affected the design.

## Version Detection Gate

Always detect and report the local GLPI version before implementation:

1. Locate GLPI root by checking for files/directories such as `inc/define.php`, `inc/includes.php`, `src/`, `plugins/`, and `marketplace/`.
2. Search for the version declaration with `rg -n "GLPI_VERSION|define\\('GLPI_VERSION'|const GLPI_VERSION"`.
3. Prefer the core version declaration, usually in `inc/define.php`, as primary evidence.
4. Use plugin metadata, Composer files, or the official example plugin compatibility only as secondary evidence.
5. Report the exact evidence to the user, including file and line.
6. If no local GLPI source/version is available, stop and ask the user to provide a GLPI checkout or choose a target version.
7. If the user-requested version conflicts with the local core or plugin metadata, stop and ask for confirmation before generating code.

Version behavior:

- GLPI 10.x: prefer `front/*.php`, hooks, `src/` classes, `setup.php`, and `hook.php`; do not generate Symfony plugin controllers unless official docs and local core prove support.
- GLPI 11.x: controllers, routing, and Twig may be used when official docs and local core confirm the pattern.
- Unknown version: do not proceed with version-sensitive implementation.

## Reference Selection

Load only the reference files needed for the task:

- `references/structure.md`: plugin folder layout, `setup.php`, `hook.php`, PSR-4, Composer, install boundaries.
- `references/database.md`: migrations, table naming, install/update/uninstall, plugin data cleanup.
- `references/objects.md`: `CommonDBTM` objects, CRUD front files, forms, list views, rights, search options.
- `references/hooks.md`: `$PLUGIN_HOOKS`, standard hooks, automatic hooks, menu/config/display hooks.
- `references/controllers.md`: controller guidance and the GLPI version boundary. Current master docs say plugin controllers require GLPI >= 11.0.
- `references/tips.md`: menus, tabs, dropdowns, CronTasks, Massive Actions, notifications, JavaScript, tests, and validation checklist.
- `references/testing.md`: test taxonomy, naming, output contract, and what qualifies as unit vs integration/E2E/probe in this plugin context.
- `references/example-plugin.md`: lessons from the official example plugin structure and what to reuse or avoid.
- `references/version-matrix.md`: GLPI 10.x vs 11.x decision matrix.
- `references/architecture.md`: feature-to-GLPI-mechanism matrix to avoid custom workarounds.
- `references/security.md`: rights, session, form, and mutation safety checklist.
- `references/packaging.md`: release, marketplace metadata, translation, and distribution checklist.
- `references/translation.md`: gettext helpers (`__`, `__s`, `_n`, `_x`, `_nx`), folder structure, `.pot`/`.po`/`.mo` workflow, xgettext extraction, Transifex CI, JS translation, and antipatterns.
- `references/corporate-readiness.md`: production-readiness checks for enterprise plugins.
- `references/antipatterns.md`: explicit patterns to reject before generating code.

## Decision Checklist

Before writing code, verify:

- The target directory is the plugin being developed, not GLPI core or another plugin.
- The requested behavior can be expressed with plugin extension points.
- The GLPI version target is detected from local `GLPI_VERSION` and confirmed when ambiguous or conflicting.
- The official docs were refreshed with `curl` when behavior depends on GLPI APIs.
- Rights, session, CSRF/form handling, and plugin-only mutation boundaries are clear.
- The feature is mapped to official GLPI extension mechanisms instead of custom utilities.
- Existing local code does not already implement the logic.
- New tables follow `glpi_plugin_{pluginkey}_{items}`.
- `setup.php` declares version and requirements and registers classes/hooks.
- `hook.php` contains install/update/uninstall hooks when database/files/default config are needed.
- Uninstall removes plugin-created tables, config, generated files under GLPI plugin data directories, and plugin-specific state.

## Documentation URLs

Use these pages as entry points and refresh them with `curl` during work:

- Guidelines: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/guidelines.html`
- Requirements: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/requirements.html`
- Database: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/database.html`
- Objects: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/objects.html`
- Hooks: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/hooks.html`
- Controllers: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/controllers.html`
- CronTasks: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/crontasks.html`
- Massive Actions: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/massiveactions.html`
- Notifications: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/notifications.html`
- Tests: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/test.html`
- JavaScript: `https://glpi-developer-documentation.readthedocs.io/en/master/plugins/javascript.html`
- Coding standards: `https://glpi-developer-documentation.readthedocs.io/en/master/codingstandards.html`
