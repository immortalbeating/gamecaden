# Maintenance entry

This repository maintains the Gamecaden toolkit. Read [README](README.md) and the current task scope first. Preserve existing worktree changes and modify only files owned by this work.

- For responsibilities or trigger changes, read the corresponding `plugins/gamecaden/skills/*/SKILL.md` and referenced `shared/` contracts; package contracts define detailed behavior.
- For sources, I/O, or panel changes, read [architecture](docs/architecture.md) and the relevant shared contracts. Preserve original source authority, revision checks, and recovery semantics.
- Root `tests/` and `scripts/` are maintenance entries; `plugins/gamecaden/` is the public plugin, and `dist/` holds build artifacts.
- Run `python scripts/check.py --suite core` or `--suite distribution` according to impact; run `--suite all` before release. See [validation](docs/validation.md) for coverage.
- Maintain code interfaces, schemas, workflow contracts, references, and templates in English. Project materials follow the user's selected language under [language preferences](plugins/gamecaden/shared/workspace.md#6-language-preferences); English templates must not force English outputs.
- Report actual commands, results, and unverified scope. Keep program checks, model behavior, runtime adoption, and user acceptance separate.
- Public material uses anonymous examples only. Credentials, local paths, private logs, business-project records, and complete local Chinese rule comparisons stay outside the public package and history.

Maintaining this toolkit does not automatically authorize running games, modifying external projects, committing, pushing, or publishing.

The sole active repository is immortalbeating/gamecaden. Preserve archived private history locally; never push private history refs or internal evidence into this public repository.
