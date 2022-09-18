from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas import Blog
import models

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request : Blog, db: Session):
    new_blog = models.Blog(title = request.title,body =  request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=404, detail="This blog is not found")
    db.commit()

def update(id:int, request:Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update(request)
    if not blog:
        raise HTTPException(status_code=404, detail="This blog is not found")
    db.commit()
    return "updated"

def show(id:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="blog with given id is not available")
    return blog