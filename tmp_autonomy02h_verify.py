from pathlib import Path
t = Path("docs/governance/AUTONOMY_WORKER_BRIDGE_V1.md").read_text(encoding="utf-8")
checks = [
    "### target_files",
    ".github/workflows/worker_bridge.yml",
    ".github/workflows/task_status_reconcile.yml",
    "docs/governance/AUTONOMY_WORKER_BRIDGE_V1.md",
    "proof_artifacts: docs/proofpacks/2026-03-06_be-core_autonomy-02/AUTONOMY02A_CORRECTION_RAW.txt",
]
for c in checks:
    print(c, "=>", c in t)
print("BAD_target_files_literal =>", "target_files: worker_bridge.yml" in t)
print("BAD_proof_literal =>", "proof_artifacts: AUTONOMY02A_CORRECTION_RAW.txt" in t)
