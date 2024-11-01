from sqlalchemy import Column, Integer, String,DateTime,Time
from db import Base
from sqlalchemy.sql import func
from datetime import datetime
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    photo = Column(String, nullable=True)  # Path to the stored photo
    created_at = Column(DateTime, default=func.now(), nullable=False)
    


class RecognisedFaces(Base):
    __tablename__ = "recognised_faces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Stores username
    datetime = Column(DateTime, default=datetime.utcnow)  # Time when captured

class UnknownRecognisedFaces(Base):
    __tablename__ = "unknown_recognised_faces"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)  # Path to the unknown face image
    datetime = Column(DateTime, default=datetime.utcnow)  # Time when captured