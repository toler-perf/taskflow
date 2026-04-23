import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    tasks = relationship("Task", back_populates="category")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(Status), default=Status.todo, nullable=False)
    priority = Column(Enum(Priority), default=Priority.medium, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="tasks")