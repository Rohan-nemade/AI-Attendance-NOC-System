from fastapi import FastAPI
from app.db import Base, engine
from app.models import *  # import models so tables are registered

from app.routes.students import router as students_router
from app.routes.teachers  import router as teachers_router
from app.routes.subjects  import router as subjects_router
from app.routes.assignments import router as assignments_router
from app.routes.submissions import router as submissions_router
from app.routes.notifications import router as notifications_router

# Create all tables (dev). For prod, use Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="P-1 AI Attendance & Assignment Backend", version="1.0.0")

app.include_router(students_router,     prefix="/api")
app.include_router(teachers_router,     prefix="/api")
app.include_router(subjects_router,     prefix="/api")
app.include_router(assignments_router,  prefix="/api")
app.include_router(submissions_router,  prefix="/api")
app.include_router(notifications_router, prefix="/api")

@app.get("/")
def health():
    return {"ok": True, "service": "P-1 Backend"}
