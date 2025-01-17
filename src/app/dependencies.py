from fastapi import HTTPException, Header, status

from .settings import AppSettings

app_settings = AppSettings()


async def verify_api_key(Authorization: str = Header()):
    print(Authorization)
    if Authorization != app_settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )