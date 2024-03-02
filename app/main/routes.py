from fastapi import APIRouter, Depends, status, HTTPException, Header
from logging import getLogger
from app.main.settings import Settings
from app.main.types import *

from firebase_admin import firestore
db = firestore.client()

router = APIRouter()
logger = getLogger()
settings = Settings()

# def does_user_exist(email: str):

@router.get('/api/get_book/{email}/{book_id}', tags=["Book", "User"])
def get_book(email: str, book_id: int):

  email = email.replace('.', ',')
  
  try:
    # if not does_user_exist(email):
    #   raise HTTPException(status_code=404, detail="User not found")

    user_books_ref = db.reference(f'/users/{email}/books')
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

@router.post('/api/set_book/{email}/{book_id}', tags=["Book", "User"])
def set_book(req: SetBookReq, email: str, book_id: str):
  
  email = email.replace('.', ',')

  print(email, req.book)

  try:
    # if not does_user_exist(email):
    #   raise HTTPException(status_code=404, detail="User not found")
    
    user_books_doc_ref = db.collection(f'users/{email}/books').document(book_id)
    user_books_doc_ref.set(req.book)

    if req.book["category"]:
      category_books_doc_ref = db.collection(f'books/{req.book["category"]}/{book_id}').document(book_id)
      category_books_doc_ref.set(req.book)
    
    print("WROTE TO BOOK USER")
    return True

  except Exception as e:
    logger.error(f"Error setting book data: {e}")
    raise HTTPException(detail=str(e),
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


#create a new user
@router.post('/api/create_user/{email}', tags=["User"])
def create_user(email: str):

  email = email.replace(".", ",")

  try:
    email_id_ref = db.reference(f'/users/{email}')
    email_id_ref.set({"og_email": email})

    return True
  except Exception as e:
    logger.error(f"Error creating user: {e}")
    raise HTTPException(detail=str(e),
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

@router.get('/api/get_all_books', tags=["Book"])
def get_all_books():
  try:
    books_ref = db.reference(f'/books')
    books = books_ref.get()
    if books:
      return {"books": books}
    else:
      raise HTTPException(status_code=404, detail="Books not found")
  except Exception as e:
    logger.error(f"Error retrieving books: {e}")
    raise HTTPException(detail=str(e),
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  
@router.get('/api/get_all_user_books/{email}', tags=["Book"])
def get_all_user_books(email: str):
  try:
    user_books_ref = db.reference(f'/users/{email}/books')
    user_books = user_books_ref.get()
    if user_books:
      return {"books": user_books}
    else:
      raise HTTPException(status_code=404, detail="Books not found")
  except Exception as e:
    logger.error(f"Error retrieving user books: {e}")
    raise HTTPException(detail=str(e),
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
