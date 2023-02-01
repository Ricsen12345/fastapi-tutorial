from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResp(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

# User should provide this data! (validation)
class PostBase(BaseModel):
    title: str                      # Required
    content: str                    # Required
    published: bool = True          # Optional with default value

# Creating new post
class PostCreate(PostBase):
    pass

# Template for response (developer should send this as response of request)
class PostResp(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResp

    # Required for all response classes
    # Automatically filter out all fields which doesn't belong to this class
    class Config:
        orm_mode = True

class PostVote(BaseModel):
    Post: PostResp
    votes: int

    class Config:
        orm_mode = True

# Return JWT token template
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

# Template for JWT Payload
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
