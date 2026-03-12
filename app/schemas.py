from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskResponse(BaseModel):

    id: int
    title: str
    description: str

    class Config:
        orm_mode = True