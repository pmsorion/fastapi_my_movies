from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from jwt_manager import create_token, validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(
                status_code=403,
                detail="No autorizado",
                headers={"WWW-Authenticate": "Bearer"}
            )