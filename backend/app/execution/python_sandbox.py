from backend.app.execution.models import ExecutionRequest, ExecutionResult
from backend.app.execution.runner import SandboxRunner


class PythonSandbox(SandboxRunner):

    def run(self, request: ExecutionRequest) -> ExecutionResult:
        return ExecutionResult(
            status="NOT_IMPLEMENTED",
            stderr="Python sandbox execution is not implemented yet."
        )
