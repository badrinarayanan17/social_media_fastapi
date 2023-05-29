from fastapi import Body, FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. database import get_db 
from typing import Optional,List


router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

# Get Posts

# @router .get("/",response_model=List[schemas.PostResponse])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
              limit:int = 10, skip : int = 0, search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # post = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Posts, func.count(models.Votes.post_id).label("Votes")).join(
        models.Votes,models.Posts.id == models.Votes.post_id,isouter=True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    
    results = list(map(lambda x:x._mapping,results))
    return results

  
# --------------------------------------------------------------------------------------------------------------------------- # 

# Create Post

@router .post("/",status_code=status.HTTP_201_CREATED,response_model=List[schemas.PostResponse])
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    print(current_user.email)
    new_post = models.Posts(user_id = current_user.id,**post.dict())
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchall()
    # conn.commit()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,20000)
    # my_posts.append(post_dict)
    # print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {new_post}


# # Get the latest posts

# @app.get("/posts/latest")
# def get_latest():
#     latest = my_posts[len(my_posts)-1]
#     print(latest)
#     return {"data":latest}


  
# --------------------------------------------------------------------------------------------------------------------------- # 

# Get Single Post

@router.get("/{id}",response_model=schemas.PostOut)  #Here id is a path parameter inside the path operations
def get_post(id:int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):    #Specifying the type of the path parameter to indicate
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Posts).filter(models.Posts.id == id).first()

    post = db.query(models.Posts, func.count(models.Votes.post_id).label("Votes")).join(
        models.Votes,models.Posts.id == models.Votes.post_id,isouter=True).group_by(
            models.Posts.id).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"Post with id : {id} was not found"}
    # print(type(id))      #id is in string, converting to int is must
    return post
# Error thrown - "value is not a valid integer"

  
# --------------------------------------------------------------------------------------------------------------------------- # 

# Deleting a post

@router .delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    # my_posts.pop(index)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    
  
# --------------------------------------------------------------------------------------------------------------------------- # 

# Updating posts

@router .put("/{id}")
def update_posts(id:int,post_update:schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the requested action")
    post_query.update(post_update.dict(),synchronize_session=False)
    db.commit()
    return {
        post_query.first()
    }
    