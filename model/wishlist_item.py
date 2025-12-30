from factory import db

class WishlistItem(db.Model):
   __tablename__ = "WishlistItem"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.UnicodeText, nullable=False)
   description = db.Column(db.UnicodeText, nullable=True)
   link = db.Column(db.UnicodeText, nullable=True)
   purchased = db.Column(db.Boolean, default=False)
   sort_order = db.Column(db.Integer, nullable=True)

   def __repr__(self) -> str:
      return f"<User {self.username}>"