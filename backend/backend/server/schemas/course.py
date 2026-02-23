from pydantic import BaseModel

class CourseCreate(BaseModel):
    name: str
    desc: str
    keywords: list[str]
    rating: float
    count_views: int

class CourseUpdate(BaseModel):
    name: str
    desk: str
    keywords: list[str]
