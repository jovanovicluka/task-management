from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db
from app.models import Base, Project, Task

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get("/projects", response_model=list[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@app.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return {"error": "Project not found"}

    return project


@app.post("/projects", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):

    db_project = Project(
        name=project.name,
        description=project.description,
        owner_id=project.owner_id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return {"error": "Project not found"}

    db.delete(project)
    db.commit()

    return {"message": "Project deleted"}


@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):

    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        project_id=task.project_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}


@app.patch("/tasks/{task_id}/status")
def update_task_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status

    db.commit()
    db.refresh(task)

    return task