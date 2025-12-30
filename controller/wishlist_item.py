from flask import Blueprint, jsonify
from factory import db
from model.wishlist_item import WishlistItem
from flask.globals import request
from sqlalchemy import select

wishlist_controller = Blueprint("wishlist_controller", __name__, url_prefix="/wishlist")

@wishlist_controller.get("/<int:item_id>")
def get_item(item_id):
   item = db.session.get(WishlistItem, item_id)

   if item is None:
      return f"There is no item with id {item_id}", 404

   return {
      "id": item.id,
      "name": item.name,
      "description": item.description if item.description else None,
      "link": item.link if item.link else None,
      "purchased": item.purchased,
      "sort_order": item.sort_order,
   }, 200

@wishlist_controller.get("/")
def get_items():
   items = db.session.scalars(select(WishlistItem)).all()

   return jsonify(
      [
         {
            "id": item.id,
            "name": item.name,
            "description": item.description if item.description else None,
            "link": item.link if item.link else None,
            "purchased": item.purchased,
            "sort_order": item.sort_order,
         }
         for item in items
      ]
   ),200

@wishlist_controller.post("/")
def post_item():
   data = request.json

   if db.session.scalar(select(WishlistItem).filter_by(name=data["name"])):
      return {"msg": "item's name not available"}, 409
   
   item = WishlistItem(
      name=data["name"],
      description=data["description"] if "description" in data else None,
      link=data["link"] if "link" in data else None,
      purchased=data["purchased"],
      sort_order=data["sort_order"]
   )

   db.session.add(item)
   db.session.commit()

   return {"msg": "User created successfully."}, 201

@wishlist_controller.put("/<int:item_id>")
def put_item(item_id):
   item = db.session.get(WishlistItem, item_id)

   if item is None:
      return {"msg": f"There is no item with id {item_id}"}, 404
   
   data = request.json

   item.name=data["name"]
   item.description=data["description"] if "description" in data else None
   item.link=data["link"] if "link" in data else None
   item.purchased=data["purchased"]
   item.sort_order=data["sort_order"]

   db.session.commit()

   return {"msg": "Item was updated"}, 200

@wishlist_controller.delete("/<int:item_id>")
def delete_item(item_id):
   item = db.session.get(WishlistItem, item_id)

   if item is None:
      return {"msg": f"There is no item with id {item_id}"}, 404
   
   db.session.delete(item)
   db.session.commit()

   return {"msg": "Item deleted from the database"}, 200