from backend.app.execution.docker_python_sandbox import DockerPythonSandbox
from backend.app.execution.judge_models import JudgeResult, TestResult
from backend.app.execution.models import ExecutionRequest
from backend.app.execution.output_comparator import compare_output
from backend.app.execution.test_case import JudgeTestCase
from backend.app.problems.models import Problem


class Judge:

    def __init__(self, sandbox=None):
        self.sandbox = sandbox or DockerPythonSandbox()

    def judge_problem(
        self,
        source_code: str,
        problem: Problem,
    ) -> JudgeResult:

        test_cases = [
            JudgeTestCase(
                input_data=test_case.input_data,
                expected_output=test_case.expected_output,
                is_hidden=test_case.is_hidden,
            )
            for test_case in problem.test_cases
        ]

        return self.judge(
            source_code=source_code,
            test_cases=test_cases,
        )

    def judge(
        self,
        source_code: str,
        test_cases: list[JudgeTestCase],
        timeout_seconds: int = 5,
        memory_mb: int = 256,
    ) -> JudgeResult:

        test_results = []
        tests_passed = 0

        for test_case in test_cases:
            request = ExecutionRequest(
                language="python",
                source_code=source_code,
                stdin=test_case.input_data,
                timeout_seconds=timeout_seconds,
                memory_mb=memory_mb,
            )

            execution_result = self.sandbox.run(request)

            if execution_result.status != "COMPLETED":
                test_results.append(
                    TestResult(
                        passed=False,
                        actual_output=None if test_case.is_hidden else execution_result.stdout,
                        expected_output=None if test_case.is_hidden else test_case.expected_output,
                        execution_time_ms=execution_result.execution_time_ms,
                        is_hidden=test_case.is_hidden,
                    )
                )

                return JudgeResult(
                    status=execution_result.status,
                    tests_passed=tests_passed,
                    total_tests=len(test_cases),
                    test_results=test_results,
                )

            passed = compare_output(
                execution_result.stdout,
                test_case.expected_output,
            )

            if passed:
                tests_passed += 1

            test_results.append(
                TestResult(
                    passed=passed,
                    actual_output=None if test_case.is_hidden else execution_result.stdout,
                    expected_output=None if test_case.is_hidden else test_case.expected_output,
                    execution_time_ms=execution_result.execution_time_ms,
                    is_hidden=test_case.is_hidden,
                )
            )

            if not passed:
                return JudgeResult(
                    status="WRONG_ANSWER",
                    tests_passed=tests_passed,
                    total_tests=len(test_cases),
                    test_results=test_results,
                )

        return JudgeResult(
            status="ACCEPTED",
            tests_passed=tests_passed,
            total_tests=len(test_cases),
            test_results=test_results,
        )
