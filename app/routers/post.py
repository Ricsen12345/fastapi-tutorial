from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional

# tags only used for documentations purpose "127.0.0.1:8000/docs"
router = APIRouter(prefix="/posts", tags=["Posts"])

# Get all posts (whenever return has a lot of data/rows...
# you should use List[schema] to indicate it!
# @router.get("/", response_model=List[schemas.PostResp])
@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db:Session=Depends(get_db), limit:int=10, search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)
    ).limit(limit).all()
    
    # Get posts with their total vote (join by default = left inner join)
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                       models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    # return posts
    return results

# Get specific post based on id
@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id:int, db: Session = Depends(get_db)):
    # cursor.execute("""
    #     SELECT * FROM posts
    #     WHERE id = %s
    # """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                    models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
                    models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"post with id:{id} does not exist!"
        )
    return post

# create new post to collections of posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResp)
def create_posts(newPost:schemas.PostCreate, db:Session=Depends(get_db), user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #     INSERT INTO posts 
    #         (title, content, published)
    #     VALUES (%s, %s, %s)
    #     RETURNING *
    # """, (newPost.title, newPost.content, newPost.published))
    # conn.commit()
    # new_post = cursor.fetchone()
    new_post = models.Post(owner_id=user.id ,**newPost.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve as in RETURNING *
    print(new_post)
    return new_post

# delete post from myPosts
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db), user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""
    #     DELETE FROM posts
    #     WHERE id = %s
    #     RETURNING *
    # """, (str(id)),)
    # conn.commit()
    # post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post==None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"post with id:{id} does not exist to begin with!"
        )
    
    # User can only delete his/her own posts
    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update with put (all fields must be updated)
@router.put("/{id}", response_model=schemas.PostResp)
def update_post(id:int, updatePost:schemas.PostCreate, db:Session=Depends(get_db), user:int=Depends(oauth2.get_current_user)):    
    # cursor.execute("""
    #     UPDATE posts
    #     SET title = %s,
    #         content = %s,
    #         published = %s
    #     WHERE id = %s
    #     RETURNING *
    # """, (updatePost.title, updatePost.content, updatePost.published, str(id)))
    # conn.commit()
    # post = cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post==None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"post with id:{id} does not exist to begin with!"
        )
    
    # User can only delete his/her own posts
    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.update(updatePost.dict(), synchronize_session=False)
    db.commit()
    return post
