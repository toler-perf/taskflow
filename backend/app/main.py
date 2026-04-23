from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .database import engine, get_db
from .routers import tasks

app = FastAPI(title="TaskFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api", tags=["Tasks & Categories"])

@app.get("/")
def root():
    return {"message": "TaskFlow API 🚀", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health_check(db = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "db": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "db": "disconnected", "error": str(e)}