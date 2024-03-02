from fastapi import APIRouter, Depends, status, HTTPException, Header
from logging import getLogger
from app.main.settings import Settings
from app.main.types import *
from firebase_admin import db

router = APIRouter()
logger = getLogger()
settings = Settings()


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
    books_ref.child(book_id).set(book.dict())
    return True

  except Exception as e:
    logger.error(f"Error setting book data: {e}")
    raise HTTPException(detail=str(e),
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def does_user_exist(user_id: str):
  user_ref = db.reference(f'/users/{user_id}')
  user_data = user_ref.get()
  if not user_data:
    return False
  return True