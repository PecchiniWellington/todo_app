from app import models, schemas, utils
from ..database import get_db
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)



""" User Create """


@router.post('/', response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


""" User Get """


@router.get('/', response_model=List[schemas.UserOut])
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user_detail(id: int, db: Session = Depends(get_db)):
    find_user = db.query(models.User).filter(models.User.id == id).first()

    if find_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} not exist')
    else:
        return find_user
