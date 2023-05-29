from fastapi import Body, FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from .. database import get_db 
from ..import schemas,oauth2

router = APIRouter(
    tags=['Vote'],
    prefix="/vote"
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote_post(vote:schemas.Vote, db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} has not been found")
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir) == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has aldready liked on post {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id )
        db.add(new_vote)
        db.commit()
        return {
            "data":"Like added successfully"
        }
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {
            "data" : "Like deleted successfully"
        }
        
    
    