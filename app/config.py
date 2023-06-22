from pydantic import BaseSettings

class Settings(BaseSettings):
    
    database_hostname : str
    database_port : str
    db_password_secret : str
    database_name : str
    db_username_secret : str
    secret_key : str
    algorithm : str
    access_token_secret : int
    
    class Config:
        env_file = ".env"
        
settings = Settings()