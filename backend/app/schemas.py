from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .models import Status, Priority

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    model_config = {"from_attributes": True}

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    status: Status = Status.todo
    priority: Priority = Priority.medium
    category_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    category_id: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryOut] = None
    model_config = {"from_attributes": True}