schema_version: 1
assets:
  - id: "{{asset_id}}"
    title: "{{title}}"
    purpose: "{{purpose}}"
    candidates:
      - id: "{{candidate_id}}"
        manifest: {path: "{{manifest_path_relative_to_ledger}}"}
        version:
          kind: "sha256"
          value: "{{actual_manifest_sha256}}"
    selected_uses: []
# 只有实际指定选用时才增加对应 purpose/runtime_id/consumer/candidate_id 与决定/证据引用。
# actual_manifest_sha256 只绑定 manifest 的原始字节；内容检查仍逐项核对其 files 摘要。
