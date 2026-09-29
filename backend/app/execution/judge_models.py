from dataclasses import dataclass
from typing import Optional


@dataclass
class TestResult:
    passed: bool
    actual_output: Optional[str] = None
    expected_output: Optional[str] = None
    execution_time_ms: Optional[float] = None
    is_hidden: bool = False


@dataclass
class JudgeResult:
    status: str
    tests_passed: int
    total_tests: int
    test_results: list[TestResult]
