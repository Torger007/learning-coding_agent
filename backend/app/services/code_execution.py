"""Code execution with Docker sandbox and dangerous code detection."""

import ast
import asyncio
import re
import tempfile
from pathlib import Path

from app.config import settings
from app.core.exceptions import SandboxError, ValidationError

DANGEROUS_MODULES = {
    "os",
    "subprocess",
    "sys",
    "shutil",
    "socket",
    "urllib",
    "pickle",
    "ctypes",
    "multiprocessing",
    "threading",
}

DANGEROUS_FUNCTIONS = {"eval", "exec", "compile", "__import__", "open", "input"}

DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"dd\s+if=.*of=/dev/",
    r"mkfs",
    r"while\s+True\s*:\s*pass",
    r"import\s+os",
    r"from\s+os\s+import",
    r"import\s+subprocess",
    r"from\s+subprocess\s+import",
    r"import\s+sys",
    r"from\s+sys\s+import",
    r"__import__",
]


class DangerousCodeDetector:
    """Static scanner for dangerous Python code patterns."""

    @staticmethod
    def scan(code: str) -> list[str]:
        """Scan code and return list of detected dangers."""
        violations: list[str] = []

        try:
            tree = ast.parse(code)
        except SyntaxError:
            tree = None

        if tree:
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split(".", maxsplit=1)[0]
                        if module_name in DANGEROUS_MODULES:
                            violations.append(f"Dangerous module import: {module_name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    module_name = node.module.split(".", maxsplit=1)[0]
                    if module_name in DANGEROUS_MODULES:
                        violations.append(f"Dangerous module import: {module_name}")
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in DANGEROUS_FUNCTIONS:
                        violations.append(f"Dangerous function call: {node.func.id}()")

        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                violations.append(f"Dangerous pattern detected: {pattern}")

        for func in DANGEROUS_FUNCTIONS:
            if re.search(rf"\b{func}\s*\(", code) and not any(
                f"Dangerous function call: {func}()" == violation for violation in violations
            ):
                violations.append(f"Dangerous function call: {func}()")

        return violations


class CodeExecutionService:
    """Execute Python code in a Docker sandbox."""

    def __init__(self) -> None:
        self.detector = DangerousCodeDetector()
        self.timeout = settings.DOCKER_TIMEOUT
        self.memory_limit = settings.DOCKER_MEMORY_LIMIT
        self.cpu_limit = settings.DOCKER_CPU_LIMIT

    async def execute(self, code: str) -> dict:
        """Execute code safely and return result."""
        violations = self.detector.scan(code)
        if violations:
            raise ValidationError(
                f"Code contains dangerous patterns: {'; '.join(violations)}"
            )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            docker_available = await self._docker_available()
            if not docker_available:
                raise SandboxError("Docker is required for sandboxed code execution")
            return await self._execute_docker(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    async def _docker_available(self) -> bool:
        """Check if Docker is available."""
        try:
            import subprocess as sp
            result = sp.run(
                ["docker", "version"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    async def _execute_docker(self, tmp_path: str) -> dict:
        """Execute code in Docker sandbox."""
        cmd = [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
            "--read-only",
            "--security-opt",
            "no-new-privileges:true",
            "--memory",
            self.memory_limit,
            "--cpus",
            str(self.cpu_limit),
            "--pids-limit",
            "64",
            "--tmpfs",
            "/tmp:noexec,nosuid,size=100m",
            "-v",
            f"{tmp_path}:/usr/local/lib/learning-coding-agent-script.py:ro",
            "python:3.12-slim",
            "python",
            "/usr/local/lib/learning-coding-agent-script.py",
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=self.timeout
            )
        except asyncio.TimeoutError:
            proc.kill()
            raise SandboxError(f"Code execution timed out after {self.timeout}s")

        output = stdout.decode("utf-8", errors="replace").strip()
        error = stderr.decode("utf-8", errors="replace").strip()

        if proc.returncode != 0:
            return {
                "success": False,
                "output": output,
                "error": error or "Execution failed with non-zero exit code",
            }

        return {
            "success": True,
            "output": output,
            "error": None,
        }

code_execution_service = CodeExecutionService()
