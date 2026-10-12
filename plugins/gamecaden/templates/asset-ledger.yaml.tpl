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
# Add the corresponding purpose/runtime_id/consumer/candidate_id and decision/evidence references only when that use has actually been selected.
# actual_manifest_sha256 binds only the raw manifest bytes; content checks still verify each digest in files.
