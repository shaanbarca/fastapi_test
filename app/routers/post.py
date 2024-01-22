from .. import schemas, models, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/",  response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = "" ):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #     # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *"""
#     #                 ,(post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # conn.commit()
#     new_post = models.Post(title=post.title, content=post.content, is_published=post.is_published)
#     return new_post

    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # This should load the id and created_at fields from the database
    return new_post

# title str, content str
@router.get("/{id}"
, response_model=schemas.Post
)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #     cursor.execute("""SELECT * from posts where id =%s""", str((id),))
#     post = cursor.fetchone()
#     # post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with id: {id} was not found")
#     return post
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return post



@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts where id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id {id} does not exist")
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != oauth2.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

# @app.put("/posts/{id}")
# def update_posts(id: int, updated_post:schemas.Post, db: Session = Depends(get_db)):

#     # post_query = db.query(models.Post).filter(models.Post.id == id)
#     # post = post_query.first()
#     # if post == None:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     #                         detail=f"post with id {id} does not exist")
#     # post_query.update(updated_post.dict(), synchronize_session=False)
#     # db.commit()
#     # post_query = db.query(models.PostCreate).filter(models.Post.id == id)
#     # post = post_query.first()
#     # if post is None:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     #                         detail=f"post with id {id} does not exist")

#     # # Update the post with the new data
#     # post_query.update(updated_post.dict(), synchronize_session=False)
#     # db.commit()
#     # db.refresh(post)  # Refresh to get the updated post from the database
#     # return {"status": post_query.first()}
#     # # cursor.execute("""SELECT * from posts WHERE id =%s """, (str(id),))
#     # # post = cursor.fetchone()
    
  
#     # if not post:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     #                         detail=f"post with id {id} does not exist")
#     # return {"status": post_query.first()}

   

@router.put("/posts/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    
    if post.owner_id != oauth2.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # Update the post with the new data
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)  # Refresh to get the updated post from the database
    return post