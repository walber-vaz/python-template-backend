from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.session import get_async_session
from app.exceptions.user_exception import UserNotAuthenticated
from app.repository.user import IUserRepositoryInterface, user_repository
from app.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.services.auth import AuthService, IAuthServiceInterface
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_PREFIX}/auth/login'
)
Session = Annotated[AsyncSession, Depends(get_async_session)]


def get_user_repository(session: Session) -> IUserRepositoryInterface:
    return user_repository.UserRepository(session=session)


def get_user_service(
    user_repository: Annotated[
        IUserRepositoryInterface, Depends(get_user_repository)
    ],
) -> UserService:
    return UserService(
        user_repository=user_repository, password_hasher=get_password_hash
    )


def get_auth_service(
    user_repository: Annotated[
        IUserRepositoryInterface, Depends(get_user_repository)
    ],
) -> IAuthServiceInterface:
    """Factory para serviço de autenticação"""
    return AuthService(
        user_repository=user_repository,
        password_verifier=verify_password,
        token_creator=create_access_token,
    )


async def get_current_user(
    user_repository: Annotated[
        IUserRepositoryInterface, Depends(get_user_repository)
    ],
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
            raise UserNotAuthenticated()

        try:
            user_id = (
                UUID(sub_user_id)
                if isinstance(sub_user_id, str)
                else sub_user_id
            )
        except ValueError:
            raise UserNotAuthenticated()
    except DecodeError:
        raise UserNotAuthenticated()

    user = await user_repository.get_by_id(user_id)

    if not user:
        raise UserNotAuthenticated()

    return user
