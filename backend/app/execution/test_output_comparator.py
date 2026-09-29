from backend.app.execution.output_comparator import compare_output


tests = [
    ("5", "5", True),
    ("5\n", "5", True),
    (" 5 ", "5", True),
    ("5", "6", False),
]


for actual, expected, expected_result in tests:
    result = compare_output(actual, expected)

    print(
        f"Actual={actual!r}, "
        f"Expected={expected!r}, "
        f"Result={result}, "
        f"Expected Result={expected_result}"
    )

    assert result == expected_result


print("All comparator tests passed.")
