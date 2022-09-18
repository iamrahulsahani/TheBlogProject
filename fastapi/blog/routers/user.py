from fastapi import APIRouter, Depends
from database import get_db
from schemas import User,ShowUser
from sqlalchemy.orm import Session
from repository import user


router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.post("/", response_model=ShowUser)
def create_user(request:User, db: Session = Depends(get_db)):
    return user.create(request, db)

@router.get("/{id}", response_model=ShowUser)
def get_user(id : int, db : Session = Depends(get_db)):
    return user.show(id, db)