from abc import ABC, abstractmethod

from app.schemas.user.user_login_input import UserLoginInput, UserLoginResponse


class IAuthServiceInterface(ABC):
    """Interface para serviços de autenticação"""

    @abstractmethod
    async def login(self, login_input: UserLoginInput) -> UserLoginResponse:
        """Autentica um usuário e retorna token de acesso"""
        pass
