from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    course_id: str
    text: str
    count_star: int

class FeedbackUpdate(BaseModel):
    text: str
    count_star: int

