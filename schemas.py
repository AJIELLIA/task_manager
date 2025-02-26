"""
schemas.py
Определяет входные схемы данных с помощью Pydantic.
"""
from pydantic import BaseModel
from typing import List, Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class Task(TaskCreate):
    id: int
    completed: bool

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    tasks: List[Task]
