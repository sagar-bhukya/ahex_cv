from pydantic import BaseModel
from fastapi import Form
from datetime import datetime,time


class UserCreate(BaseModel):
    username: str

    # Use Form to receive form data instead of JSON
    def __init__(self, username: str = Form(...)):
        self.username = username
class UserResponse(BaseModel):
    id: int
    username: str
    photo: str
    created_at: datetime  # New field for timestamp
    class Config:
        orm_mode = True


class RecognisedFaceResponse(BaseModel):
    name: str
    datetime: datetime

class UnknownRecognisedFaceResponse(BaseModel):
    path: str
    datetime: datetime