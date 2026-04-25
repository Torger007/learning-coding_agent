"""Tests for code execution and dangerous code detection."""

import pytest

from app.core.exceptions import ValidationError
from app.services.code_execution import DangerousCodeDetector, CodeExecutionService


class TestDangerousCodeDetector:
    """Test suite for DangerousCodeDetector."""

    def test_detects_dangerous_import_os(self):
        """Detector should flag os import."""
        code = "import os\nos.system('ls')"
        violations = DangerousCodeDetector.scan(code)
        assert any("os" in v for v in violations)

    def test_detects_eval(self):
        """Detector should flag eval call."""
        code = "result = eval('1 + 1')"
        violations = DangerousCodeDetector.scan(code)
        assert any("eval" in v for v in violations)

    def test_detects_dangerous_import_socket(self):
        """Detector should flag dangerous imports from the module list."""
        code = "import socket\nprint(socket.gethostname())"
        violations = DangerousCodeDetector.scan(code)
        assert any("socket" in v for v in violations)

    def test_detects_infinite_loop(self):
        """Detector should flag while True pass."""
        code = "while True: pass"
        violations = DangerousCodeDetector.scan(code)
        assert any("while" in v and "pass" in v for v in violations)

    def test_allows_safe_code(self):
        """Detector should allow safe code."""
        code = "print('Hello, World!')\nx = [1, 2, 3]\nprint(sum(x))"
        violations = DangerousCodeDetector.scan(code)
        assert violations == []


class TestCodeExecutionService:
    """Test suite for CodeExecutionService."""

    @pytest.fixture
    def service(self):
        """Create a CodeExecutionService instance."""
        return CodeExecutionService()

    def test_rejects_dangerous_code(self, service):
        """Service should reject code with dangerous patterns."""
        with pytest.raises(ValidationError):
            # Use asyncio.run for async method in sync test context
            import asyncio
            asyncio.run(service.execute("import os\nos.system('rm -rf /')"))

    def test_scanner_called_before_execution(self, service, monkeypatch):
        """Scanner should be invoked before docker execution."""
        scanned = []

        original_scan = DangerousCodeDetector.scan

        def mock_scan(code):
            scanned.append(code)
            return original_scan(code)

        monkeypatch.setattr(DangerousCodeDetector, "scan", staticmethod(mock_scan))

        import asyncio
        with pytest.raises(Exception):
            asyncio.run(service.execute("import os"))

        assert len(scanned) == 1
        assert "import os" in scanned[0]
