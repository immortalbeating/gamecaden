<a id="项目目录与文件职责"></a>
# Project directories and file responsibilities

Read this when creating project structure, adding modules/production pipelines, migrating paths, or when directory responsibilities are unclear. Follow [workspace](../shared/workspace.md) for project/runtime roots and record ownership; do not rearrange unrelated existing projects for tidy directories.

<a id="应统一的边界"></a>
## Boundaries to keep consistent

| ID | Conditions and requirements | Basis for checking |
|---|---|---|
| LAYOUT-ROOT | **Required**: Each actual runtime root has a locatable engine/startup identifier; games, offline tools, design packages and generators in one repository state their respective purposes. When no runtime project exists, retain the target choice without inventing an existing entry point. | Reading relationships from the selected entry to actual configuration/source/resources; a document title or repository name alone does not determine the engine. |
| LAYOUT-AUTHORITY | **Required**: Work records, design sources, runtime content, production inputs and generated outputs have distinguishable responsibilities; each fact has one maintained source. | Which content changes runtime/design when edited; names and sources distinguish snapshots, derived copies and independent candidates. |
| LAYOUT-IDENTITY | **Required**: Resource moves/renames preserve actual engine identity, case and references, and recheck affected imports, resource keys, scenes and build paths. | Check Godot resource references, Unity `.meta`/GUID, Creator `.meta`/UUID/sub-assets, and Web URL/build paths according to the respective profile. |
| LAYOUT-GENERATED | **Required**: Treat rebuildable caches separately from metadata that carries identity; generated outputs have sources and generation methods, and actual unsaved inputs are not deleted as caches. | Existing tool, engine and version-control conventions; inclusion in Git/packages depends on purpose and project policy, not just folder names. |
| LAYOUT-BOUNDARY | **Required**: Reusable units or independent lifecycles have understandable entry points/interfaces; **default**: group by feature, or retain clear existing type-based directories. | Related objects can be located for modification, instantiation, exit and reuse; file/scene counts do not establish modularity. |

<a id="新项目的默认安排"></a>
## Default arrangement for new projects

The following illustrates responsibilities; it is not a complete directory tree that must be created:

```text
project-root/
├── AGENTS.md                 Existing entry or brief guidance needed for adoption
├── game-workflow/            Configurable: workflow mapping, current rules and work records
├── <runtime-root>/           May be the project root; follows actual engine conventions internally
├── tools/                    Used when project tools/generators exist
└── artifacts/                Used when rebuildable reports/build outputs need to be retained
```

- A single runtime root may be the project root; adding `game/` is not mandatory. Retain Godot feature scenes/resources, Unity/Creator engine directories, and existing Web build/no-build structure respectively.
- Establish definite entries for the current Vision/necessary Spec overview/Roadmap according to [workspace adoption rules](../shared/workspace.md#default-locations-for-new-materials); retain the locations and maintenance scopes of older detailed materials and existing Task/Epic records. Routine continuation does not automatically migrate them to new default locations.
- Production sources, candidates and adopted content may use separate directories or a reliable ledger/manifest; adoption status comes from original records, not guesses based on `final/`, `approved/` or timestamps.
- When the team/framework has no naming convention, default to portable, case-consistent, searchable names; continue using valid existing names. Fix actual cross-platform conflicts; stylistic differences alone do not trigger repository-wide renaming.
- Handle inputs, user saves, API configuration and credentials within their actual host storage boundaries; workflow records must not become mixed storage for runtime saves or private configuration.

<a id="新建与旧项目的处理"></a>
## Handling new and existing projects

init registers only the paths, identities and adopted rules needed now; develop/assets create directories as actual outputs appear. Brief structural choices can go in an existing Spec or entry description, without another mandatory "directory master ledger".

Default storage/promotion of Task-specific evidence, standalone reports and shared materials follows [shared records](../shared/records.md#retention-indexing-and-versions); [actual problems](../shared/records.md#8-organize-according-to-actual-problems), such as hard-to-find goals/next steps, duplicate maintenance and broken references, trigger organization. The directory illustration does not imply cleaning up formal evidence as rebuildable caches; older flat attachments need not be moved for layout consistency.

Use an existing layout directly when responsibilities and consumers can be located. Include migration only for references, confusion or tool limits affecting this delivery; check actual readers and resource identity beforehand, then affected entries, imports and delivery paths afterward. Preserve existing uncommitted work, candidates and user inputs.

When new independent pages/levels, cross-lifecycle state, reusable units or editing needs change, first explain boundaries using the [engineering structure contract](references/structure-contract.md). An agreement to temporarily retain an existing layout applies only within its original scope; when this defect comes from incorrect ownership, relevant structural adjustment is needed for delivery and cannot be postponed on the grounds of "reusing the old structure". Composition explains responsibility better than directory/scene counts.

Independently released tools may have their own stack, build and rule scope; for example, an HTML panel in a Godot repository follows Web entries, without registering the game engine as Web.
