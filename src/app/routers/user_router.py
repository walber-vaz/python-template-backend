from http import HTTPStatus
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.schemas.response import Response
from app.schemas.user.user_input_create import UserCreate, UserResponse
from app.services import user_service

Session = Annotated[AsyncSession, Depends(get_async_session)]
router = APIRouter(
    prefix='/users',
)


@router.post(
    '',
    response_model=Response[UserResponse],
    status_code=HTTPStatus.CREATED,
    summary='Create a new user',
    description='This endpoint allows you to create a new user in the system. '
    "You need to provide the user's email, password, first name, last name, and optionally a phone number.",  # noqa: E501
    responses={
        HTTPStatus.CREATED.value: {
            'model': Response[UserResponse],
            'description': 'User created successfully.',
        },
        HTTPStatus.BAD_REQUEST.value: {
            'model': Response[Any],
            'description': 'Invalid input data. Please check the provided information.',  # noqa: E501
        },
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            'model': Response[Any],
            'description': 'Invalid input data. Please check the provided information.',  # noqa: E501
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            'model': Response[Any],
            'description': 'An unexpected error occurred. Please try again later.',  # noqa: E501
        },
        HTTPStatus.CONFLICT.value: {
            'model': Response[Any],
            'description': 'Email already exists. Please use a different email address or phone number.',  # noqa: E501
        },
    },
)
async def create_user(
    user: UserCreate, session: Session
) -> Response[UserResponse]:
    return await user_service.store(user, session)
