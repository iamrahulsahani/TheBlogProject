from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hashing import Hash
from database import get_db
from JWTtoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
import models

router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login")
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist!")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}