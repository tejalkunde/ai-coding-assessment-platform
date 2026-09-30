from backend.app.execution.judge import Judge
from backend.app.execution.test_case import JudgeTestCase


def test_judge_accepts_correct_solution():
    judge = Judge()

    test_cases = [
        JudgeTestCase(
            input_data="2 3",
            expected_output="5",
        ),
        JudgeTestCase(
            input_data="10 20",
            expected_output="30",
        ),
        JudgeTestCase(
            input_data="100 250",
            expected_output="350",
            is_hidden=True,
        ),
    ]

    source_code = '''
a, b = map(int, input().split())
print(a + b)
'''

    result = judge.judge(
        source_code=source_code,
        test_cases=test_cases,
    )

    assert result.status == "ACCEPTED"
    assert result.tests_passed == 3
    assert result.total_tests == 3


def test_judge_rejects_wrong_answer():
    judge = Judge()

    test_cases = [
        JudgeTestCase(
            input_data="2 3",
            expected_output="5",
        ),
        JudgeTestCase(
            input_data="10 20",
            expected_output="30",
        ),
        JudgeTestCase(
            input_data="100 250",
            expected_output="350",
            is_hidden=True,
        ),
    ]

    source_code = '''
a, b = map(int, input().split())

if a == 100 and b == 250:
    print(999)
else:
    print(a + b)
'''

    result = judge.judge(
        source_code=source_code,
        test_cases=test_cases,
    )

    assert result.status == "WRONG_ANSWER"
    assert result.tests_passed == 2
    assert result.total_tests == 3


def test_hidden_test_output_is_not_exposed():
    judge = Judge()

    test_cases = [
        JudgeTestCase(
            input_data="100 250",
            expected_output="350",
            is_hidden=True,
        ),
    ]

    source_code = '''
print(999)
'''

    result = judge.judge(
        source_code=source_code,
        test_cases=test_cases,
    )

    test_result = result.test_results[0]

    assert test_result.passed is False
    assert test_result.is_hidden is True
    assert test_result.actual_output is None
    assert test_result.expected_output is None
