
from logging import getLogger
from typing import List
from uuid import uuid4
from openai import AsyncOpenAI, OpenAI
from app.main import settings
from app.main.settings import getPc
from pinecone import ServerlessSpec
from app.main.settings import getOpenai

client = getOpenai()

backgrounds_index_name = "backgrounds"
story_index_name = "books"

pc = getPc()
logger = getLogger()

async def vdb_store_image(imageTitle, left_url, right_url):
  vector = await create_vector(imageTitle)
  print("got vector")

  store_embed(backgrounds_index_name, str(uuid4()), left_url=left_url, right_url=right_url, vector=vector)
  print("stored embed")

### Check function below  
async def vdb_store_story(query, text):
  vector = await create_vector(query)
  
  if "book" not in pc.list_indexes().names():
    create_index(index_name="books", dims="1536")

  print(vector)
  index = pc.Index("books")
  vec = [{"id": str(uuid4()), "values": vector, "metadata": {"story": text}}]
  res = index.upsert(
    vectors=vec
  )

  print("resd", res)
  return
  
# this will not work if we call immediately after writing to vector, pinecone has a significant sync time
def get_embedding(index_name: str, emb_id: str, namespace: str = ""): 
  index = pc.Index(index_name)
  
  print("getting embedding") 
  return index.fetch(
    ids=[emb_id], 
    namespace=namespace
  ) 

async def query_by_search(query: str): 
  query_vector = await create_vector(query)
  index = pc.Index(backgrounds_index_name)
  
  print("querying embedding") 

  return index.query(
    vector=query_vector,
    top_k=1,
    include_values=True, 
    include_metadata=True
  )

async def query_by_search_story(query: str):
  query_vector = await create_vector(query)
  index = pc.Index(story_index_name)
  
  print("querying embedding") 

  return index.query(
    vector=query_vector,
    top_k=1,
    include_values=True, 
    include_metadata=True
  )
    
async def create_vector(data): 
  if data: 
    response = await client.embeddings.create(
      input = [data], 
      model = "text-embedding-ada-002"
    )

    vector = response.data[0].embedding

    return vector
  else: 
    print("No form reponse")
    return False

def store_embed(index_name: str, vector_id: str, left_url: str, right_url: str, vector: List): 
  if index_name not in pc.list_indexes().names():
    create_index(index_name=index_name, dims="1536")

  index = pc.Index(index_name)
  vec = [{"id": vector_id, "values": vector, "metadata": {"left_id": left_url, "right_id": right_url }}]
  index.upsert(
    vectors=vec
  )
  
  print("upserted vector")

### Check function below 
def store_embed_story(index_name: str, vector_id: str, text: str, vector: List): 
  if index_name not in pc.list_indexes().names():
    create_index(index_name="books", dims="1536")

  print(vector)
  index = pc.Index("books")
  vec = [{"id": vector_id, "values": vector, "metadata": {"story": text}}]
  index.upsert(
    vectors=vec
  )
  
  print("upserted embed vector")
  
def create_index(index_name: str, dims: int): 
  try:
    pc.create_index(
      name=index_name,
      dimension=dims,
      metric="euclidean",
      spec=ServerlessSpec(
        cloud="aws",
        region="us-west-2"
      )
    )
  except:
    logger.error("Could not create index %s", index_name)