from fastapi import FastAPI
from db import Base, engine
from routers import user

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include user router
app.include_router(user.router, prefix="/api")
