from backend.app.execution.judge import Judge
from backend.app.execution.test_case import TestCase


judge = Judge()

test_cases = [
    TestCase(
        input_data="2 3",
        expected_output="5",
    ),
    TestCase(
        input_data="10 20",
        expected_output="30",
    ),
    TestCase(
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

print("Status:", result.status)
print("Tests passed:", result.tests_passed)
print("Total tests:", result.total_tests)

for index, test_result in enumerate(result.test_results, start=1):
    print(
        f"Test {index}: "
        f"passed={test_result.passed}, "
        f"actual={test_result.actual_output!r}, "
        f"expected={test_result.expected_output!r}, "
        f"hidden={test_result.is_hidden}"
    )
