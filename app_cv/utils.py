import shutil
from fastapi import UploadFile
import os
import uuid
import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
from models import RecognisedFaces,UnknownRecognisedFaces
import db
from sqlalchemy.orm import Session
# Function to save user images
def save_image(file: UploadFile):
    folder_path = 'images'
    os.makedirs(folder_path, exist_ok=True)
    file_location = os.path.join(folder_path, file.filename)
    
    with open(file_location, "wb") as f:
        f.write(file.file.read())  # Save the image
    return file_location

# Function to save unknown images
def save_unknown_image(image):
    uuid_filename = f"{uuid.uuid4()}.jpg"  # Generate unique filename
    path = os.path.join("unknown_recognised_faces", uuid_filename)
    os.makedirs("unknown_recognised_faces", exist_ok=True)
    
    cv2.imwrite(path, image)  # Save the image using OpenCV
    return path

# Handle recognition logic
def handle_recognition(name, face_image, db):
    if name != "Unknown Person":
        recognized_entry = RecognisedFaces(name=name, datetime=datetime.utcnow())
        db.add(recognized_entry)
        db.commit()
    else:
        image_path = save_unknown_image(face_image)
        unknown_entry = UnknownRecognisedFaces(path=image_path, datetime=datetime.utcnow())
        db.add(unknown_entry)
        db.commit()

# Load images and class names dynamically
def load_known_faces():
    path = 'images'
    images = []
    classNames = []
    imageFiles = os.listdir(path)

    for file in imageFiles:
        file_path = os.path.join(path, file)
        print(f"Loading image from: {file_path}")  # Debugging line
        image = cv2.imread(file_path)
        
        if image is None:
            print(f"Failed to load image: {file_path}")  # Debugging line
            continue

        images.append(image)
        classNames.append(os.path.splitext(file)[0])

    return images, classNames

# Function to find encodings of each image
def findEncodings(images):
    encodeList = []
    for img in images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
        encodings = face_recognition.face_encodings(img_rgb)
        
        if encodings:
            encodeList.append(encodings[0])  # Append the first encoding
        else:
            print("No face found in image, skipping.")

    return encodeList

# Start face recognition
def start_face_recognition(db):
    images, classNames = load_known_faces()
    
    if not images:
        print("No images loaded for recognition.")
        return  # Handle the case where no images are found

    encodeListKnown = findEncodings(images)

    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        if not success:
            break

        img_small = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        img_rgb = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

        facesInFrame = face_recognition.face_locations(img_rgb)
        encodesInFrame = face_recognition.face_encodings(img_rgb, facesInFrame)

        for encodeFace, faceLoc in zip(encodesInFrame, facesInFrame):
            faceDistances = face_recognition.face_distance(encodeListKnown, encodeFace)
            bestMatchIndex = np.argmin(faceDistances)

            if faceDistances[bestMatchIndex] < 0.5:  # Adjust threshold as necessary
                name = classNames[bestMatchIndex].upper()
            else:
                name = "Unknown Person"

            # Handle recognition
            handle_recognition(name, img_rgb, db)

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()