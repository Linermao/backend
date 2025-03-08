import base64
from utils.handle_error import ErrorHandler

def decode_base64(text: str) -> str:
    return base64.b64decode(text).decode('utf-8')

def encode_base64(text: str) -> str:
    try:
      return base64.b64encode(text.encode("utf-8")).decode("utf-8")
    except base64.binascii.Error:
      ErrorHandler.handle_base64_error()