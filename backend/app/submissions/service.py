from backend.app.execution.judge import Judge
from backend.app.problems.service import ProblemService
from backend.app.submissions.models import SubmissionRequest, SubmissionResponse


class SubmissionService:

    def __init__(self, problem_service=None, judge=None):
        self.problem_service = problem_service or ProblemService()
        self.judge = judge or Judge()

    def submit(self, request: SubmissionRequest) -> SubmissionResponse:
        problem = self.problem_service.get_problem(request.problem_id)

        result = self.judge.judge_problem(
            source_code=request.source_code,
            problem=problem,
        )

        return SubmissionResponse(
            status=result.status,
            tests_passed=result.tests_passed,
            total_tests=result.total_tests,
        )
