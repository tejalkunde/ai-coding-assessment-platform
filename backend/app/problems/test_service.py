import pytest

from backend.app.problems.models import Problem, ProblemTestCase
from backend.app.problems.service import ProblemService


@pytest.fixture
def service():
    return ProblemService()


@pytest.fixture
def sample_problem():
    return Problem(
        problem_id="sum-two-numbers",
        title="Sum of Two Numbers",
        description="Read two integers and print their sum.",
        difficulty="EASY",
        supported_languages=["python"],
    )


def test_create_and_get_problem(service, sample_problem):
    created = service.create_problem(sample_problem)

    assert created.problem_id == "sum-two-numbers"
    assert service.get_problem("sum-two-numbers") is created


def test_list_problems(service, sample_problem):
    service.create_problem(sample_problem)

    problems = service.list_problems()

    assert len(problems) == 1
    assert problems[0].title == "Sum of Two Numbers"


def test_duplicate_problem_is_rejected(service, sample_problem):
    service.create_problem(sample_problem)

    with pytest.raises(ValueError, match="Problem already exists"):
        service.create_problem(sample_problem)


def test_missing_problem_raises_error(service):
    with pytest.raises(KeyError, match="Problem not found"):
        service.get_problem("missing-problem")


def test_add_test_case(service, sample_problem):
    service.create_problem(sample_problem)

    test_case = ProblemTestCase(
        input_data="2 3",
        expected_output="5",
    )

    updated = service.add_test_case("sum-two-numbers", test_case)

    assert len(updated.test_cases) == 1
    assert updated.test_cases[0].expected_output == "5"
