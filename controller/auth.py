from factory import db, api
from model import User
from spectree import Response
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from schemas.auth import LoginMessage, LoginResponseMessage, DefaultResponseAuth, CreateUser
from schemas.wishlist_item import DefaultResponse
from datetime import datetime
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash

auth_user = Blueprint('auth_user', __name__, url_prefix='/users')

@auth_user.post("/login")
@api.validate(json=LoginMessage, resp=Response(HTTP_200=LoginResponseMessage, HTTP_401=DefaultResponseAuth),security={}, tags=["auth"])
def login():
   """
   Login
   """
   data = request.json

   user = db.session.scalars(select(User).filter_by(name=data["name"])).first()
   if user and user.verify_password(data["password"]):
      return {
         "access_token": create_access_token(
            identity=user.name, expires_delta=None
         )
      },200
   
   return {"msg": "Username and password do not match"}, 401

@auth_user.post("/")
@api.validate(json=CreateUser, resp=Response(HTTP_201=DefaultResponseAuth), security={}, tags=["auth"])
def create_user():
   """
   Create an user
   """
   data = request.json

   if db.session.scalars(select(User).filter_by(name=data["name"])).first():
      return {"msg": "username not available"}, 409
   
   if "birthdate" in data:
      if data["birthdate"].endswith("Z"):
         data["birthdate"] = data["birthdate"][:-1]

   user = User(
   name=data["name"],
   email=data["email"],
   password_hash=generate_password_hash(data["password"]),
   birthdate=(
      datetime.fromisoformat(data["birthdate"]) if "birthdate" in data else None
   ))

   db.session.add(user)
   db.session.commit()

   return {"msg": "User created successfully."}, 201

@auth_user.post("/logout")
@api.validate(resp=Response(HTTP_200=DefaultResponseAuth), tags=["auth"])
@jwt_required()
def logout():
    """
    Logout user
    """

    return {"msg": "Logout successfully."}