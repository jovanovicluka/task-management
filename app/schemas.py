from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    owner_id: int

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    project_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    project_id: int

    class Config:
        from_attributes = True