from pydantic import BaseModel, ConfigDict
from typing import Optional

class OrmBase(BaseModel):
   id: int
   model_config = ConfigDict(from_attributes=True)

class WishlistItemCreate(OrmBase):
   name: str
   description: Optional[str]
   link: Optional[str]
   purchased: bool
   sort_order: Optional[int]

class WishlistItemResponse(OrmBase):
   name: str
   description: Optional[str]
   link: Optional[str]
   purchased: bool
   sort_order: Optional[int]

class WishlistItemUpdate(BaseModel):
   name: str
   description: Optional[str]
   link: Optional[str]
   purchased: Optional[bool]
   sort_order: Optional[int]

class WishListItems(BaseModel):
   items: list[WishlistItemCreate]

class DefaultResponse(BaseModel):
   id: int
   msg: str