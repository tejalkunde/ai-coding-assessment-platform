from backend.app.execution.judge import Judge
from backend.app.problems.models import Problem, ProblemTestCase
from backend.app.problems.service import ProblemService
from backend.app.submissions.models import SubmissionRequest
from backend.app.submissions.service import SubmissionService


def create_service():
    problem_service = ProblemService()

    problem = Problem(
        problem_id="two-sum-test",
        title="Echo Input",
        description="Print the input.",
        difficulty="easy",
        supported_languages=["python"],
        test_cases=[
            ProblemTestCase(
                input_data="5\n",
                expected_output="5\n",
            )
        ],
    )

    problem_service.create_problem(problem)

    return SubmissionService(
        problem_service=problem_service,
        judge=Judge(),
    )


def test_submission_accepts_correct_solution():
    service = create_service()

    request = SubmissionRequest(
        problem_id="two-sum-test",
        source_code='print(input())',
        language="python",
    )

    result = service.submit(request)

    assert result.status == "ACCEPTED"
    assert result.tests_passed == 1
    assert result.total_tests == 1


def test_submission_rejects_wrong_solution():
    service = create_service()

    request = SubmissionRequest(
        problem_id="two-sum-test",
        source_code='print("wrong")',
        language="python",
    )

    result = service.submit(request)

    assert result.status == "WRONG_ANSWER"
    assert result.tests_passed == 0
    assert result.total_tests == 1
