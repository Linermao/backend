from core.database import get_collection
from core.config import config
from utils.handle_error import ErrorHandler
from pymongo.errors import PyMongoError
from models.user import UserInDB, Token, TokenData
from passlib.context import CryptContext
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from utils.jwt_utils import verify_password, create_access_token, verify_access_token
import jwt
from jwt.exceptions import InvalidTokenError

database_name = 'Authentication'
collection_name = 'users'

# 密码哈希配置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

async def get_user(username: str) -> UserInDB:
  try:
    collection = get_collection(database_name, collection_name)
    db_user = await collection.find_one({'username': username})

    if not db_user:
      ErrorHandler.handle_not_found_error(f"username: {username}")

    db_user['_id'] = str(db_user['_id'])
    return UserInDB(**db_user)

  except PyMongoError as e:
      ErrorHandler.handle_mongodb_error(e)
  except Exception as e:
      ErrorHandler.handle_unexpected_error(e)

async def authenticate_user(username, password) -> UserInDB:
  try:
    db_user = await get_user(username)
    
    if not db_user:
        ErrorHandler.handle_not_found_error(f"username: {username}")
    if not verify_password(password, db_user.hashed_password):
        ErrorHandler.handle_password_error()
    
    return db_user
  except PyMongoError as e:
      ErrorHandler.handle_mongodb_error(e)
  except Exception as e:
      ErrorHandler.handle_unexpected_error(e)

async def login_for_access_token(form_data: OAuth2PasswordRequestForm):
    """登录并获取 token"""
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
      # all error down   
      pass

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        username = payload.get("sub")

        if username is None:
            ErrorHandler.handle_not_found_error(f"username: {username}")

        return username
    except InvalidTokenError:
        ErrorHandler.handle_token_invaliable()
    

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        ErrorHandler.handle_not_found_error(f"username: {current_user.username}")
    return current_user
