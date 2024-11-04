from pydantic import BaseModel,Field
from fastapi import Form
from datetime import datetime,time


class UserCreate(BaseModel):
    username: str = Field(..., description="The username of the user")

class UserResponse(BaseModel):
    id:int
    username: str
    photo: str
    # Uncomment if you want to include created_at
    # created_at: datetime

    class Config:
        orm_mode = True
class RecognisedFaceResponse(BaseModel):
    id:int
    username: str
    datetime: datetime

    class Config:
        orm_mode = True

class UnknownRecognisedFaceResponse(BaseModel):
    path: str
    datetime: datetime