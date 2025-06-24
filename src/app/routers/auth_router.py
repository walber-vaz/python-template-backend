from http import HTTPStatus
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.routers.deps import get_auth_service, get_current_user
from app.schemas.response import Response
from app.schemas.user.user_input_create import UserResponse
from app.schemas.user.user_login_input import UserLoginInput, UserLoginResponse
from app.services.auth import IAuthServiceInterface

AuthService = Annotated[IAuthServiceInterface, Depends(get_auth_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter(prefix='/auth')


@router.post(
    '/login',
    response_model=UserLoginResponse,
    status_code=HTTPStatus.OK,
    summary='User login',
    description='This endpoint allows users to log in to the system using their email and password.',  # noqa: E501
    responses={
        HTTPStatus.OK.value: {
            'model': UserLoginResponse,
            'description': 'Login successful. Returns an access token.',
        },
        HTTPStatus.UNAUTHORIZED.value: {
            'model': Response[Any],
            'description': 'Invalid email or password.',
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            'model': Response[Any],
            'description': 'An unexpected error occurred. Please try again later.',  # noqa: E501
        },
        HTTPStatus.BAD_REQUEST.value: {
            'model': Response[Any],
            'description': 'Bad request. Please check the input data.',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            'model': Response[Any],
            'description': 'Validation error. Please check the input data.',
        },
    },
)
async def user_login(
    auth_service: AuthService,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> UserLoginResponse:
    login_input = UserLoginInput(
        email=form_data.username, password=form_data.password
    )
    return await auth_service.login(
        login_input=login_input,
    )


@router.get(
    '/me',
    response_model=Response[UserResponse],
    status_code=HTTPStatus.OK,
    summary='Get current user',
    description='This endpoint retrieves the currently authenticated user.',
    responses={
        HTTPStatus.OK.value: {
            'model': Response[UserResponse],
            'description': 'User found successfully.',
        },
        HTTPStatus.UNAUTHORIZED.value: {
            'model': Response[Any],
            'description': 'User not authenticated.',
        },
    },
)
async def get_me(current_user: CurrentUser) -> Response[UserResponse]:
    return Response[UserResponse](
        data=UserResponse.model_validate(current_user),
        message='Usuário encontrado.',
        status_code=HTTPStatus.OK.value,
    )
