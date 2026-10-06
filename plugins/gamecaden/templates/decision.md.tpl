---
id: "{{decision_id}}"
title: "{{title}}"
events:
  - event_id: "e1"
    decided_at: null
    recorded_at: "{{actual_recorded_at}}"
    actor:
      kind: "{{actual_decider_kind}}"
      id: "{{actual_decider_id}}"
    action: "{{actual_action}}"
    subjects:
      - ref: {id: "{{subject_id}}"}
        scope: "{{subject_scope}}"
    scope: "{{decision_scope}}"
    conclusion: "{{actual_conclusion}}"
---

# {{title}}

## 理由与依据
{{reason_alternatives_and_recoverable_basis}}

## 适用与后续
{{exact_scope_versions_and_followup_owners}}
