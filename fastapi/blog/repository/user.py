from sqlalchemy.orm import Session
from fastapi import HTTPException
from hashing import Hash
from schemas import User
import models

def create(request:User, db: Session):
    hashed_password = Hash.encrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id : int, db : Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user