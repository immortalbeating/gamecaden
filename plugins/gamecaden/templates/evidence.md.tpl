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
# 按实际需要增加 subject.version、report_refs、corrects；未知信息不要补造。
---

# {{title}}

## 方法与环境
{{actual_method_environment_and_baseline}}

## 观察与结论
{{observations_and_support_for_result}}

## 覆盖、限制与来源
{{coverage_limits_and_raw_report_refs}}
