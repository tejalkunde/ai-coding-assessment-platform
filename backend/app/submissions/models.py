from pydantic import BaseModel


class SubmissionRequest(BaseModel):
    problem_id: str
    source_code: str
    language: str


class SubmissionResponse(BaseModel):
    status: str
    tests_passed: int
    total_tests: int