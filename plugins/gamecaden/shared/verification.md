<a id="验证范围证据适用性与结论"></a>
# Verification Scope, Evidence Applicability, and Conclusions

Development checks in develop/assets, verification in verify, and closure judgments in close share this convention. See [common records](records.md) for Evidence storage and sole responsibility; this page introduces neither a second task lifecycle nor mandatory reports.

See the [format contract](formats-v1.md) for the concrete form of new native Evidence/Decision; continue directly referencing existing complete reports. Schema validation only establishes valid record shape and cannot replace the evidence-applicability judgments required here.

<a id="1-先确定正在证明什么"></a>
## 1. First Establish What Is Being Proven

Read the outcomes, objects, conditions, and scope to assess from the user request, current effective Task/Epic commitments, and related Spec. A local check may answer only a local question; a claim that the whole delivery holds must cover all its necessary conditions. Implementer summaries, test lists, and derived progress are leads and cannot replace original requirements.

Ordinary quick fixes may connect requirements and checks in a brief explanation; for multiple systems, consumers, or acceptance conditions, map them in a table in the original Task or an existing report. There is no need to create a document per requirement or artificially add global numbering.

Choose checks around failure modes: some requirements need static data; others need actual execution, natural input, target scale, or user judgment. Choose methods sufficient for this work's impacts; do not expand into an unrelated full audit because a tool is available, or reduce necessary coverage because of a quick label.

The existence of required data/diagrams/frame slots supports only the corresponding material facts. To claim rules are active, visuals are reproduced, or actions are complete, check reading/wiring and corresponding observations along real consumers; after implementation or measurement changes, check whether this round's evidence covers the final baseline. Static checks that fulfill the original commitment remain valid; do not uniformly require all work to run the game for additional verification.

<a id="2-判断已有证据是否仍适用"></a>
## 2. Assess Whether Existing Evidence Still Applies

Check actually relevant conditions:

- Object and scope: whether the implementation, resource version, consumer, scene, platform, or user path matches the current claim.
- Baseline and inputs: which code, data, configuration, tool versions, and environment properties can change this conclusion; with uncommitted changes, HEAD alone does not sufficiently describe the tested implementation.
- Method and result: whether the report was actually executed and covers requirements, and whether raw results, failures, and limitations can be found.
- Provenance and independence: who executed it, when, and where; attribute self-checks, tool checks, independent verification, and user acceptance separately.

Reuse depends on applicability, not mechanical judgments based on report age or file time. Session changes, unrelated document edits, or file changes that do not affect the conclusion require no full revalidation. When runtime environments/build artifacts change, results from the original environment may remain historical support but cannot prove corresponding behavior in the new environment.

When a change affects one part, recheck that part and actual related surfaces, retaining other still-valid results. Partial results from different versions prove only their own objects; without version consistency or combination checks, they cannot be assembled into an overall current pass.

When evidence scope is unclear, first inspect original artifacts, commands, and actual conditions. Mark connections that cannot be established as unproven; changing report dates, titles, or result fields does not restore credibility.

<a id="3-如实表达检查结论"></a>
## 3. Report Check Conclusions Truthfully

| Conclusion meaning | Required explanation |
|---|---|
| Passed | Specific requirements, applicable object/baseline, and supporting observations |
| Failed | Observed differences, reproduction conditions, and affected requirements |
| Undetermined/verification blocked | Missing information, environment, or capability, and the claim affected |
| Not executed/not covered | Which part was unchecked and why; plans are not execution results |
| Not applicable | Grounds based on actual goals, platforms, or explicitly defined scope |

These report check facts, not new Task state enums. Express technical passes, user acceptance, adoption decisions, engineering integration, and release separately. Judge overall conclusions against all necessary conditions; passing counts or averages cannot substitute for missing conditions.

Record preexisting failures separately from new regressions in this work. Unrelated old issues need not block local delivery, but if an issue prevents the current commitment from being fulfilled, it remains an obstacle even if longstanding. For example, “This change introduced no startup errors” does not prove that a release package required to start is ready.

<a id="4-自检与独立核验"></a>
## 4. Self-checks and Independent Verification

verify is a responsibility; independent verification is one possible execution arrangement within it. Simple work with sufficient self-check evidence can be judged directly; arrange a suitable independent executor and explain coverage when the user or effective rules require it, or when current risk truly needs a second perspective.

Independent executors should first inspect original requirements, tested objects, and effective evidence, then use implementer explanations as investigation leads. The handoff package includes the actual root, object/baseline, requirement sources, evidence locations, and known limitations, not just an implementer-selected passing list.

Follow host-permitted agent roles and permissions; select a role capable of image inspection for visual issues. Independent verifiers keep the tested implementation unchanged and return locations, observations, impacts, and necessary next steps when issues are found. An implementer checking their own work with a different prompt cannot be recorded as an independent result; when independence is unavailable, state truthfully that the condition is still missing.

New issues must correspond to effective requirements or evidenced relevant risks. Unrelated refactoring preferred by a reviewer cannot become a temporary closure gate; explain the connection to the current goal for a real new risk, then address it within original scope or create follow-up work with clear ownership.

<a id="5-接受范围变化与失败后的动作"></a>
## 5. Acceptance, Scope Changes, and Actions After Failure

Human acceptance is required only when actually agreed for this work. Reusing explicit existing decisions requires checking object, version, use, and aspect; machine PASS or model impressions do not mean the user has accepted. When user judgment is needed, prepare concrete materials and known differences before asking the corresponding question.

Users may explicitly adjust delivery scope, acceptance arrangements, or risk commitments they own. After saving the grounds and old/new relationship, judge against currently effective conditions; unexecuted checks remain unexecuted, and failed observations do not become passes because delivery is allowed. Saying only “wrap up” does not automatically revoke agreed necessary conditions.

When implementation or content problems are found, route repairs to the corresponding responsibility under original authorization, then recheck affected scope. For check-only requests, deliver findings without modifying the tested implementation. Return to corresponding design/change handling if requirements must change. Keep using effective results rather than clearing all evidence after one failure.

Repeatedly rerunning the same failure without new observations or actual repairs is not progress. Distinguish failed test assertions, execution infrastructure faults, and missing decisions; continue safely retryable infrastructure actions covered by existing authorization, while retaining recoverable next steps for real gaps.
