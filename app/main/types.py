from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

class Base(BaseModel):
  empty: str
  
  
class GenerateBookRequest(BaseModel):
  search_query: str
  user_id: str


class CreateUserRequest(BaseModel):
  username: str
  email: str


class ImagePosition(BaseModel):
  x: int
  y: int


class Image(BaseModel):
  src: str
  position: Optional[ImagePosition]


class Page(BaseModel):
  pageNum: int
  text: str
  images: List[Image]


class Book(BaseModel):
  title: str
  pages: List[Page]


class SaveBookRequest(BaseModel):
  user_id: str
  book: Book