#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from pathlib import Path


PROTECTED_ACCEPTED_ROUTES: list[tuple[str, str]] = [
    ("POST", "/api/assets/ingest"),
    ("POST", "/api/assets/match"),
    ("POST", "/api/assets/resolve"),
    ("POST", "/api/assets/bulk-resolve"),
    ("POST", "/api/assets/upsert"),
    ("POST", "/api/assets/link"),
    ("POST", "/api/assets/{asset_id}/archive"),
    ("POST", "/api/assets/{asset_id}/restore"),
    ("DELETE", "/api/assets/link"),
    ("DELETE", "/api/assets/{asset_id}"),
    ("GET", "/api/assets"),
    ("GET", "/api/assets/overview"),
    ("GET", "/api/assets/metrics"),
    ("GET", "/api/assets/export"),
    ("GET", "/api/assets/{id}"),
    ("GET", "/api/assets/{id}/raw"),
    ("GET", "/api/assets/{id}/timeline"),
    ("GET", "/api/assets/{id}/snapshot"),
    ("GET", "/api/assets/{id}/audit"),
    ("GET", "/api/assets/search"),
]


def load_text_from_git(ref: str, rel_path: str) -> str:
    cmd = ["git", "show", f"{ref}:{rel_path}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to read {rel_path} at {ref}")
    return result.stdout


def parse_route_rows(markdown_text: str) -> dict[tuple[str, str], dict[str, str]]:
    rows: dict[tuple[str, str], dict[str, str]] = {}
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 5:
            continue
        method, endpoint, handler, _runtime, notes = cells[:5]
        method = method.replace("`", "").strip()
        endpoint = endpoint.replace("`", "").strip()
        handler = handler.replace("`", "").strip()
        notes = notes.replace("`", "").strip()
        if method in {"Method", "---"}:
            continue
        key = (method, endpoint)
        rows[key] = {"handler": handler, "notes": notes}
    return rows


def is_accepted(row: dict[str, str]) -> bool:
    return "accepted live route" in row.get("notes", "").lower()


def is_downgraded(row: dict[str, str]) -> bool:
    handler = row.get("handler", "").lower()
    notes = row.get("notes", "").lower()
    bad_markers = ["reserved", "n/a", "non-exposed", "deprecated"]
    return any(marker in handler or marker in notes for marker in bad_markers)


def main() -> int:
    parser = argparse.ArgumentParser(description="Guard against silent accepted-route downgrades in ROUTE_MAP_V1")
    parser.add_argument("--route-map", default="docs/architecture/ROUTE_MAP_V1.md")
    parser.add_argument("--base-ref", default="origin/feature/core-asset-ingest-01")
    parser.add_argument("--base-file", default="")
    parser.add_argument("--head-file", default="")
    args = parser.parse_args()

    route_map_path = Path(args.route_map)

    if args.base_file:
        base_text = Path(args.base_file).read_text(encoding="utf-8")
    else:
        merge_base = subprocess.check_output(["git", "merge-base", "HEAD", args.base_ref], text=True).strip()
        print(f"CHECK_MERGE_BASE={merge_base}")
        base_text = load_text_from_git(merge_base, args.route_map)

    head_text = Path(args.head_file).read_text(encoding="utf-8") if args.head_file else route_map_path.read_text(encoding="utf-8")

    base_rows = parse_route_rows(base_text)
    head_rows = parse_route_rows(head_text)

    accepted_base = {k: v for k, v in base_rows.items() if is_accepted(v)}
    violations: list[str] = []

    for key in sorted(accepted_base.keys()):
        method, endpoint = key
        head_row = head_rows.get(key)
        if head_row is None:
            violations.append(f"MISSING_ACCEPTED_ROUTE={method} {endpoint}")
            continue
        if is_downgraded(head_row):
            violations.append(f"DOWNGRADED_ACCEPTED_ROUTE={method} {endpoint} -> handler:{head_row['handler']} notes:{head_row['notes']}")

    for method, endpoint in PROTECTED_ACCEPTED_ROUTES:
        protected_key = (method, endpoint)
        head_row = head_rows.get(protected_key)
        if head_row is None:
            violations.append(f"MISSING_PROTECTED_ROUTE={method} {endpoint}")
            continue
        if is_downgraded(head_row):
            violations.append(f"DOWNGRADED_PROTECTED_ROUTE={method} {endpoint} -> handler:{head_row['handler']} notes:{head_row['notes']}")

    if violations:
        for item in violations:
            print(item)
        print("CHECK_RESULT=FAIL")
        return 1

    print(f"CHECK_ACCEPTED_ROUTE_COUNT={len(accepted_base)}")
    print(f"CHECK_PROTECTED_ROUTE_COUNT={len(PROTECTED_ACCEPTED_ROUTES)}")
    print("CHECK_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
