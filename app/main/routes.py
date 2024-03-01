from fastapi import APIRouter, Depends, status, HTTPException, Header
from logging import getLogger
from app.main.settings import Settings
from app.main.types import *

router = APIRouter()
logger = getLogger()
settings = Settings()


@router.post('/api/send_email', tags=["Email"])
def test(req: Base):
    return True
  # except Exception as e:
  #   logger.error(f"Error sending email: {e}")
  #   raise HTTPException(detail=str(e),
  #              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
