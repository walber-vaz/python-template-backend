from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas.response import Response
from app.schemas.user.user_input_create import UserCreate, UserResponse


class IUserServiceInterface(ABC):
    """Interface para serviços de usuário"""

    @abstractmethod
    async def store(self, user: UserCreate) -> Response[UserResponse]:
        """Cria um novo usuário"""
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Response[UserResponse]:
        """Busca usuário por ID"""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Response[UserResponse]:
        """Busca usuário por email"""
        pass

    @abstractmethod
    async def update_user(
        self, user_id: UUID, user_data: UserCreate
    ) -> Response[UserResponse]:
        """Atualiza um usuário"""
        pass

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> Response[None]:
        """Remove um usuário"""
        pass
