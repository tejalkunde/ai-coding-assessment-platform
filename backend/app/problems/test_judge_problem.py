from backend.app.execution.judge import Judge
from backend.app.problems.models import Problem, ProblemTestCase


def test_judge_problem_accepts_solution():
    problem = Problem(
        problem_id="sum-two-numbers",
        title="Sum of Two Numbers",
        description="Read two integers and print their sum.",
        difficulty="EASY",
        supported_languages=["python"],
        test_cases=[
            ProblemTestCase(
                input_data="2 3",
                expected_output="5",
            ),
            ProblemTestCase(
                input_data="10 20",
                expected_output="30",
                is_hidden=True,
            ),
        ],
    )

    judge = Judge()

    result = judge.judge_problem(
        source_code="""
a, b = map(int, input().split())
print(a + b)
""",
        problem=problem,
    )

    assert result.status == "ACCEPTED"
    assert result.tests_passed == 2
    assert result.total_tests == 2
    assert result.test_results[0].actual_output == "5\n"
    assert result.test_results[1].actual_output is None
    assert result.test_results[1].expected_output is None


def test_judge_problem_rejects_wrong_solution():
    problem = Problem(
        problem_id="sum-two-numbers",
        title="Sum of Two Numbers",
        description="Read two integers and print their sum.",
        difficulty="EASY",
        supported_languages=["python"],
        test_cases=[
            ProblemTestCase(
                input_data="2 3",
                expected_output="5",
            ),
        ],
    )

    judge = Judge()

    result = judge.judge_problem(
        source_code="""
a, b = map(int, input().split())
print(a - b)
""",
        problem=problem,
    )

    assert result.status == "WRONG_ANSWER"
    assert result.tests_passed == 0
    assert result.total_tests == 1
