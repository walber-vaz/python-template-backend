from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.user_exception import UserNotAuthenticated
from app.models import User
from app.repository import user_repository
from app.schemas.user.user_login_input import UserLoginInput, UserLoginResponse
from app.security import create_access_token, verify_password


async def login(
    login_input: UserLoginInput,
    session: AsyncSession,
) -> UserLoginResponse:
    user: User | None = await user_repository.get_user_by_email(
        email=login_input.email, session=session
    )

    if not user or not verify_password(login_input.password, user.password):
        raise UserNotAuthenticated

    access_token = create_access_token(
        data={'sub': str(user.id)},
    )

    return UserLoginResponse(access_token=access_token)
