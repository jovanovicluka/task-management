from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import users, tasks, projects;

app = FastAPI()
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is running"}