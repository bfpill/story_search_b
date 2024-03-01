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
  

@router.post('/api/persona', tags=["persona"])
def generate_persona_from_responses(req: Base, content = "full", curr_persona={}):
  
  summaries = []

  prompt = '''
    Task Overview:

    You will be provided with a dataset containing responses to a customer experience survey. Your task is to analyze the survey responses, identify common themes and characteristics among the participants, and synthesize this information into a single, representative user persona. This persona should encapsulate the shared attributes, needs, and behaviors of the survey respondents.
    Read the data and then follow the instructions.
  '''
            
  completion = client.chat.completions.create(
    response_format={ "type": "json_object" },
    messages=[{ 
      "role": "system", 
      "content": prompt 
    }], 
    model="gpt-4-0125-preview",
  )

  persona_json = completion.choices[0].message.content
  persona = json.loads(persona_json)


