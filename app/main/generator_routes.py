import json
from typing import Union
from fastapi import APIRouter, status, HTTPException 
from openai import OpenAI
from logging import getLogger
from app.main.image_routes import generate_background_image 
import asyncio
from PIL import Image
from uuid import uuid4

import requests
from io import BytesIO
from app.main.image_storage_handlers import store_image

from app.main.types import *
from app.main.data_handlers import *
from app.main.vdb_handlers import query_by_search, vdb_store_image

router = APIRouter()
client = OpenAI()
logger = getLogger()

def generate_book_json(query): 
  json_structure = {
        "title": "Funny Title",
        "pages": [
            {
                "pageNum": 1,
                "text": "Page 1 Text",
                "images": [
                    "Image One Title",
                    "Image Two Title",
                ],
                "background_image": "Trains"
            },
            {
                "pageNum": 2,
                "text": "Page 2 Text",
                "images": [
                    "Image One Title",
                    "Image Two Title",
                ],
                "background_image": "Trains"
            }
        ]
    }
 
  prompt = f'''
    Create a short story based on factual information about "{query}".
    The story should be engaging, with fictional 
    characters and a narrative that weaves in the factual information seamlessly.

    Format the story according to the following JSON structure, where each "page" 
    represents a page of the story, and "text" contains the content of each section.
    Include fictional images by specifying their hypothetical title,
    but ensure they relate to the content of the story. 
    The background image should be the same for pairs of pages, and just a simple word or two. 
    
    {str(json_structure)}
    Add more pages as needed, following the pattern above.
    
    The story should be roughly 40 words total, and 4 pages long. 
    
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

@router.post('/book', tags=["book"])
async def generate_book_request(req: GenerateBookRequest):
    
  print("generating a book")
  book_json = generate_book_json(req.search_query)

  # Add something here to get the books general color theme
  images = []
  for i, page in enumerate(book_json["pages"]): 
    if i % 2 == 0: 
      left_image_url, right_image_url = "", ""

      left_image_url, right_image_url = get_cached_backgrounds(page["background_image"])

      if not left_image_url and not right_image_url: 
        image_url = generate_background_image(page["background_image"], "blue")
        left_image_data, right_image_data = split_image(image_url)

        left_id, right_id = str(uuid4()), str(uuid4())

        left_image_url = store_image(left_id, left_image_data)
        right_image_url = store_image(right_id, right_image_data)

        vdb_store_image(page["background_image"], left_image_url, right_image_url)
      
      images.append(left_image_url)
      images.append(right_image_url)
    
  for page, image_url in zip(book_json["pages"], images):
    page["background_image_query"] = page["background_image"]
    page["background_image"] = image_url
    
  return book_json

def get_cached_backgrounds(query): 
  emb = query_by_search(query)
  if emb["matches"] and emb["matches"][0]["score"] > 0.9:
    if "metadata" in emb:
      left_url, right_url = emb["metadata"]["left_url"], emb["metadata"]["right_url"]
      return left_url, right_url

  return None, None


def split_image(url):
    response = requests.get(url)
    original_image = Image.open(BytesIO(response.content))

    width, height = original_image.size
    mid = width // 2

    left_half = original_image.crop((0, 0, mid, height))
    right_half = original_image.crop((mid, 0, width, height))

    left_bytes = BytesIO()
    right_bytes = BytesIO()
    left_half.save(left_bytes, format=original_image.format)
    right_half.save(right_bytes, format=original_image.format)

    return left_bytes.getvalue(), right_bytes.getvalue()

    


