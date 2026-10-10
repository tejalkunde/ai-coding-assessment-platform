import pytest
from pydantic import ValidationError

from backend.app.submissions.models import SubmissionRequest


def test_valid_python_submission():
    request = SubmissionRequest(
        problem_id="two-sum",
        source_code="print(1 + 1)",
        language="python",
    )

    assert request.problem_id == "two-sum"
    assert request.language == "python"


def test_unsupported_language_is_rejected():
    with pytest.raises(ValidationError):
        SubmissionRequest(
            problem_id="two-sum",
            source_code="System.out.println(2);",
            language="java",
        )


@pytest.mark.parametrize("field", ["problem_id", "source_code"])
@pytest.mark.parametrize("value", ["", "   "])
def test_empty_or_whitespace_fields_are_rejected(field, value):
    data = {
        "problem_id": "two-sum",
        "source_code": "print(1 + 1)",
        "language": "python",
    }
    data[field] = value

    with pytest.raises(ValidationError):
        SubmissionRequest(**data)
