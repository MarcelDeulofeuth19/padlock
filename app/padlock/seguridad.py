from fastapi import HTTPException, Request, status
from app.padlock.config import ALO_API_CLAVE


async def validar_api_key(request: Request) -> None:
    api_key = request.headers.get("alo-api-key")
    if not api_key or api_key != ALO_API_CLAVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key invalida.",
        )
