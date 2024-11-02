from sqlalchemy import Column, Integer, String,DateTime,Time,ForeignKey
from db import Base
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship

class RecognisedFaces(Base):
    __tablename__ = "recognised_faces"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"), unique=True)
    datetime = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="recognised_faces")

# models.py
class User(Base):
    __tablename__ = "users"
    
    username = Column(String, primary_key=True, unique=True, index=True)
    photo = Column(String, nullable=True)  # path to the photo

    recognised_faces = relationship("RecognisedFaces", back_populates="user")

class UnknownRecognisedFaces(Base):
    __tablename__ = "unknown_recognised_faces"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)  # Path to the unknown face image
    datetime = Column(DateTime, default=datetime.utcnow)  # Time when captured