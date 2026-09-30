from backend.app.execution.output_comparator import compare_output


def test_exact_match():
    assert compare_output("5", "5") is True


def test_trailing_newline_is_ignored():
    assert compare_output("5\n", "5") is True


def test_surrounding_whitespace_is_ignored():
    assert compare_output(" 5 ", "5") is True


def test_different_output_fails():
    assert compare_output("5", "6") is False
