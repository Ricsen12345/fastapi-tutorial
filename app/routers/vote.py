from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session=Depends(get_db), user:int=Depends(oauth2.get_current_user)):
    # Check whether post exist or not
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {vote.post_id} doesn't exist!")

    # Check whether certain user already has vote on certain post
    voteQuery = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,
                                             models.Vote.user_id==user.id)
    foundVote = voteQuery.first()

    # If user press like button on the post
    if vote.dir==1:
        # If user already liked the post in the past
        if foundVote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {user.id} has already voted on post {vote.post_id}"
            )
        # If user haven't liked the post in the paast
        newVote = models.Vote(post_id=vote.post_id, user_id=user.id)
        db.add(newVote)
        db.commit()
        return {"Message": "successfully updated vote"}
    # If user press dislike button
    else:
        # If the vote doesn't exist
        if not foundVote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote can't be applied on post that doesn't exist"
            )
        # If vote exist delete it!
        voteQuery.delete(synchronize_session=False)
        db.commit()
        return {"Message": "successfully updated vote"}
    pass