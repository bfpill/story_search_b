from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

class Base(BaseModel):
  empty: str
  
  
class GenerateBookRequest(BaseModel):
  search_query: str
  user_id: str
