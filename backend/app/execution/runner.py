from abc import ABC, abstractmethod

from backend.app.execution.models import ExecutionRequest, ExecutionResult


class SandboxRunner(ABC):

    @abstractmethod
    def run(self, request: ExecutionRequest) -> ExecutionResult:
        pass
