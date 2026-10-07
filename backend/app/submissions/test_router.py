from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.problems.router import problem_service


client = TestClient(app)


def setup_problem():
    problem_service._problems.clear()

    response = client.post(
        "/problems/",
        json={
            "problem_id": "echo-api-test",
            "title": "Echo Input",
            "description": "Print the input.",
            "difficulty": "easy",
            "supported_languages": ["python"],
            "test_cases": [
                {
                    "input_data": "5\n",
                    "expected_output": "5\n",
                    "is_hidden": False,
                    "time_limit_seconds": 5,
                    "memory_limit_mb": 256
                }
            ]
        },
    )

    assert response.status_code == 200


def test_submission_api_accepts_correct_solution():
    setup_problem()

    response = client.post(
        "/submissions/",
        json={
            "problem_id": "echo-api-test",
            "source_code": "print(input())",
            "language": "python"
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ACCEPTED"
    assert response.json()["tests_passed"] == 1
    assert response.json()["total_tests"] == 1


def test_submission_api_rejects_wrong_solution():
    setup_problem()

    response = client.post(
        "/submissions/",
        json={
            "problem_id": "echo-api-test",
            "source_code": 'print("wrong")',
            "language": "python"
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "WRONG_ANSWER"
    assert response.json()["tests_passed"] == 0
    assert response.json()["total_tests"] == 1


def test_submission_api_returns_404_for_missing_problem():
    problem_service._problems.clear()

    response = client.post(
        "/submissions/",
        json={
            "problem_id": "does-not-exist",
            "source_code": "print(input())",
            "language": "python"
        },
    )

    assert response.status_code == 404
