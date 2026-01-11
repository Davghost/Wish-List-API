from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class LoginMessage(BaseModel):
   name: str
   password: str

class LoginResponseMessage(BaseModel):
   access_token: str

class DefaultResponseAuth(BaseModel):
   msg: str

class CreateUser(BaseModel):
   name: str
   password: str
   email: str
   birthdate: Optional[datetime]