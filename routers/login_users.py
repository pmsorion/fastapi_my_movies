from fastapi import APIRouter
from fastapi.responses import JSONResponse

from jwt_manager import create_token
from schemas.user import User

login_router = APIRouter()

@login_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin123":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)