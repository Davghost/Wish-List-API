from flask import Blueprint, jsonify
from factory import db, api
from model.wishlist_item import WishlistItem
from flask.globals import request
from sqlalchemy import select
from spectree import Response
from schemas.wishlist_item import DefaultResponse, WishlistItemCreate, OrmBase, WishlistItemUpdate, WishListItems, WishlistItemResponse
from flask_jwt_extended import jwt_required

wishlist_controller = Blueprint("wishlist_controller", __name__, url_prefix="/wishlist")

@wishlist_controller.get("/<int:item_id>")
@api.validate(resp=Response(HTTP_200=WishlistItemResponse, HTTP_404=DefaultResponse), tags=["items"])
@jwt_required()
def get_item(item_id):
   """
   Get a specified item
   """
   item = db.session.get(WishlistItem, item_id)

   if item is None:
      return f"There is no item with id {item_id}", 404

   response = WishlistItemResponse.model_validate(item).model_dump()
   
   return response,200

@wishlist_controller.get("/")
@api.validate(resp=Response(HTTP_200=WishListItems), tags=["items"])
@jwt_required()
def get_items():
   """
   Get all items
   """
   items = db.session.scalars(select(WishlistItem)).all()

   response = WishListItems(
      items=[WishlistItemResponse.model_validate(item).model_dump() for item in items]
   ).model_dump()
   return response, 200

@wishlist_controller.post("/")
@api.validate(json=WishlistItemCreate, resp=Response(HTTP_201=DefaultResponse), tags=["items"])
@jwt_required()
def post_item():
   """
   Create an item
   """
   data = request.json

   if db.session.scalar(select(WishlistItem).filter_by(name=data["name"])):
      return {"msg": "item's name not available"}, 409
   
   item = WishlistItem(
      name=data["name"],
      description=data["description"] if "description" in data else None,
      link=data["link"] if "link" in data else None,
      purchased=data["purchased"],
      sort_order=data["sort_order"] if "sort_order" in data else None
   )

   db.session.add(item)
   db.session.commit()

   return{
      "id": item.id,
      "msg": "Item created successfully."
      }, 201

@wishlist_controller.put("/<int:item_id>")
@api.validate(json=WishlistItemUpdate ,resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["items"])
@jwt_required()
def put_item(item_id):
   """
   Updated an item
   """
   item = db.session.get(WishlistItem, item_id)

   if item is None:
      return {"msg": f"There is no item with id {item_id}"}, 404
   
   data = request.json

   item.name=data["name"]
   item.description=data["description"] if "description" in data else None
   item.link=data["link"] if "link" in data else None
   item.purchased=data["purchased"]
   item.sort_order=data["sort_order"] if "sort_order" in data else None

   db.session.commit()

   return {"msg": "Item was updated"}, 200

@wishlist_controller.delete("/<int:item_id>")
@api.validate(resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["items"])
@jwt_required()
def delete_item(item_id):
   """
   Delete an item
   """
   item = db.session.get(WishlistItem, item_id)

   if item is None:
      return {"msg": f"There is no item with id {item_id}"}, 404
   
   db.session.delete(item)
   db.session.commit()

   return {"msg": "Item deleted from the database"}, 200