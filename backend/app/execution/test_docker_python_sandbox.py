from backend.app.execution.docker_python_sandbox import DockerPythonSandbox
from backend.app.execution.models import ExecutionRequest


def test_python_code_executes_successfully():
    sandbox = DockerPythonSandbox()

    request = ExecutionRequest(
        language="python",
        source_code='print("Hello from sandbox")',
    )

    result = sandbox.run(request)

    assert result.status == "COMPLETED"
    assert result.stdout.strip() == "Hello from sandbox"
    assert result.exit_code == 0


def test_python_code_times_out():
    sandbox = DockerPythonSandbox()

    request = ExecutionRequest(
        language="python",
        source_code="while True:\n    pass",
        timeout_seconds=2,
    )

    result = sandbox.run(request)

    assert result.status == "TIME_LIMIT_EXCEEDED"


def test_python_runtime_error():
    sandbox = DockerPythonSandbox()

    request = ExecutionRequest(
        language="python",
        source_code="print(1 / 0)",
    )

    result = sandbox.run(request)

    assert result.status == "RUNTIME_ERROR"
    assert result.exit_code != 0
    assert "ZeroDivisionError" in result.stderr


def test_python_code_exceeds_memory_limit():
    sandbox = DockerPythonSandbox()

    request = ExecutionRequest(
        language="python",
        source_code="data = b'x' * (1024 * 1024 * 512)",
        memory_mb=256,
    )

    result = sandbox.run(request)

    assert result.status == "MEMORY_LIMIT_EXCEEDED"
    assert result.exit_code == 137

def test_python_code_has_no_network_access():
    sandbox = DockerPythonSandbox()

    request = ExecutionRequest(
        language="python",
        source_code="""
import urllib.request

urllib.request.urlopen("https://example.com", timeout=2)
""",
        timeout_seconds=5,
    )

    result = sandbox.run(request)

    assert result.status in ["RUNTIME_ERROR", "TIME_LIMIT_EXCEEDED"]

def test_python_code_cannot_write_to_workspace():
    sandbox = DockerPythonSandbox()

    request = ExecutionRequest(
        language="python",
        source_code="""
with open("/workspace/hacked.txt", "w") as file:
    file.write("hacked")
""",
    )

    result = sandbox.run(request)

    assert result.status == "RUNTIME_ERROR"
    assert "Read-only file system" in result.stderr

def test_python_code_receives_stdin():
    sandbox = DockerPythonSandbox()

    request = ExecutionRequest(
        language="python",
        source_code="""
name = input()
print(f"Hello, {name}")
""",
        stdin="Tejal\n",
    )

    result = sandbox.run(request)

    assert result.status == "COMPLETED"
    assert result.stdout.strip() == "Hello, Tejal"
