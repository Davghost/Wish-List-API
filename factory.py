from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def create_app():
   app = Flask(__name__)

   app.config.from_object(Config)

   db.init_app(app)

   #importar models
   from model import WishlistItem
   migrate.init_app(app, db)

   #importar controllers
   from controller import wishlist_controller
   app.register_blueprint(wishlist_controller)

   return app