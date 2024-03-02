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


class Page(BaseModel):
  pageNum: int
  text: str
  images: List[str]


class BookData(BaseModel):
  title: str
  pages: List[Page]
  
  
class GenerateBackgroundImageReq(GenerateBookRequest): 
  color: str


class User(BaseModel):
  email: str
