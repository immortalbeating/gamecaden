---
id: "{{evidence_id}}"
title: "{{title}}"
observed_at: null
actor: null
subjects:
  - ref: {id: "{{subject_id}}"}
    scope: "{{checked_scope}}"
result: "{{actual_result}}"
coverage: []
# Add subject.version, report_refs, and corrects as actually needed; leave unknown information unknown.
---

# {{title}}

<a id="方法与环境"></a>
## Method and environment
{{actual_method_environment_and_baseline}}

<a id="观察与结论"></a>
## Observations and conclusions
{{observations_and_support_for_result}}

<a id="覆盖限制与来源"></a>
## Coverage, limitations, and sources
{{coverage_limits_and_raw_report_refs}}
