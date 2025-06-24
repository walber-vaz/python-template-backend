from http import HTTPStatus
from typing import Protocol
from uuid import UUID

from app.models import User
from app.repository.user import IUserRepositoryInterface
from app.schemas.response import Response
from app.schemas.user.user_input_create import UserCreate, UserResponse
from app.security import get_password_hash
from app.services.user import IUserServiceInterface


class PasswordHasherProtocol(Protocol):
    """Protocol para hash de senhas"""

    def __call__(self, password: str) -> str: ...  # noqa: E704


class UserService(IUserServiceInterface):
    """Serviço de usuário com injeção de dependências"""

    def __init__(
        self,
        user_repository: IUserRepositoryInterface,
        password_hasher: PasswordHasherProtocol = get_password_hash,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def store(self, user: UserCreate) -> Response[UserResponse]:
        """Cria um novo usuário"""
        try:
            # Criar modelo do usuário
            user_model = User(
                email=user.email,
                password=self._password_hasher(user.password),
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
            )

            # Salvar no repositório
            user_created = await self._user_repository.create(user_model)

            return Response[UserResponse](
                data=UserResponse.model_validate(user_created),
                message='Usuário criado com sucesso.',
                status_code=HTTPStatus.CREATED.value,
            )

        except ValueError as e:
            return Response[UserResponse](
                data=None,
                message=str(e),
                status_code=HTTPStatus.BAD_REQUEST.value,
            )
        except Exception:
            return Response[UserResponse](
                data=None,
                message='Erro interno do servidor.',
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )

    async def get_user_by_id(self, user_id: UUID) -> Response[UserResponse]:
        """Busca usuário por ID"""
        try:
            user = await self._user_repository.get_by_id(user_id)

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

        except Exception:
            return Response[UserResponse](
                data=None,
                message='Erro interno do servidor.',
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )

    async def get_user_by_email(self, email: str) -> Response[UserResponse]:
        """Busca usuário por email"""
        try:
            user = await self._user_repository.get_by_email(email)

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

        except Exception:
            return Response[UserResponse](
                data=None,
                message='Erro interno do servidor.',
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )

    async def update_user(
        self, user_id: UUID, user_data: UserCreate
    ) -> Response[UserResponse]:
        """Atualiza um usuário"""
        try:
            # Verificar se usuário existe
            existing_user = await self._user_repository.get_by_id(user_id)
            if not existing_user:
                return Response[UserResponse](
                    data=None,
                    message='Usuário não encontrado.',
                    status_code=HTTPStatus.NOT_FOUND.value,
                )

            # Atualizar campos
            existing_user.email = user_data.email
            existing_user.first_name = user_data.first_name
            existing_user.last_name = user_data.last_name
            existing_user.phone = user_data.phone

            # Se senha foi fornecida, atualizar hash
            if user_data.password:
                existing_user.password = self._password_hasher(
                    user_data.password
                )

            # Salvar alterações
            updated_user = await self._user_repository.update(existing_user)

            return Response[UserResponse](
                data=UserResponse.model_validate(updated_user),
                message='Usuário atualizado com sucesso.',
                status_code=HTTPStatus.OK.value,
            )

        except ValueError as e:
            return Response[UserResponse](
                data=None,
                message=str(e),
                status_code=HTTPStatus.BAD_REQUEST.value,
            )
        except Exception:
            return Response[UserResponse](
                data=None,
                message='Erro interno do servidor.',
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )

    async def delete_user(self, user_id: UUID) -> Response[None]:
        """Remove um usuário"""
        try:
            success = await self._user_repository.delete(user_id)

            if not success:
                return Response[None](
                    data=None,
                    message='Usuário não encontrado.',
                    status_code=HTTPStatus.NOT_FOUND.value,
                )

            return Response[None](
                data=None,
                message='Usuário removido com sucesso.',
                status_code=HTTPStatus.NO_CONTENT.value,
            )

        except Exception:
            return Response[None](
                data=None,
                message='Erro interno do servidor.',
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            )
