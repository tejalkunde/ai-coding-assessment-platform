from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.problems.router import problem_service


client = TestClient(app)


def setup_function():
    problem_service._problems.clear()


def test_create_problem():
    response = client.post(
        "/problems/",
        json={
            "problem_id": "sum-two-numbers",
            "title": "Sum of Two Numbers",
            "description": "Read two integers and print their sum.",
            "difficulty": "EASY",
            "supported_languages": ["python"],
            "test_cases": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["problem_id"] == "sum-two-numbers"
    assert data["title"] == "Sum of Two Numbers"


def test_list_problems():
    client.post(
        "/problems/",
        json={
            "problem_id": "sum-two-numbers",
            "title": "Sum of Two Numbers",
            "description": "Read two integers and print their sum.",
            "difficulty": "EASY",
            "supported_languages": ["python"],
            "test_cases": [],
        },
    )

    response = client.get("/problems/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_problem():
    client.post(
        "/problems/",
        json={
            "problem_id": "sum-two-numbers",
            "title": "Sum of Two Numbers",
            "description": "Read two integers and print their sum.",
            "difficulty": "EASY",
            "supported_languages": ["python"],
            "test_cases": [],
        },
    )

    response = client.get("/problems/sum-two-numbers")

    assert response.status_code == 200
    assert response.json()["problem_id"] == "sum-two-numbers"


def test_missing_problem_returns_404():
    response = client.get("/problems/missing-problem")

    assert response.status_code == 404


def test_duplicate_problem_returns_409():
    payload = {
        "problem_id": "sum-two-numbers",
        "title": "Sum of Two Numbers",
        "description": "Read two integers and print their sum.",
        "difficulty": "EASY",
        "supported_languages": ["python"],
        "test_cases": [],
    }

    client.post("/problems/", json=payload)

    response = client.post("/problems/", json=payload)

    assert response.status_code == 409


def test_add_test_case():
    client.post(
        "/problems/",
        json={
            "problem_id": "sum-two-numbers",
            "title": "Sum of Two Numbers",
            "description": "Read two integers and print their sum.",
            "difficulty": "EASY",
            "supported_languages": ["python"],
            "test_cases": [],
        },
    )

    response = client.post(
        "/problems/sum-two-numbers/test-cases",
        json={
            "input_data": "2 3",
            "expected_output": "5",
            "is_hidden": False,
            "time_limit_seconds": 5,
            "memory_limit_mb": 256,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["test_cases"]) == 1
    assert data["test_cases"][0]["expected_output"] == "5"
