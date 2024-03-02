import base64
import json
from logging import getLogger
import os
import uuid
from openai import AsyncOpenAI, OpenAI
from pinecone import ServerlessSpec
from app.main.types import *

from firebase_admin import firestore

db = firestore.client()
logger = getLogger()
client = AsyncOpenAI()

response_index_dims = 1536
form_index_dims= 1

def read_sections_store(form_id: str):
  map_ref = db.collection('forms').document(form_id).collection('cards').document(form_id)
  doc = map_ref.get()
  data = doc.to_dict()
  return data 

def write_sections_store(form_id: str, data) :
  map_ref = db.collection('forms').document(form_id).collection('cards').document(form_id)
  map_ref.set(data)
  return data 