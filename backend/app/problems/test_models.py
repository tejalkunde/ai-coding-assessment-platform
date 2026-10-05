from backend.app.problems.models import Problem, ProblemTestCase


def test_test_case_defaults():
    test_case = ProblemTestCase(
        input_data="2 3",
        expected_output="5",
    )

    assert test_case.is_hidden is False
    assert test_case.time_limit_seconds == 5
    assert test_case.memory_limit_mb == 256


def test_hidden_test_case():
    test_case = ProblemTestCase(
        input_data="100 250",
        expected_output="350",
        is_hidden=True,
    )

    assert test_case.is_hidden is True


def test_problem_contains_test_cases():
    test_cases = [
        ProblemTestCase(
            input_data="2 3",
            expected_output="5",
        ),
        ProblemTestCase(
            input_data="10 20",
            expected_output="30",
            is_hidden=True,
        ),
    ]

    problem = Problem(
        problem_id="sum-two-numbers",
        title="Sum of Two Numbers",
        description="Read two integers and print their sum.",
        difficulty="EASY",
        supported_languages=["python"],
        test_cases=test_cases,
    )

    assert problem.problem_id == "sum-two-numbers"
    assert len(problem.test_cases) == 2
    assert problem.test_cases[1].is_hidden is True

