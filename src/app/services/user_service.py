from http import HTTPStatus
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repository import user_repository
from app.schemas.response import Response
from app.schemas.user.user_input_create import UserCreate, UserResponse
from app.security import get_password_hash


async def store(
    user: UserCreate, session: AsyncSession
) -> Response[UserResponse]:
    user_model = User(
        email=user.email,
        password=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
    )

    user_created = await user_repository.create_user(user_model, session)

    return Response[UserResponse](
        data=UserResponse.model_validate(user_created),
        message='Usuário criado com sucesso.',
        status_code=HTTPStatus.CREATED.value,
    )


async def get_user_by_id(
    user_id: UUID, session: AsyncSession
) -> Response[UserResponse]:
    user = await user_repository.get_user_by_id(
        user_id=user_id, session=session
    )

    if not user:
        return Response[UserResponse](
            data=None,
            message='Usuário não encontrado.',
            status_code=HTTPStatus.NOT_FOUND.value,
        )

    return Response[UserResponse](
        data=UserResponse.model_validate(user),
        message='Usuário encontrado.',
        status_code=HTTPStatus.OK.value,
    )
