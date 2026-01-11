from werkzeug.security import check_password_hash, generate_password_hash
from factory import db
from datetime import datetime, timezone

class User(db.Model):
   __tablename__ = "user"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(64), nullable=False, unique=True, index=True)
   password_hash = db.Column(db.String(256), index=True)
   email = db.Column(db.String(128), nullable=False, index=True, unique=True)
   birthdate = db.Column(db.DateTime)
   created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

   @property
   def password(self):
      raise AttributeError("Password is not a readable attribute")
   
   @password.setter
   def password(self, password):
      self.password_hash = generate_password_hash(password)

   def verify_password(self, password):
      return check_password_hash(self.password_hash, password)