from pydantic import BaseModel


class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str | None = None

class UserInDB(BaseModel):
  _id: str | None = None
  username: str
  email: str | None = None
  disabled: str | None = None
  hashed_password: str