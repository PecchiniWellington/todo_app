from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import func, outerjoin
from sqlalchemy.orm import Session
from app import models, oauth2, schemas
from ..database import get_db
from typing import List, Optional


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)
""" Post List """


@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Post, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


""" Post Detail """


@router.get("/{id}", response_model=schemas.PostOut)
def get_post_detail(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_detail = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Post, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {id} not found')

    return post_detail


""" Post Create """


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    print(current_user.id)
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


""" Post Delete """


@ router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(
        models.Post.id == id).first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'not authorized to perform requested action')

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {id} not found')
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


""" Post Update """


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    find_post = db.query(models.Post).filter(models.Post.id == id)

    if find_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'not authorized to perform requested action')

    if find_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {id} not found')
    else:
        find_post.update(post.dict(), synchronize_session=False)
        db.commit()

        return find_post.first()
