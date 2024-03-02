from fastapi import APIRouter, Depends, status, HTTPException, Header
from logging import getLogger
from app.main.settings import Settings
from app.main.types import *
from firebase_admin import db

router = APIRouter()
logger = getLogger()
settings = Settings()


# @router.post('/api/send_email', tags=["Email"])
# def test(req: Base):
#   return True
#   # except Exception as e:
#   #   logger.error(f"Error sending email: {e}")
#   #   raise HTTPException(detail=str(e),
#   #              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# push sample book data to firebase
@router.post('/api/save_book', tags=["Book", "User"])
def save_book(req: SaveBookRequest):
  try:
    if not does_user_exist(req.user_id):
      raise HTTPException(status_code=404, detail="User not found")

    book = req.book.dict()
    user_books_ref = db.reference(f'/users/{req.user_id}/books')
    user_books_ref.push(book)

    return True

  except Exception as e:
    logger.error(f"Error saving book data: {e}")
    raise HTTPException(detail=str(e),
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# get all books for a user
@router.get('/api/get_books/{user_id}', tags=["Book", "User"])
def get_all_books(user_id: str):
  try:
    if not does_user_exist(user_id):
      raise HTTPException(status_code=404, detail="User not found")

    # Get a database reference to the 'users' node.
    user_books_ref = db.reference(f'/users/{user_id}/books')
    user_books = user_books_ref.get()

    if user_books:
      # Return the user data
      return {"success": True, "books": user_books}
    else:
      raise HTTPException(status_code=404, detail="Books not found")
  
  except Exception as e:
    logger.error(f"Error retrieving user books: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
  

# get book data from id
@router.get('/api/get_book/{user_id}/{book_id}', tags=["Book", "User"])
def get_book(user_id: str, book_id: str):
  try:
    if not does_user_exist(user_id):
      raise HTTPException(status_code=404, detail="User not found")

    # Get a database reference to the 'users' node.
    user_books_ref = db.reference(f'/users/{user_id}/books')
    user_books = user_books_ref.get()

    if user_books:
      # Find the book with the specified id
      book = next((book for book in user_books if book["book_id"] == book_id), None)
      if book:
        # Return the book data
        return {"success": True, "book": book}
      else:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
      raise HTTPException(status_code=404, detail="Books not found")
  
  except Exception as e:
    logger.error(f"Error retrieving user books: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  

def does_user_exist(user_id: str):
  user_ref = db.reference(f'/users/{user_id}')
  user_data = user_ref.get()
  if not user_data:
    return False
  return True