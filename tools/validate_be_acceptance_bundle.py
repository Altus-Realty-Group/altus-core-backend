#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


def parse_kv_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def find_runtime_raw_file(proof_dir: Path) -> Path | None:
    preferred = proof_dir / "runtime_http_raw.txt"
    if preferred.exists():
        return preferred
    candidates = sorted(proof_dir.glob("*_http_raw.txt"))
    return candidates[0] if candidates else None


def extract_live_sha(raw_http_text: str) -> str:
    match = re.search(r"^x-altus-build-sha:\s*([^\s]+)", raw_http_text, flags=re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate deterministic BE acceptance bundle completeness and integrity")
    parser.add_argument("--proof-dir", required=True)
    parser.add_argument("--reviewed-sha", required=True)
    parser.add_argument("--runtime-affecting", action="store_true")
    parser.add_argument("--require-persistence", action="store_true")
    args = parser.parse_args()

    proof_dir = Path(args.proof_dir)
    reviewed_sha = args.reviewed_sha.strip()

    print(f"CHECK_PROOF_DIR={proof_dir}")
    print(f"CHECK_REVIEWED_SHA={reviewed_sha}")

    required_files = [
        "README.md",
        "proof_manifest.json",
        "route_and_commit.txt",
        "git_scope.txt",
        "telemetry_evidence.txt",
        "validation.txt",
    ]

    missing: list[str] = []
    for name in required_files:
        if not (proof_dir / name).exists():
            missing.append(name)

    if args.require_persistence and not (proof_dir / "persistence_evidence.txt").exists():
        missing.append("persistence_evidence.txt")

    runtime_raw = find_runtime_raw_file(proof_dir)
    if args.runtime_affecting and runtime_raw is None:
        missing.append("runtime_http_raw.txt|*_http_raw.txt")

    manifest_json = proof_dir / "proof_manifest.json"
    route_commit_txt = proof_dir / "route_and_commit.txt"

    live_sha = ""
    route_data = parse_kv_file(route_commit_txt)
    if "live_build_sha" in route_data and route_data["live_build_sha"]:
        live_sha = route_data["live_build_sha"]

    if runtime_raw is not None:
        live_sha = live_sha or extract_live_sha(runtime_raw.read_text(encoding="utf-8", errors="ignore"))

    manifest_data: dict[str, str] = {}
    if manifest_json.exists():
        try:
            raw = json.loads(manifest_json.read_text(encoding="utf-8"))
            manifest_data = {str(k): str(v) for k, v in raw.items()}
        except Exception:
            missing.append("proof_manifest.json(valid-json)")

    manifest_reviewed = manifest_data.get("reviewed_commit_sha", "")
    if manifest_reviewed and manifest_reviewed != reviewed_sha:
        print(f"CHECK_FAIL_MANIFEST_REVIEWED_SHA_MISMATCH=manifest:{manifest_reviewed} reviewed:{reviewed_sha}")
        return 1

    if not live_sha:
        print("CHECK_FAIL_LIVE_BUILD_SHA_MISSING=missing x-altus-build-sha in route_and_commit/runtime raw")
        return 1

    if live_sha != reviewed_sha:
        print(f"CHECK_FAIL_SHA_MISMATCH=reviewed:{reviewed_sha} live:{live_sha}")
        return 1

    if missing:
        print("CHECK_FAIL_MISSING_FILES=" + ",".join(missing))
        return 1

    print(f"CHECK_RUNTIME_RAW_FILE={runtime_raw.name if runtime_raw else ''}")
    print(f"CHECK_LIVE_SHA={live_sha}")
    print("CHECK_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
