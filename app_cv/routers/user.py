from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from db import SessionLocal
from models import User,RecognisedFaces,UnknownRecognisedFaces
from schemas import UserResponse,RecognisedFaceResponse,UnknownRecognisedFaceResponse,UserCreate
from utils import save_image,start_face_recognition
from typing import List
import cv2

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/users/", response_model=UserResponse)
async def create_user(
    username: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check if user already exists
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    # Save the image and get the path
    photo_path = save_image(file)

    # Create and add the user
    db_user = User(username=username, photo=photo_path)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
@router.get("/users/", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Endpoint to get a user by ID
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/", response_model=dict)
async def delete_all_users(db: Session = Depends(get_db)):
    # Delete all users
    db.query(User).delete()
    db.commit()
    return {"message": "All users have been deleted"}



@router.get("/recognised_faces/", response_model=List[RecognisedFaceResponse])
def get_recognised_faces(db: Session = Depends(get_db)):
    faces = db.query(RecognisedFaces).all()
    return faces

@router.get("/unknown_faces/",response_model=List[UnknownRecognisedFaceResponse])
async def get_unknown_faces(db: Session = Depends(get_db)):
    return db.query(UnknownRecognisedFaces).all()

@router.post("/start_recognition/")
async def start_recognition(db: Session = Depends(get_db)):
    start_face_recognition(db)
    return {"message": "Face recognition started."}