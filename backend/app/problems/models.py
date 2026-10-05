from dataclasses import dataclass, field
from typing import List


@dataclass
class ProblemTestCase:
    input_data: str
    expected_output: str
    is_hidden: bool = False
    time_limit_seconds: int = 5
    memory_limit_mb: int = 256


@dataclass
class Problem:
    problem_id: str
    title: str
    description: str
    difficulty: str
    supported_languages: List[str] = field(default_factory=list)
    test_cases: List[ProblemTestCase] = field(default_factory=list)

