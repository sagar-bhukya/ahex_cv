from sqlalchemy import Column, Integer, String,DateTime,Time,ForeignKey,UniqueConstraint
from db import Base
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship

# RecognisedFaces model with a unique constraint on username and date
class RecognisedFaces(Base):
    __tablename__ = "recognised_faces"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"))
    datetime = Column(DateTime, default=func.now())
    date = Column(DateTime, default=func.current_date())  # Computed column for date portion

    user = relationship("User", back_populates="recognised_faces")

    # Composite unique constraint on username and date
    __table_args__ = (
        UniqueConstraint('username', 'date', name='uix_username_date'),
    )

# User model with an id field and back-populated relationship
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each user
    username = Column(String, unique=True, nullable=False, index=True)
    photo = Column(String, nullable=True)  # Path to the photo

    recognised_faces = relationship("RecognisedFaces", back_populates="user")
class UnknownRecognisedFaces(Base):
    __tablename__ = "unknown_recognised_faces"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)  # Path to the unknown face image
    datetime = Column(DateTime, default=datetime.utcnow)  # Time when captured