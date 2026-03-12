from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import User
from ..schemas import UserCreate
from ..deps import get_db
from ..security import hash_password, verify_password, create_access_token


router = APIRouter()

#Register and login

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    db_user = User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401)

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401)

    token = create_access_token({"user_id": db_user.id})

    return {"access_token": token, "token_type": "bearer"}