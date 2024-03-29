import base64
import json
from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from pinecone import Pinecone

import firebase_admin
from firebase_admin import credentials

load_dotenv()

class Settings(BaseSettings):
  secret_key: str = "SECRET_KEY NOT SET"
  openai_api_key: str = "OPENAI_API_KEY NOT SET"
  email_pass: str = "EMAIL_PASS NOT SET"
  email_user: str = "EMAIL_USER NOT SET"
  master_password: str = "MASTER PASS NOT SET"
  pinecone_api_key: str = "PINECONE_API_KEY NOT SET" 
  firebase_credentials_base64: str = "FIREBASE CRED NOT SET"

  production: bool = False
  logger_file: str = 'surv.log'
  temp_files: str = '/tmp/surv/tmp'

  class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'

settings = Settings()
client = AsyncOpenAI(api_key=settings.openai_api_key)

pc_key = settings.pinecone_api_key

cred = credentials.Certificate("app/firebase_config/firebase_cred.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'storysearch2.appspot.com'})

# firebase_credentials = json.loads(firebase_credentials_json)

# cred = credentials.Certificate(firebase_credentials)
# firebase_admin.initialize_app(cred,  {'storageBucket': 'storysearch2.appspot.com'})

# def getFireabseApp():
#   return firebase_

def getOpenai():
  return client

def getPc():
  pc = Pinecone(api_key=settings.pinecone_api_key)
  return pc

