from email import message
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2, schemas
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix='/votes', tags=['votes'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post doesn't exist")

    votes = db.query(models.Vote).filter(models.Vote.post_id ==
                                         vote.post_id, models.Vote.user_id == current_user.id)

    found_votes = votes.first()

    if vote.dir == 1:
        if found_votes:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.email} as already voted {found_votes.id}")

        new_vote = models.Vote(post_id=vote.post_id,
                               user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'messagge': 'Successfully added vote'}
    else:
        if not found_votes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"votes doesn't exist")

        votes.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Successfully delete vote'}
