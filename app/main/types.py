from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

class Base(BaseModel):
  empty: str

class SetBookReq(BaseModel):
  book: Dict
  
class GenerateBookRequest(BaseModel):
  search_query: str
  user_id: str
  title: str
  
class GenerateSearchOptionsReq(BaseModel):
  search_query: str

class UpdateUserReq(BaseModel):
  new_data: Any

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
  category: str
  
  
class GenerateBackgroundImageReq(GenerateBookRequest): 
  color: str
  

class User(BaseModel):
  email: str
