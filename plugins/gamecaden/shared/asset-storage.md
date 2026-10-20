# Asset storage and retention

Use this when establishing storage for formal asset production, arranging repeated generation/capture/build batches, or changing uses and retained payloads. Existing project rules, actual consumers, original commitments, and current authorization determine the scope. Small repairs with sufficient existing arrangements reuse them directly.

## Establish the current arrangement

Locate the current sources, candidates, runtime outputs, evidence, temporary work, and recovery dependencies. Reuse their existing inventories and maintenance locations. When arrangements are missing, save the choices needed for this batch in the original Task; reusable project rules belong in existing Git/development rules or the relevant Spec. A short table can suffice; this introduces no mandatory storage document, asset grade, or per-file form.

The arrangement identifies storage/versioning destinations, which real bytes must remain available, rebuild or restore methods, applicable resource constraints, and the next review point. Asset uses come from the [original ledger and consumers](asset-handoff.md), not a second asset database. Production-only masters, editable sources, and failure reproductions may remain necessary even when the game never loads them.

## Versioning, storage, and recovery

For a Git project entering formal binary-asset production without an adequate existing binary policy, default to **Git plus Git LFS** for versioned creative sources and substantial binary payloads. Preserve an applicable existing Git policy or alternative version system, such as Perforce. Concept discussion and work without Git do not require repository creation. Tool selection follows current setup/implementation scope; [Git action permissions](git-policy.md) still govern staging, commits, history changes, and remote delivery.

| Material | Default arrangement, adapted to actual consumers |
|---|---|
| Code, text configuration, manifests, ledgers, and decision/evidence indexes | Ordinary Git when the project versions these materials; reference existing inventories directly |
| Versioned binary creative sources and required deliverables | Project-scoped LFS path/type rules, or the established equivalent; keep required current bytes accessible to production and runtime readers |
| Temporary probes, decoded intermediates, diagnostic captures, caches, and duplicate builds | Separate local working outputs with explicit retention; exclude from Git and engine import when consumers permit |
| Historical payloads still needed for comparison, reuse, rollback, or reproduction | Stable online versions or a documented archive with a tested restoration path; protect unique source and hand-edited work |
| Independent backups | A separate recoverable destination and its own retention policy; snapshots/backup tools supplement versioning and working-output management |

Check actual attributes/ignore behavior on representative intended and excluded paths. For LFS, verify real pointer OID/size, required local objects, and agreement with the asset bytes/digests; installing the CLI or writing `.gitattributes` alone is insufficient. Keep a known restore route before treating another copy as dispensable. A pointer alone does not prove payload availability, and local-only LFS objects may be the only confirmed copy. Existing Git history, remote availability, and LFS-cache reclamation are separate matters; forward configuration is not a historical migration.

Git ignore, engine import exclusions, and physical retention have different effects. Ignore rules leave existing files and tracked history in place. Catalogue/preview interfaces are optional; retain a single authoritative ledger and version system. Configure the chosen tool under existing authorization rather than introducing a paid service, history migration, or second asset catalogue as an implicit dependency.

## Bound a batch without capping the goal

Track three different quantities:

- **Deliverables:** required identities/uses and versions from the current scope, accounting for valid reuse. Failed attempts do not complete these obligations.
- **Attempts and returned outputs:** actual jobs, retries, and files. A call may return several candidates or no file; failures are recorded by their real outcomes.
- **Resources:** retained file bytes, temporary/copy/archive costs, and confirmed charges. Failed or unselected files occupy storage while retained; a failed job is not assumed free.

Estimate the next batch from existing same-route samples: planned output count times observed file size, plus necessary processing, captures, copies, and restoration costs. State uncertainty rather than inventing a success rate or universal retry allowance. Without measurements, produce a small batch of currently needed work and update the estimate from its results. Use real project constraints; an estimate is not a new approval gate or a fixed allowance for the complete asset goal.

Give repeated capture, extraction, and build jobs finite output/termination conditions tied to their question and required coverage. Use the producer's supported count/byte/duration controls; add a missing bound in the responsible producer when that implementation is in scope. Record what was actually enforced. The workflow itself is not a disk monitor or generation quota service. Check batch totals at meaningful boundaries rather than repeatedly scanning the entire repository per image.

Reuse unchanged immutable dependencies by version/digest. Freeze a needed dependency version once and reference it across runs; a distinct reproduction may retain its own justified snapshot. Avoid new full payload copies merely to refresh a report. Protect immutable bytes from writes through shared links, and retain the native reader's path/link restrictions.

When requirements or production routes change, update the original plan and rolling estimate. Ordinary fixes, retries, and batch-size changes continue within existing scope. If an explicit storage/cost constraint will be exceeded, pause only the affected job to resolve that resource issue; continue independent authorized work and retain the complete delivery obligation. Report limited capture coverage honestly instead of silently truncating a required result into a pass.

## Review retention at actual boundaries

| Moment | Appropriate action |
|---|---|
| Before and during production | Choose storage once, reuse valid versions, avoid duplicate payloads, and remove consumed rebuildable intermediates only under the existing retention scope |
| A production/review batch reaches a clear conclusion | Reconcile current uses, pending comparisons, source/reproduction needs, and the batch's retained outputs |
| A consumer/version is replaced, review ends, or a reproduction is resolved | Reassess the affected historical materials and their recovery dependencies, without a repository-wide sweep |

Candidate registration or selection for one use **does not retire other candidates**. Pending comparison, acceptance, revision, and other uses can still depend on their bytes. A rejected attempt may contain useful source, hand work, or failure evidence; status or absence from runtime alone is not a deletion criterion.

| Retained purpose | Treatment |
|---|---|
| Current consumers, required production sources, or pending review | Keep the actual necessary members accessible; a log or thumbnail cannot replace promised review/reproduction coverage |
| Historical comparison, reuse, rollback, or failure reproduction | Keep the needed version online or archive its bytes with digest/location and an actual restore method |
| Unreferenced duplicates or consumed, demonstrably rebuildable intermediates | Deduplicate or reclaim within the adopted scope, protecting the retained source and its readers |
| Explicitly discarded payloads with no remaining consumption, review, reuse, or required reproduction purpose | Retire under the adopted policy; retain sufficient identity, reason, conclusions, and representative grounds |

For an actual move/deletion, check current references and undeclared recovery/backup dependencies as well as Git tracking. Bind the affected paths/versions and reasons in the existing batch record or tool inventory; a batch can share one rationale. Preserve unknown-purpose and unique required inputs until their disposition is resolved. Existing authorization may cover routine cleanup; selecting a candidate or closing a Task does not grant additional destructive scope.

Distinguish **online**, **archived and recoverable**, and **retired without guaranteed recovery** in the original retention explanation; these are payload availability facts, not new asset acceptance states or mandatory schema fields. Keep original reports, identities, and digests honest. If full historical media are retired, disclose the lost replay/closure coverage rather than claiming that an existing report preserves all pixels.

Native candidate bindings remain unchanged. Archive references aid navigation but are not an automatic native restore operation: restore needed original bytes at the supported binding, then revalidate. Historical unavailable-payload diagnostics do not become passes; current selection and actual integration still require their own files and checks under [asset handoff](asset-handoff.md#candidate-snapshots-and-legacy-recovery).

## Measure the scope honestly

Report the measured roots, time/baseline, skipped links, and whether Git/LFS, other worktrees, and external archives are included. Separate path-size totals, unique file content where hard links exist, archive/recovery costs, and observed volume-space changes. Moving bytes to another directory on the same disk does not free that disk; removing a branch or working copy does not imply equivalent object reclamation. Estimates, planned removals, and actual reclaimed bytes retain separate conclusions.
