from fastapi import APIRouter, HTTPException

from backend.app.problems.router import problem_service
from backend.app.submissions.models import SubmissionRequest
from backend.app.submissions.service import SubmissionService


router = APIRouter(prefix="/submissions", tags=["Submissions"])

submission_service = SubmissionService(
    problem_service=problem_service
)


@router.post("/")
def submit_solution(request: SubmissionRequest):
    try:
        return submission_service.submit(request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
