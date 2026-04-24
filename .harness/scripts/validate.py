"""主验证管道。

运行所有检查并生成报告。
"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"


def run(cmd: list[str], cwd: Path | None = None) -> tuple[bool, str]:
    """运行命令，返回 (是否成功, 输出)。"""
    result = subprocess.run(
        cmd,
        cwd=cwd or PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, result.stdout + result.stderr


def check_backend() -> dict:
    """检查后端代码。"""
    results = {}
    results["ruff"], out = run(["ruff", "check", "."], cwd=BACKEND_DIR)
    results["ruff_output"] = out
    results["mypy"], out = run(["mypy", "src/"], cwd=BACKEND_DIR)
    results["mypy_output"] = out
    results["pytest"], out = run(["pytest", "-q"], cwd=BACKEND_DIR)
    results["pytest_output"] = out
    return results


def check_security() -> dict:
    """安全检查。"""
    results = {}
    # 检查硬编码 API Key
    result = subprocess.run(
        ["grep", "-rE", r"(sk-[a-zA-Z0-9]{20,})", "--include=*.py", "--include=*.ts", "src/", "backend/"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    results["api_key_leak"] = result.returncode != 0  # grep 找到匹配则失败
    results["api_key_output"] = result.stdout if result.stdout else "None found"
    return results


def main() -> int:
    print("=" * 60)
    print("Project Validation Report")
    print("=" * 60)

    # Backend checks
    print("\n[Backend]")
    backend = check_backend()
    print(f"  ruff:   {'PASS' if backend['ruff'] else 'FAIL'}")
    print(f"  mypy:   {'PASS' if backend['mypy'] else 'FAIL'}")
    print(f"  pytest: {'PASS' if backend['pytest'] else 'FAIL'}")

    # Security checks
    print("\n[Security]")
    sec = check_security()
    print(f"  api_key_leak: {'PASS' if sec['api_key_leak'] else 'FAIL'}")

    # Summary
    all_pass = all([
        backend["ruff"], backend["mypy"], backend["pytest"],
        sec["api_key_leak"],
    ])
    print("\n" + "=" * 60)
    print(f"Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")
    print("=" * 60)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
