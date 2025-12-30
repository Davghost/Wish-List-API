from pydantic import BaseModel, ConfigDict
from typing import Optional

class OrmBase(BaseModel):
   model_config = ConfigDict(from_attributes=True)

class WishlistItemCreate(OrmBase):
   name: str
   description: Optional[str]
   link: Optional[str]
   purchased: Optional[bool]
   sort_order: Optional[int]

class WishlistItemResponse(OrmBase):
   id: str
   name: str
   description: Optional[str]
   link: Optional[str]
   purchased: Optional[bool]
   sort_order: Optional[int]

class WishlistItemUpdate(BaseModel):
   name: str
   description: Optional[str]
   link: Optional[str]
   purchased: Optional[bool]
   sort_order: Optional[int]

class WishListItems(BaseModel):
   items: list[WishlistItemResponse]

class DefaultResponse(BaseModel):
   id: int
   msg: str