from pydantic import BaseModel


class UserLogin(BaseModel):
    login: str
    password: str


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    role: str
    exp: str
    stack: list[str]


class UserResponse(BaseModel):
    login: str
    first_name: str
    last_name: str
    age: int
    role: str
    exp: str
    stack: list[str]
