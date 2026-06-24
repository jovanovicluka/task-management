from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app import schemas
from app.security import hash_password, verify_password
from app.jwt import create_access_token, create_refresh_token, decode_token
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post('/register')
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post('/login', response_model=schemas.Token)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail='Invalid credentials'
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        {"sub": str(db_user.id)}
    )

    refresh_token = create_refresh_token(
        {"sub": str(db_user.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get(
"/me",
response_model=schemas.CurrentUserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post("/refresh")
def refresh_access_token(
    data: schemas.RefreshTokenRequest
):
    payload = decode_token(
        data.refresh_token
    )

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )

    user_id = payload.get("sub")

    new_access_token = create_access_token(
        {"sub": user_id}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
