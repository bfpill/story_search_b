import json
from typing import Union
from fastapi import APIRouter, status, HTTPException 
from openai import AsyncOpenAI, OpenAI
from logging import getLogger
from app.main.settings import getOpenai
from app.main.image_routes import generate_background_image 
import asyncio
from PIL import Image
from uuid import uuid4

import requests
from io import BytesIO
from app.main.image_storage_handlers import store_image 

from app.main.types import *
from app.main.data_handlers import *
from app.main.utils import get_random_pastel_color
from app.main.vdb_handlers import query_by_search, query_by_search_story, vdb_store_image, vdb_store_story

router = APIRouter()
client = getOpenai()
logger = getLogger()

@router.post('/search', tags=["book"])
async def generate_search_options(req: GenerateSearchOptionsReq): 
  json_structure = {"titles": [
    "Possible Title 1",
    "Possible Title 2",
    "Possible Title 3",
    ]}
 
  prompt = f'''
    Create 3 possible titles for a childrens book about {req.search_query}".
    Ouput the possible titles as a JSON array of strings. \n
    {str(json_structure)}
    '''
            
  completion = await client.chat.completions.create(
    response_format={ "type": "json_object" },
    messages=[{ 
      "role": "system", 
      "content": prompt 
    }], 
    model="gpt-4-0125-preview",
  )
  
  titles_json = completion.choices[0].message.content
  titles = json.loads(titles_json)
  
  print("titles", titles)
  
  return titles 

async def generate_book_json(query, title): 
  json_structure = {
        "title": "Funny Title",
        "category": "ie Science, Animals, Vehicles, etc",
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
    The title of the story is "{title}"
    The story should be engaging, with fictional 
    characters and a narrative that weaves in the factual information seamlessly.

    Format the story according to the following JSON structure, where each "page" 
    represents a page of the story, and "text" contains the content of each section.
    Include fictional images by specifying their hypothetical title,
    but ensure they relate to the content of the story. 
    The background image covers two pages. It should be relavant to the text on the 2 pages, and describe the scene well. 
    
    {str(json_structure)}
    Add more pages as needed, following the pattern above.
    
    The story should be roughly 80 words total, and 8 pages long. 
    
    '''
            
  completion = await client.chat.completions.create(
    response_format={ "type": "json_object" },
    messages=[{ 
      "role": "system", 
      "content": prompt 
    }], 
    model="gpt-4-0125-preview",
  )
  
  book_json = completion.choices[0].message.content
  book = json.loads(book_json)

  book["color"] = get_random_pastel_color()
  book["complementary_color"] = get_random_pastel_color()

  print(book)
  
  print("finished book")
  
  return book 

@router.post('/book', tags=["book"])
async def generate_book_request(req: GenerateBookRequest):
  print("generating a book")

  book_json = await generate_book_json(req.search_query, req.title)
  # cached_story = await get_cached_story(req.search_query)
  # print("BOOK_URL", cached_story)
  # if not cached_story: 
  text = " ".join([page["text"] for page in book_json["pages"]])
  
  await vdb_store_story(req.search_query, text)

  images = []
  for i, page in enumerate(book_json["pages"]): 
    if i % 2 == 0: 
      left_image_url, right_image_url = "", ""

      left_image_url, right_image_url = await get_cached_backgrounds(page["background_image"])

      if not left_image_url and not right_image_url: 
        image_url = await generate_background_image(page["background_image"], book_json["color"])
        left_image_data, right_image_data = split_image(image_url)

        left_id, right_id = str(uuid4()), str(uuid4())

        left_image_url = store_image(left_id, left_image_data)
        right_image_url = store_image(right_id, right_image_data)

        await vdb_store_image(page["background_image"], left_image_url, right_image_url)
      
      images.append(left_image_url)
      images.append(right_image_url)
    
  for page, image_url in zip(book_json["pages"], images):
    page["background_image_query"] = page["background_image"]
    page["background_image"] = image_url
    
  return book_json

async def get_cached_backgrounds(query): 
  emb = await query_by_search(query)

  matches = emb["matches"]
  
  if not matches: 
    return None, None

  match = matches[0]
  if match and match["score"] > 0.98:
    print("EMB", emb["matches"][0]['score'])
    if "metadata" in match:
      print("GOT EXISTING IMAGE")
      left_url, right_url = match["metadata"]["left_id"], match["metadata"]["right_id"]
      return left_url, right_url

  return None, None

async def get_cached_story(query):
  emb = await query_by_search_story(query)

  matches = emb["matches"]
  
  if not matches: 
    return

  match = matches[0]
  
  if match and "score" in match and match["score"] > 0.91:
    if "metadata" in match:
      print("EMB", emb["matches"][0]['score'])
      print("GOT EXISTING STORY")
      return match["metadata"]["story"]


def split_image(url):
  response = requests.get(url)
  original_image = Image.open(BytesIO(response.content))

  width, height = original_image.size
  mid = width // 2

  # New dimensions based on 8:6 ratio
  target_width = (height * 8) // 6

  if target_width > width:
      target_width = width
      target_height = (target_width * 6) // 8
  else:
      target_height = height

  left_edge = (width - target_width) // 2
  top_edge = (height - target_height) // 2

  cropped_image = original_image.crop((left_edge, top_edge, left_edge + target_width, top_edge + target_height))

  mid_point = target_width // 2
  left_half = cropped_image.crop((0, 0, mid_point, height))
  right_half = cropped_image.crop((mid_point, 0, target_width, height))

  left_bytes = BytesIO()
  right_bytes = BytesIO()
  left_half.save(left_bytes, format=original_image.format)
  right_half.save(right_bytes, format=original_image.format)

  return left_bytes.getvalue(), right_bytes.getvalue()

    


