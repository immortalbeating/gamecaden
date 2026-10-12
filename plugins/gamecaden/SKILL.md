---
name: gamecaden
description: Use only when the user explicitly requests Gamecaden for this work, or effective guidance in the current project has adopted Gamecaden. Organize game requirements, design, development, assets, verification and continuation; retain the project's original records and authorized scope.
---

# Gamecaden

This is the standalone Skill entrypoint for the complete package. Resolve relative paths from this file's directory; the eight responsibilities and shared documents, tools and templates remain in this directory.

First check the applicability conditions above; when they are not met, follow the original project guidance. See [Workflow applicability](shared/workspace.md) for boundaries.

Read [flow](skills/flow/SKILL.md) and locate the next action from the current request and original work. When the user explicitly names a responsibility, read the corresponding [init](skills/init/SKILL.md), [brainstorm](skills/brainstorm/SKILL.md), [design](skills/design/SKILL.md), [develop](skills/develop/SKILL.md), [assets](skills/assets/SKILL.md), [verify](skills/verify/SKILL.md) or [close](skills/close/SKILL.md) directly, retain existing design and authorization, and complete the original request.

A standalone installation calls this entrypoint and the responsibility files within the package; read back the actual callable names from the host. See [Instructions](INSTALL.md) for installation and updates. Reading the text does not require Python; before actually adopting a project, the first local I/O, or starting the panel, read [Tool readiness and invocation](shared/local-io.md#1-environment-and-invocation) and check the environment. Read-only consultation or init inspect does not automatically install anything or write project guidance.
