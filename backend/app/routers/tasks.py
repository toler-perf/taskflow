from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Task, Category
from ..schemas import TaskCreate, TaskUpdate, TaskOut, CategoryCreate, CategoryOut

router = APIRouter()

# --- Категории ---
@router.post("/categories/", response_model=CategoryOut, status_code=201)
def create_category(cat: CategoryCreate, db: Session = Depends(get_db)):
    if db.query(Category).filter(Category.name == cat.name).first():
        raise HTTPException(status_code=400, detail="Category already exists")
    db_cat = Category(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@router.get("/categories/", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# --- Задачи ---
@router.post("/tasks/", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    if not db.query(Category).filter(Category.id == task.category_id).first():
        raise HTTPException(status_code=404, detail="Category not found")
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[TaskOut])
def read_tasks(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id.desc()).offset(skip).limit(limit).all()

@router.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()