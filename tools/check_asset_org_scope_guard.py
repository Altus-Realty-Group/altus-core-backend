#!/usr/bin/env python3
import argparse
import ast
from pathlib import Path


class AssetRouteGuardChecker(ast.NodeVisitor):
    def __init__(self) -> None:
        self.missing_routes: list[str] = []
        self.protected_route_count = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        asset_routes = self._extract_asset_routes(node)
        if not asset_routes:
            return

        self.protected_route_count += len(asset_routes)
        has_guard = self._function_has_org_guard(node)
        if not has_guard:
            for route in asset_routes:
                self.missing_routes.append(route)

    @staticmethod
    def _extract_asset_routes(node: ast.FunctionDef) -> list[str]:
        routes: list[str] = []
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue
            if not isinstance(decorator.func, ast.Attribute):
                continue
            if decorator.func.attr != "route":
                continue

            route_value = ""
            for kw in decorator.keywords:
                if kw.arg == "route" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    route_value = kw.value.value.strip()
                    break

            if not route_value:
                continue
            if not route_value.startswith("assets"):
                continue

            routes.append(f"/api/{route_value}")

        return routes

    @staticmethod
    def _function_has_org_guard(node: ast.FunctionDef) -> bool:
        for child in ast.walk(node):
            if not isinstance(child, ast.Call):
                continue
            if not isinstance(child.func, ast.Name):
                continue
            if child.func.id != "_require_org_id":
                continue
            if len(child.args) == 1 and isinstance(child.args[0], ast.Name) and child.args[0].id == "req":
                return True
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Check all asset routes enforce _require_org_id(req)")
    parser.add_argument("--function-app", default="azure/functions/asset_ingest/function_app.py")
    args = parser.parse_args()

    source_path = Path(args.function_app)
    tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))

    checker = AssetRouteGuardChecker()
    checker.visit(tree)

    if checker.missing_routes:
        print("CHECK_ASSET_ROUTE_GUARDS=FAIL")
        for route in sorted(set(checker.missing_routes)):
            print(f"MISSING_GUARD_ROUTE={route}")
        print("CHECK_RESULT=FAIL")
        return 1

    print("CHECK_ASSET_ROUTE_GUARDS=PASS")
    print(f"CHECK_PROTECTED_ROUTE_COUNT={checker.protected_route_count}")
    print("CHECK_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
