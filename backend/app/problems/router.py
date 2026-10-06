from fastapi import APIRouter, HTTPException

from backend.app.problems.models import Problem
from backend.app.problems.service import ProblemService


router = APIRouter(prefix="/problems", tags=["Problems"])

problem_service = ProblemService()


@router.post("/")
def create_problem(problem: Problem):
    try:
        return problem_service.create_problem(problem)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.get("/")
def list_problems():
    return problem_service.list_problems()


@router.get("/{problem_id}")
def get_problem(problem_id: str):
    try:
        return problem_service.get_problem(problem_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/{problem_id}/test-cases")
def add_test_case(problem_id: str, test_case: dict):
    from backend.app.problems.models import ProblemTestCase

    try:
        problem_test_case = ProblemTestCase(**test_case)
        return problem_service.add_test_case(problem_id, problem_test_case)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
