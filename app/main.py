import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as assignment_router
from app.database import Base,engine
from app import models

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

app = FastAPI()
app.include_router(assignment_router)

# Allow frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Attendance-NOC API is running"}

Base.metadata.create_all(bind=engine)
