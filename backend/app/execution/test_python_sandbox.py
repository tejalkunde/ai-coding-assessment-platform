from backend.app.execution.docker_python_sandbox import DockerPythonSandbox
from backend.app.execution.models import ExecutionRequest


sandbox = DockerPythonSandbox()

request = ExecutionRequest(
    language="python",
    source_code='''
print(10 / 0)
''',
    timeout_seconds=5,
)

result = sandbox.run(request)

print("Status:", result.status)
print("Output:", result.stdout)
print("Error:", result.stderr)
print("Time:", result.execution_time_ms, "ms")
print("Exit code:", result.exit_code)
