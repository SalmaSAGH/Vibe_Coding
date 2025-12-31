from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config.settings import get_settings

settings = get_settings()
api_key_header = APIKeyHeader(name=settings.api_key_header, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key from header"""
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key missing"
        )
    
    if api_key not in settings.api_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return api_key
