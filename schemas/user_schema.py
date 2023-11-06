from pydantic import BaseModel
from typing import Optional

class User_schema(BaseModel):
    id:Optional[int] = None
    name:str
    username:str
    user_pass:str

class DataUser(BaseModel):
    username:str
    user_pass:str
