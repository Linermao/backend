from fastapi import APIRouter, Depends
from models.user import Token, UserInDB
from services.user_service import login_for_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post('/login', response_model=Token)
async def login_for_access_token_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
  return await login_for_access_token(form_data)

@router.get('/verify_token', response_model=str)
async def post_token_for_verify(current_username: str = Depends(get_current_user)):
  return current_username