from fastapi import APIRouter
from schemas import Blog, ShowBlog, User
from fastapi import Depends
from typing import List
from database import get_db
from sqlalchemy.orm import Session
from repository import blog
from oauth2 import get_current_user

router = APIRouter(
    tags=["Blogs"],
    prefix="/blog"

)

@router.get("/", response_model=List[ShowBlog], tags=["Blogs"])
def all(db: Session = Depends(get_db), get_current_user:User = Depends(get_current_user)):
    return blog.get_all(db)

@router.post("/", status_code=201, tags=["Blogs"])
def create_blog(request : Blog, db: Session = Depends(get_db), get_current_user:User = Depends(get_current_user)):
    return blog.create(request, db)

@router.get("/{id}", status_code=200, response_model=ShowBlog, tags=["Blogs"])
def show(id:int, db: Session = Depends(get_db), get_current_user:User = Depends(get_current_user)):
    return blog.show(id, db)

@router.delete("/{id}", status_code=204, tags=["Blogs"])
def destroy(id:int, db: Session = Depends(get_db), get_current_user:User = Depends(get_current_user)):
    return blog.destroy(id,db)

@router.put("/{id}", status_code=202, tags=["Blogs"])
def update(id:int, request:Blog, db: Session = Depends(get_db), get_current_user:User = Depends(get_current_user)):
    return blog.update(id, request, db)