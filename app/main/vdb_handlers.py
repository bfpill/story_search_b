
from logging import getLogger
from typing import List
from uuid import uuid4
from openai import OpenAI
from app.main.settings import getPc
from pinecone import ServerlessSpec
client = OpenAI()

backgrounds_index_name = "backgrounds"
pc = getPc()
logger = getLogger()

def vdb_store_image(imageTitle, left_url, right_url):
  vector = create_vector(imageTitle)
  print("got vector")

  store_embed(backgrounds_index_name, str(uuid4()), left_url=left_url, right_url=right_url, vector=vector)
  print("stored embed")
  
# this will not work if we call immediately after writing to vector, pinecone has a significant sync time
def get_embedding(index_name: str, emb_id: str, namespace: str = ""): 
  index = pc.Index(index_name)
  
  print("getting embedding") 
  return index.fetch(
    ids=[emb_id], 
    namespace=namespace
  ) 

def query_by_search(query: str): 
  query_vector = create_vector(query)
  index = pc.Index(backgrounds_index_name)
  
  print("querying embedding") 

  return index.query(
    vector=query_vector,
    top_k=1,
    include_values=True, 
    include_metadata=True
  )
    
def create_vector(data): 
  if data: 
    response = client.embeddings.create(
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