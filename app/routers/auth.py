from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas
from ..database import get_db

router = APIRouter(tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm only return "username" and "password"
    # Check whether user exist/not
    findUser = db.query(models.User).filter(models.User.email == user.username).first()
    if not findUser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # Check whether password for that user is correct/not
    if not utils.verify(user.password, findUser.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # Create JWT Token
    access_token = oauth2.create_accesss_token(data = {"user_id": findUser.id})

    return {"access_token": access_token, "token_type": "bearer"}