import base64
import json
from openai import OpenAI
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

import firebase_admin
from firebase_admin import credentials, auth

load_dotenv()


class Settings(BaseSettings):
  secret_key: str = os.environ.get("SECRET_KEY")
  openai_api_key: str = os.environ.get("OPENAI_API_KEY")
  email_pass: str = os.environ.get("EMAIL_PASS")
  email_user: str = os.environ.get("EMAIL_USER")
  firebase_credentials_base64: str = os.environ.get("FIREBASE_CREDENTIALS_BASE64")
  master_password: str = os.environ.get("MASTER_PASSWORD")
  firebase_database_url: str = os.environ.get("FIREBASE_DATABASE_URL")

  production: bool = False
  logger_file: str = 'surv.log'
  temp_files: str = '/tmp/surv/tmp'

  class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'

settings = Settings()
client = OpenAI(api_key=settings.openai_api_key)


firebase_credentials_json = base64.b64decode(settings.firebase_credentials_base64)
firebase_credentials = json.loads(firebase_credentials_json)

cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred, {
  'databaseURL': settings.firebase_database_url
})

# def getFireabseApp():
#   return firebase_

def getOpenai():
  return client

