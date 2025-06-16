from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.session import get_async_session
from app.exceptions.user_exception import UserNotAuthenticated
from app.repository import user_repository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_PREFIX}/auth/login'
)


async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )
        sub_user_id = payload.get('sub')

        if not sub_user_id:
            raise UserNotAuthenticated
    except DecodeError:
        raise UserNotAuthenticated

    user = await user_repository.get_user_by_id(
        user_id=sub_user_id, session=session
    )

    if not user:
        raise UserNotAuthenticated

    return user
