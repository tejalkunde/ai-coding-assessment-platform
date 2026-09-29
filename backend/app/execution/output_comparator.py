def normalize_output(output: str) -> str:
    return output.strip()


def compare_output(actual: str, expected: str) -> bool:
    return normalize_output(actual) == normalize_output(expected)
