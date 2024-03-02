from fastapi import APIRouter, Depends, status, HTTPException, Header
from logging import getLogger
from app.main.settings import Settings
from app.main.types import *
from firebase_admin import db

router = APIRouter()
logger = getLogger()
settings = Settings()

def does_user_exist(user_id: str):
  user_ref = db.reference(f'/users/{user_id}')
  user_data = user_ref.get()
  if not user_data:
    return False
  return True

@router.get('/api/get_book/{user_id}/{book_id}', tags=["Book", "User"])
def get_book(user_id: int, book_id: int):
  try:
    if not does_user_exist(user_id):
      raise HTTPException(status_code=404, detail="User not found")

    user_books_ref = db.reference(f'/users/{user_id}/books')
    user_books = user_books_ref.get()
    
    if user_books:
      query = user_books_ref.order_by_key().equal_to(str(book_id))
      book = query.get()
      if book:
        return {"success": True, "book": book}
      else:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
      raise HTTPException(status_code=404, detail="Books not found")
  
  except Exception as e:
    logger.error(f"Error retrieving user books: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/api/set_book/{user_id}/{book_id}', tags=["Book", "User"])
def set_book(user_id: str, book_id: str, book: BookData):
  try:
    if not does_user_exist(user_id):
      raise HTTPException(status_code=404, detail="User not found")
    
    books_ref = db.reference(f'/users/{user_id}/books')
    books_ref.child(book_id).set(book.model_dump())
    return True

  except Exception as e:
    logger.error(f"Error setting book data: {e}")
    raise HTTPException(detail=str(e),
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


#create a new user
@router.post('/api/create_user/{user_id}', tags=["User"])
def create_user(user_id: int, user: User):
  try:
    # check if email already exists in /accounts/emails where email is key and user_id is value
    user_id_ref = db.reference(f'/accounts/id/{user_id}')
    user_data = user_id_ref.get()
    if user_data:
      raise HTTPException(status_code=400, detail="Email already exists")
    
    # create new user with user_id as key and email as value
    user_id_ref.set({"email": user.email})

    return True
  except Exception as e:
    logger.error(f"Error creating user: {e}")
    raise HTTPException(detail=str(e),
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/api/get_user/{user_id}', tags=["User"])
def get_user_id(user_id: int):
  try:
    acc_ref = db.reference(f'/accounts/id/{user_id}')
    account = acc_ref.get()
    if account:
      return {"user_id": account}
    else:
      raise HTTPException(status_code=404, detail="User not found")
  except Exception as e:
    logger.error(f"Error retrieving account: {e}")
    raise HTTPException(detail=str(e),
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
# email -> user_id 
  
# create user with email and username and new id given
