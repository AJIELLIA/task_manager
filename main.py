"""
main.py
Основной файл приложения FastAPI
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Task as TaskModel
from schemas import TaskCreate, TaskList, Task
import uvicorn
from database import get_db
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Создает новую задачу."""
    db_task = TaskModel(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logging.info(f"Задача {db_task.id} создана")
    return db_task


@app.get("/tasks/", response_model=TaskList)
async def get_tasks(skip: int = 0, limit: int = 10, completed: bool = None, db: Session = Depends(get_db)):
    """Получает список задач, с возможностью фильтрации по статусу завершенности."""
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter(TaskModel.completed == completed)
    tasks = query.offset(skip).limit(limit).all()
    return TaskList(tasks=tasks)


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Получает конкретную задачу по ID."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    """Обновляет задачу по ID."""
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.dict().items():
        setattr(db_task, key, value)

    db.commit()
    logging.info(f"Задача {db_task.id} обновлена")
    return db_task


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Удаляет задачу по ID."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    logging.info(f"Задача {task.id} удалена")
    return task


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
