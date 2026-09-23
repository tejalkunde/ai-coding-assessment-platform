from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionRequest:
    language: str
    source_code: str
    stdin: str = ""
    timeout_seconds: int = 5
    memory_mb: int = 256


@dataclass
class ExecutionResult:
    status: str
    stdout: str = ""
    stderr: str = ""
    execution_time_ms: Optional[float] = None
    memory_used_mb: Optional[float] = None
    exit_code: Optional[int] = None
