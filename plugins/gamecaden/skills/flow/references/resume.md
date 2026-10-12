<a id="再次进入与续接"></a>
# Re-entry and continuation

Read only when continuing, restoring or checking existing work. Restore from original project records; chat history and handoff files supplement context.

<a id="0-怎样进入恢复以及能够保证什么"></a>
## 0. How restoration starts and what it can guarantee

After a request starts in the correct project, the host loads effective project guidance; installed Skills may match their descriptions or be explicitly selected by the user. Project guidance should state that development/continuation requests enter flow first; this is a verifiable reading path, not a runner that forces automatic execution.

Users usually need only say “continue the previous work” or “continue T-012”, without retelling the whole project. Ask further only when the project is unbound, work cannot be located or a substantive choice exists. When a Skill is not installed, guidance is not effectively loaded or records are not saved, do not promise that this automatic reading path is available.

A blank session alone does not start implementation. For progress queries, restore enough context to answer; advance according to effective tasks and scope only when continuation is requested. For explicit fallback, users can select an actually installed flow Skill or provide a project/Task path; do not cite an uninstalled command as if it were an automatic capability.

Save task records promptly at important results, scope changes, deferral/cancellation and handoff. After abrupt interruption, only persisted content and facts verifiable from the current situation can be reliably restored; automatic recovery of unsaved conversation, temporary state or decisions cannot be guaranteed. Check persistent records, effective entrypoints and new-session restoration verification separately.

Quick work can be briefly recorded after completion, but when waiting, session switching or interruptible sustained actions are expected, first leave sufficient active/continuation records. If an unexpected interruption occurs before the first saved record, reconstruct known circumstances only from actual changes and accessible sources; do not pretend complete task records already exist.

<a id="1-定位哪项工作"></a>
## 1. Locate the work

Priority: explicit Task/Issue/path in this turn → clear context for current unfinished work → match the request's goal to relevant active work. Progress can navigate; return to original records ultimately.

With multiple candidates, compare goals, scope, runtime roots and original management sources, rather than selecting by last-modified date. Offer concise choices only when substantive ambiguity remains, listing actual work identifiers and differences.

Also read the original Task's current advancement constraints: explicitly deferred or cancelled work cannot execute automatically merely because it remains in a list. Select directly when existing priorities, dependencies and current intent suffice; multiple candidates alone do not necessarily require a question. Explicit resumption of a Task can lift that user deferral; other necessary conditions continue to apply.

The current request may only query status or may change original scope. A status question during active execution does not automatically revoke the original implementation request; an independent read-only status request does not automatically authorize subsequent implementation.

<a id="2-核对当前现场"></a>
## 2. Check the current situation

Resolve actual project roots, runtime roots and relevant paths through workspace mappings. Check current code, resources, worktree/branch and uncommitted differences related to this task.

When restoring or switching worktrees, compare currently effective guidance/entrypoints, shell working directory and local I/O project_root so they refer to the explicit target checkout. Worktree attachment alone cannot prove the default command directory has changed; specify working directory and project root explicitly as needed. Repair an invalid entrypoint according to its specific gap, without repeating full-project init.

- The same project in different worktrees may have different candidates and rules; use the explicitly targeted one and retain its scope identifiers.
- Old processes, ports, bridge files and caches do not prove the current runtime target; check the actual connected project before engine operations.
- Preserve unrelated dirty changes. If they overlap current changes and intent cannot be determined, clarify the specific conflict; do not clean the entire workspace.
- When a link points to a project outside current authorization, check its purpose first; source mappings do not expand write authorization.

<a id="3-恢复足够上下文"></a>
## 3. Restore sufficient context

Read the Task's current results, unfinished items and next step first, then relevant Epic/Spec/design and evidence/decisions required by the current action. Read history only when differences need explanation; restoration does not justify loading every Task, log and parking lot.

When original work cites [PDP](../../../shared/phased-development.md), read only the current Stage and necessary adjacent prerequisites, continuing under the original Task's Epic ownership. Complete relevant entrypoints when missing sources affect stage/version route arrangements; independent local repairs do not thereby migrate the entire project.

To understand game direction, effective rules or outcome arrangements, find the corresponding current primary documents through index, then follow specific references to detailed materials. Old mappings can still support local continuation; organize primary documents during formal adoption or explicitly requested related repair. Missing new primary documents does not automatically expand this task.

Distinguish “done”, “verified”, “accepted” and “actually integrated”. Check the object, version, use and baseline corresponding to records; a report generation date or old PASS alone does not prove current applicability.

<a id="4-根据差异继续"></a>
## 4. Continue according to differences

| Situation | Next action |
|---|---|
| Goals, objects and prerequisites are unchanged; original evidence still applies | Reuse and continue the next action |
| Only some inputs changed | Supplement affected checks or decisions; retain unrelated valid results |
| Original Task remains active with only an ordinary small repair | Continue in the original Task |
| Original work was truly complete then; new requirements/regressions arose later | Use existing work responsible for the new change or a new Task; retain historical closure |
| Investigation establishes that commitments were unmet at original closure | Explain the mistaken judgment within the same work and reopen as needed; retain the old closure event |
| User explicitly changes goals, defers or abandons work | Update scope and advancement constraints under the change-handling reference; save affected work's destination |
| Necessary acceptance is missing | Explain the specific object and gap; continue work independent of that acceptance |
| Source records are missing | Check existing pointers/history; retain unknowns when unverifiable, without fabricating completion status |

When an old process still owns the work, advance using its actual records and closure rules. A new workflow entrypoint does not transfer management authority.

When additions, modifications, deferral or cancellation actually occur, read [Change handling](change-work.md); ordinary restoration does not need all change details.

<a id="5-输出与持久化"></a>
## 5. Output and persistence

Use one current context during execution: actual roots, work source/identifier, current goal, next action, applicable evidence and unresolved points. This is working understanding; it does not require context.json or another HANDOFF.

Write back to the original Task when obtaining new results, encountering a blocker requiring a pause, handing off or closing. When an independent handoff file is genuinely needed, export a snapshot from updated original records under [Derived outputs](../../../shared/derived-outputs.md#standalone-handoff), retaining actual scope/baseline, original grounds and default path. Save repeated generations as separate versions; restoration still advances from original records.
