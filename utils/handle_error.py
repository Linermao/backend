from fastapi import HTTPException
from pymongo.errors import PyMongoError

class ErrorHandler:
    @staticmethod
    def handle_base64_error() -> None:
        """处理 Base64 解码错误"""
        raise HTTPException(status_code=400, detail="Base64 decoding error: Invalid encoding")

    @staticmethod
    def handle_mongodb_error(e: PyMongoError) -> None:
        """处理 MongoDB 错误"""
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")

    @staticmethod
    def handle_not_found_error(resource: str) -> None:
        """处理资源未找到错误"""
        raise HTTPException(status_code=404, detail=f"{resource} not found")

    @staticmethod
    def handle_unexpected_error(e: Exception) -> None:
        """处理未知错误"""
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def handle_invalid_content_error() -> None:
        """处理无效内容格式错误"""
        raise HTTPException(status_code=400, detail="Invalid content format for Base64 decoding")

    @staticmethod
    def handle_network_error() -> None:
        """处理网络错误"""
        raise HTTPException(status_code=500, detail="Network error occurred")
    
    @staticmethod
    def handle_password_error() -> None:
        """处理用户密码错误"""
        raise HTTPException(status_code=401, detail="Error password")
    
    @staticmethod
    def handle_use_disabled_error(username) -> None:
        """处理用户封禁错误"""
        raise HTTPException(status_code=401, detail=f"This accound: {username} has been baned")
    
    @staticmethod
    def handle_token_invaliable() -> None:
        """处理token错误"""
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    @staticmethod
    def handle_token_timeout() -> None:
        """处理token错误"""
        raise HTTPException(status_code=401, detail="token timeout, please relogin")
    