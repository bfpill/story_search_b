import base64
import json
from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from pinecone import Pinecone

import firebase_admin
from firebase_admin import credentials, auth

load_dotenv()


class Settings(BaseSettings):
  secret_key: str = "SECRET_KEY NOT SET"
  openai_api_key: str = "OPENAI_API_KEY NOT SET"
  email_pass: str = "EMAIL_PASS NOT SET"
  email_user: str = "EMAIL_USER NOT SET"
  firebase_credentials_base64: str = "FIREBASE CRED NOT SET"
  firebase_database_url: str = "FIREBASE_DATABASE_URL"
  master_password: str = "MASTER PASS NOT SET"
  pinecone_api_key: str = "PINECONE_API_KEY NOT SET" 

  production: bool = False
  logger_file: str = 'surv.log'
  temp_files: str = '/tmp/surv/tmp'

  class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'

settings = Settings()
client = AsyncOpenAI(api_key=settings.openai_api_key)

pc_key = settings.pinecone_api_key

firebase_credentials_json = base64.b64decode(settings.firebase_credentials_base64)
firebase_credentials = json.loads(firebase_credentials_json)

cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred,  {'storageBucket': 'baggetters-38a7c.appspot.com', 
                                      'databaseURL': settings.firebase_database_url})

# def getFireabseApp():
#   return firebase_

def getOpenai():
  return client

def getPc():
  pc = Pinecone(api_key=settings.pinecone_api_key)
  return pc

