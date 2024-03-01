import json
from typing import Union
from uuid import uuid4
from fastapi import APIRouter, status, HTTPException 
from openai import OpenAI
from logging import getLogger

from app.main.types import *
from app.main.data_handlers import *

router = APIRouter()
client = OpenAI()
logger = getLogger()

@router.post('/book', tags=["book"])
def generate_book_request(req: GenerateBookRequest):
  json_structure = {
        "title": "Funny Title",
        "pages": [
            {
                "pageNum": 1,
                "text": "Page 1 Text",
                "images": [
                    "Image One Title",
                    "Image Two Title",
                ]
            },
            {
                "pageNum": 2,
                "text": "Page 2 Text",
                "images": [
                    "Image One Title",
                    "Image Two Title",
                ]
            },
        ]
    }
 
  prompt = f'''
    Create a short story based on factual information about "{req.search_query}".
    The story should be engaging, with fictional 
    characters and a narrative that weaves in the factual information seamlessly.

    Format the story according to the following JSON structure, where each "page" 
    represents a page of the story, and "text" contains the content of each section.
    Include fictional images by specifying their hypothetical title,
    but ensure they relate to the content of the story:
    
    {str(json_structure)}
    Add more pages as needed, following the pattern above.
    
    The story should be roughly 100 words total, and 10 pages long. 
    
    '''
            
  completion = client.chat.completions.create(
    response_format={ "type": "json_object" },
    messages=[{ 
      "role": "system", 
      "content": prompt 
    }], 
    model="gpt-4-0125-preview",
  )
  
  book_json = completion.choices[0].message.content
  book = json.loads(book_json)
  print(book)
  
  print("finished book")
  
  return book 


