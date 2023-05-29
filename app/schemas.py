from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    
    title:str
    content:str
    published:bool = True
 
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime
    class Config:
            orm_mode = True
            
            
class PostResponse(PostBase):
    
    id:int
    created_at:datetime
    user_id:int
    owner:UserOut
    class Config:
            orm_mode = True

class PostOut(BaseModel):
    Posts:PostResponse
    Votes:int
    class Config:
            orm_mode = True
    

            
class UserCreate(BaseModel):
    
    email:EmailStr
    password:str
    

class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id : int
    dir:conint(le=1)