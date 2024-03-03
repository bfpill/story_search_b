from logging import getLogger
from fastapi import APIRouter
from openai import AsyncOpenAI, OpenAI
import asyncio
from app.main.settings import getOpenai


from app.main.types import GenerateBackgroundImageReq
router = APIRouter()
client = getOpenai()
logger = getLogger()


async def generate_background_image(query, color):
  prompt = f"Generate a mostly {color} watercolor pastel childrens book background image, landscape, low detail, \n."
  prompt += f"The picture should be of a {query}"

  print("genning image, ", prompt)
  response = await client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",
    quality="standard",
    n=1,
  )

  image_url = response.data[0].url
  
  print(image_url)
  
  return image_url

@router.post('/bg_image', tags=["Email"])
async def handle_generate_background_image(req: GenerateBackgroundImageReq):
  image_url = await generate_background_image(req.search_query, req.color)
 