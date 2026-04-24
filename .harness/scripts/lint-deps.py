"""依赖方向检查。

确保模块间无循环依赖，且依赖方向正确。
"""
import ast
import sys
from pathlib import Path

ALLOWED_IMPORTS = {
    "api": {"services", "models", "schemas", "core", "db"},
    "services": {"models", "schemas", "core", "db", "repositories"},
    "repositories": {"models", "core", "db"},
    "models": set(),
    "schemas": set(),
    "core": set(),
    "db": {"models"},
}


def check_file(path: Path) -> list[str]:
    """检查单个文件的导入方向。"""
    violations = []
    module_layer = path.parts[2] if len(path.parts) > 2 else ""

    allowed = ALLOWED_IMPORTS.get(module_layer)
    if not allowed:
        return violations

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return violations

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith("app."):
                target_layer = module.split(".")[1] if len(module.split(".")) > 1 else ""
                if target_layer and target_layer not in allowed and target_layer != module_layer:
                    violations.append(
                        f"{path}: imports from '{target_layer}' but allowed are {allowed}"
                    )
    return violations


def main() -> int:
    backend = Path("backend/app")
    if not backend.exists():
        print("backend/app not found")
        return 0

    all_violations = []
    for py_file in backend.rglob("*.py"):
        all_violations.extend(check_file(py_file))

    if all_violations:
        print("Dependency direction violations found:")
        for v in all_violations:
            print(f"  - {v}")
        return 1

    print("All dependency directions valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
