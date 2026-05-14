from pydantic import BaseModel


class ClassificationRequest(BaseModel):
    comment: str


class ClassificationResponse(BaseModel):
    comment: str
    label: str
    score: float
