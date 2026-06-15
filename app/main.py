from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db
from app.models import Base
from app.models import Project

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