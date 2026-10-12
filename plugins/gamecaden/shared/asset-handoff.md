<a id="资产主台账版本决定与运行交接"></a>
# Asset Master Ledger, Version Decisions, and Runtime Handoff

Asset production in assets, integration in develop, and later review/verification share this convention. See [common records](records.md) for each record's sole responsibility; this page details update timing and handoff judgments without establishing a parallel asset-state system.

When new native ledgers/decisions are actually needed, use the [format contract](formats-v1.md) and [on-demand templates](../templates/catalog.md). [Local I/O tools](local-io.md) provide corresponding operations according to interface contracts; tool documentation defines current version checks, decision-maker binding, and recovery capabilities. Panel bridges and actual host user input still require separate integration validation.

<a id="1-用身份和用途连接记录"></a>
## 1. Connect Records by Identity and Use

A handoff must at least answer: which asset/content, which actual version, where it will be used, on what permitted scope, where files and technical inventories are located, what has been proven, and what remains missing. Existing materials may be directly referenced without a new handoff file each time.

Organize identities by asset families and variants that can actually be used independently; locate candidate versions through existing unambiguous tool IDs, content digests, or versions and file inventories. If a same-named path can be overwritten, the path alone cannot bind a review conclusion. Acceptance of multiple files at once must identify the member set and each version, rather than merely stating “the entire current directory passed.”

The ledger owns the following information, using existing Markdown/YAML or tool formats:

| Ledger content | What to save/reference |
|---|---|
| Identity and use | Stable identifier, name, asset family/variant, and intended consumers |
| Sources and candidates | Source grounds, candidate versions needing retention, corresponding production inventory/manifest references |
| Designated selection relationships | Which version is planned for which use/consumer, supported by which effective selection or acceptance record |
| Replacement and retention relationships | What replaces it, which uses retain it, and related decision/work references |
| Integration grounds entry points | Related engineering consumers and Evidence references for checking actual use |

Technical facts such as dimensions, frame counts, encoding, and per-file digests are owned by manifests/actual files; do not manually copy sufficient existing inventories. Designated selection in the ledger does not replace actual runtime results. In a new project, create the asset master ledger under workspace defaults when independent tracking is first actually needed; directly maintain existing effective ledgers without changing format or opening another ledger for this Skill.

<a id="2-按事件更新对应来源"></a>
## 2. Update Corresponding Sources by Event

| Actual event | Update responsibility |
|---|---|
| An asset identity/candidate is formed for continued use, comparison, or review | Register identity, uses, and version references in the ledger; record this output in the original Task |
| Files are generated, converted, or replaced | Production inventory/manifest reflects actual files; technical check results belong to Evidence |
| User/authorized executor selects, accepts, rejects, or requests revision | Decision or original records save the decision-maker, exact object/version/aspect and use scope; ledger references the effective decision |
| A use is explicitly selected or replaced | Update designated relationships in the ledger; retain necessary history and the disposition of replaced objects |
| Actual resource references/scenes/configuration are changed and checked | Engineering consumers own actual wiring; Evidence records results for this baseline, Task summarizes, and ledger links their grounds |
| Only a panel, progress, or overview is refreshed | Derive from original sources; create no new acceptance or passing facts |

Save only candidate identities meaningful for use; do not enter every random temporary artifact into the master ledger. Tools may manage complete task membership through inventories. Update original entries for existing objects; moving back and forth between Skills does not create new asset or task identities.

<a id="候选快照与遗留恢复"></a>
### Candidate Snapshots and Legacy Recovery

Candidates needing continued review/comparison must keep their manifests and required members at stable version locations or supported retention sources. Runtime-import copies may be replaced but cannot be the sole overwritable payload shared by multiple historical candidates. Retain materials sufficient to review conclusions according to project storage policy, without requiring all large trial-run files in Git.

After overwrites, migration, or loss, first inspect real files, old reports, and available history. If original bytes can be recovered, preserve original identities and digest relationships; if only historical locations or old observations remain and original payloads are insufficient, record the limitation rather than changing old manifests/digests to launder them into passes. Archive links or migration references can support human navigation; current native tools still reject junctions/symbolic links. Report successful location separately from content-digest revalidation.

Register current content using new stable candidates and manifests while retaining old identities, decisions, and selection relationships. Native `asset.upsert` strictly checks new candidates and added references, preserves old bindings, and returns historical candidate payload diagnostics; unrelated historical mismatches do not block new-version registration. `asset.select` still checks actual members of the candidate being designated, and historical acceptance does not transfer to new versions. Successful registration does not prove old payload recovery, updated designated selection, or engineering integration; then update related uses under current authorization and verify consumers.

<a id="3-技术接受选用与接入分别判断"></a>
## 3. Judge Technical Checks, Acceptance, Selection, and Integration Separately

Technical checks establish which consumer conditions files/packages meet; acceptance states who judged which aspects of which version; designated selection states intended uses; actual integration is proven by engineering and applicable runtime evidence. These facts may develop gradually and are not collapsed into a general state enum.

When project requirements call for human acceptance, actual user decisions govern; scopes authorized for model judgment may be completed as required and attributed truthfully. Acceptance of appearance does not automatically authorize all runtime modifications; existing explicit authorization to “integrate after passing” needs no repeated question.

When previews are needed for review, establish temporary/isolated previews within project-permitted scope and explain their purpose and retention; preview wiring is not formal adoption. Preserve project restrictions on preview actions rather than bypassing them under the name of preview.

After new candidates or conversions appear, judge existing evidence/decision applicability by the scope of change. Acceptance bound to exact old content does not automatically transfer to changed content; explicitly inheritable reference or conversion scopes continue with retained source relationships. One unrelated change does not revoke all historical acceptance.

<a id="4-批量接受反馈与撤回"></a>
## 4. Batch Acceptance, Feedback, and Withdrawal

Before submitting decisions, check current objects, reviewed versions, member scope, and existing decisions, preventing an old page from accepting new content as if just reviewed. Use supported revision/digest checks, concurrency protection, or atomic writeback when provided by existing tools.

Browser-local selections, localStorage, and exported feedback packages prove only that data was saved there. Claim decisions are saved only after supported import/writeback reaches authoritative sources and is read back; without writeback capability, provide an inspectable feedback package and specific next steps rather than fabricating synchronization.

When writeback partially succeeds, explain saved and unsaved items individually; query original records before retrying to avoid duplicates or overwriting others' decisions. Do not assume an unavailable general panel bridge exists.

Rejection concerns the reviewed object and scope and retains reasons usable for revision; replacement decisions retain old records and new references. Withdrawing acceptance/changing designated selection and reverting runtime modifications already performed are different actions, handled separately under actual authorization. Merely reverting the ledger to an old version does not automatically revert engine resources.

<a id="5-实际接入与部分结果"></a>
## 5. Actual Integration and Partial Results

After checking handoff objects and permitted scope, develop completes file placement, import/conversion, references, and event/state wiring required by the consumer, then verifies through actual entry points. Use methods for the project's engine/platform; successful copying or importing alone cannot prove correct display, motion, sound, or gameplay.

Before reusing adoption/generation scripts, check purpose, permitted inputs/versions, and current goals. Scripts preserving historical baselines or explicitly rejecting replay cannot be rerun merely because their name fits; use currently supported local integration methods and retain anti-rollback conditions.

If the same version is allowed for consumers A and B, and A succeeds while B fails: retain effective acceptance scope and record A's actual result and B's failure; B's previous resource is determined by its actual references. If the original goal requires both integrations, the Task retains B's unfinished obligation; do not expand A's evidence into whole-batch success.

Material problems return to assets, consumer wiring/lifecycle problems to develop, and input-contract changes to relevant design. Revisions within an existing Task retain original work identity; only independent follow-up deliveries create separate work under common rules.
