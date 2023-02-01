from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

# tags only used for documentations purpose "127.0.0.1:8000/docs"
router = APIRouter(prefix="/users", tags=["Users"])

# create users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResp)
def create_user(newUser: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashedPassword = utils.hash(newUser.password)
    newUser.password = hashedPassword
    # Insert data
    new_user = models.User(**newUser.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Get user
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResp)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} doesn't exist"
        )
    return user
