from typing import Dict, List

from backend.app.problems.models import Problem, ProblemTestCase


class ProblemService:
    def __init__(self):
        self._problems: Dict[str, Problem] = {}

    def create_problem(self, problem: Problem) -> Problem:
        if problem.problem_id in self._problems:
            raise ValueError(f"Problem already exists: {problem.problem_id}")

        self._problems[problem.problem_id] = problem
        return problem

    def get_problem(self, problem_id: str) -> Problem:
        if problem_id not in self._problems:
            raise KeyError(f"Problem not found: {problem_id}")

        return self._problems[problem_id]

    def list_problems(self) -> List[Problem]:
        return list(self._problems.values())

    def add_test_case(
        self,
        problem_id: str,
        test_case: ProblemTestCase,
    ) -> Problem:
        problem = self.get_problem(problem_id)
        problem.test_cases.append(test_case)
        return problem
