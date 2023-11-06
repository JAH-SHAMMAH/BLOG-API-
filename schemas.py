from pydantic import BaseModel
from datetime import datetime
from typing import Optional
CATEGORY = {
    1: {"category": "Christ",
        "blogs": []
        },
    2: {"category": "Spirituality",
        "blogs": []
        },
    3: {"category": "Music",
        "blogs": []
        },
    4: {"category": "Mysteries",
        "blogs": []
        }
}


class BaseUser(BaseModel):
    username: str
    email: str


class User(BaseModel):
    id: int
    username: str
    email: str


class BlogCategory(BaseModel):
    name: str
    body: str
    date_published: datetime
    # owner: User
    # category: str


class RegisterUser(BaseUser):
    FirstName: str
    LastName: str
    password: str


class Blog(BaseModel):
    name: str
    body: str
    url: str
    date_published: datetime


class BlogRequest(BaseModel):
    date_published: str


class UpdateBlog(BaseModel):
    name: str
    body: str


class UpdateUser(BaseModel):
    username: str
    email: str


class ShowUser(BaseUser):
    blogs: list[Blog] = []

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    id: int
    owner: User

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str
