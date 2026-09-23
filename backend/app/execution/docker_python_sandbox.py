import subprocess
import tempfile
import time
from pathlib import Path

from backend.app.execution.models import ExecutionRequest, ExecutionResult
from backend.app.execution.runner import SandboxRunner


class DockerPythonSandbox(SandboxRunner):

    def run(self, request: ExecutionRequest) -> ExecutionResult:
        start_time = time.perf_counter()

        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            source_file = workspace / "main.py"
            source_file.write_text(request.source_code, encoding="utf-8")

            command = [
                "docker",
                "run",
                "--rm",
                "-i",
                "--network",
                "none",
                "--memory",
                f"{request.memory_mb}m",
                "--cpus",
                "1",
                "--pids-limit",
                "64",
                "--mount",
                f"type=bind,source={workspace},target=/workspace,readonly",
                "python:3.13-alpine",
                "python",
                "/workspace/main.py",
            ]

            try:
                result = subprocess.run(
                    command,
                    input=request.stdin,
                    text=True,
                    capture_output=True,
                    timeout=request.timeout_seconds,
                )

                execution_time_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                if result.returncode == 0:
                    status = "COMPLETED"
                elif result.returncode == 137:
                    status = "MEMORY_LIMIT_EXCEEDED"
                else:
                    status = "RUNTIME_ERROR"

                return ExecutionResult(
                    status=status,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    execution_time_ms=execution_time_ms,
                    exit_code=result.returncode,
                )

            except subprocess.TimeoutExpired as exc:
                execution_time_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                return ExecutionResult(
                    status="TIME_LIMIT_EXCEEDED",
                    stdout=exc.stdout or "",
                    stderr=exc.stderr or "",
                    execution_time_ms=execution_time_ms,
                )
