from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from spectree import SpecTree, SecurityScheme
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()

jwt = JWTManager()

api = SpecTree(
   "flask",
   title="Wish List API",
   version="v.1.0",
   path="docs",
   security_schemes=[
      SecurityScheme(
         name ="api_key",
         data={"type": "apiKey", "name": "Authorization", "in": "header"},
      )
   ],
   security={"api_key":[]},
)

def create_app():
   app = Flask(__name__)

   app.config.from_object(Config)
   
   jwt.init_app(app)

   db.init_app(app)

   #importar models
   from model import WishlistItem, User
   migrate.init_app(app, db)

   #importar controllers
   from controller import wishlist_controller, auth_user
   app.register_blueprint(wishlist_controller)
   app.register_blueprint(auth_user)

   api.register(app)

   return app