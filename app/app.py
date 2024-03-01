from uuid import uuid4
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from logging import getLogger
from app.logconfig import setup_rich_logger
from app.main import generator_routes, routes
from app.main.settings import Settings, settings
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException
from firebase_admin import auth

def get_app() -> FastAPI:
  app = FastAPI(
    description="Surv Backend", version="0.0.1",
    # TODO: get servers from passed in cmd line / env var
    # servers=[
    #   {"url": "https://verveguy.ngrok.app", "description": "Personal laptop"},
    # ]
  )
  setup_rich_logger()
  return app

app = get_app()

logger = getLogger()

origins = [
  "http://localhost:*",
  "https://localhost:*",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["*"],
)

NO_AUTH_NEEDED = [
    "/api/waitlist",        
    "/usage",  
    "/demo_auth"
]

app.include_router(routes.router)
app.include_router(generator_routes.router)
settings = Settings()

# user_info = request.state.user
@app.middleware("http")
async def firebase_auth_middleware(request: Request, call_next):

  # if request.url.path in NO_AUTH_NEEDED or request.method == "OPTIONS":
        # return await call_next(request)

  # try:
  #     authorization: str = request.headers.get("Authorization")
  #     if not authorization:
  #         raise HTTPException(status_code=401, detail="Authorization header is missing")

  #     scheme, token = authorization.split()
  #     if scheme.lower() != 'bearer':
  #         raise HTTPException(status_code=401, detail="Invalid authentication scheme")
  #     if token != settings.master_password:
  #         decoded_token = auth.verify_id_token(token)
  #         request.state.user = decoded_token

  # except Exception as e:
  #     raise HTTPException(status_code=403, detail=f"Invalid authentication token: {str(e)}")

  return await call_next(request)

# @app.get("/demo_auth", response_class=HTMLResponse, tags=["Usage"])
# async def get_demo_auth():
#   try:
#     uid = str(uuid4())
#     custom_token = auth.create_custom_token(uid)
#     token_str = custom_token.decode() if isinstance(custom_token, bytes) else custom_token
#     print("custom_token", token_str)
#     return JSONResponse(content={"token": token_str})
  
#   except Exception as e:
#     raise HTTPException(status_code=403, detail=f"Invalid authentication token: {str(e)}")
     

@app.get("/", response_class=HTMLResponse, tags=["Usage"])
@app.get("/usage", response_class=HTMLResponse)
async def usage():
  return """<html>
  Surv service is running.
  See the none existent documentation
  </html>
  """
