from typing import Literal

from pydantic import BaseModel, Field, field_validator


class SubmissionRequest(BaseModel):
    problem_id: str = Field(min_length=1)
    source_code: str = Field(min_length=1)
    language: Literal["python"]

    @field_validator("problem_id", "source_code")
    @classmethod
    def reject_whitespace_only(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field cannot be empty or whitespace.")
        return value


class SubmissionResponse(BaseModel):
    status: str
    tests_passed: int
    total_tests: int
