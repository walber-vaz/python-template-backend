from datetime import datetime, timedelta
from typing import Any, Dict
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

from app.config import settings

pwd_context = PasswordHash.recommended()


def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(ZoneInfo('UTC')) + timedelta(
        days=settings.JWT_EXPIRATION
    )
    to_encode.update({
        'exp': expire,
        'iss': settings.JWT_ISSUER,
        'aud': settings.JWT_AUDIENCE,
    })

    return encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    ).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
