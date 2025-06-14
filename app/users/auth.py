from datetime import datetime, timedelta, UTC
from jose import jwt
from app.users.hashing import verify_password
from app.users.service import UsersService
from app.config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt

async def authenticate_user(username: str, password: str):
    user = await UsersService.find_one_or_none(username=username)
    if not user or not verify_password(password, user.hash_password):
        return None
    return user