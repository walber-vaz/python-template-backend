from typing import Dict, Protocol

from app.exceptions.user_exception import UserNotAuthenticated
from app.models import User
from app.repository.user import IUserRepositoryInterface
from app.schemas.user.user_login_input import UserLoginInput, UserLoginResponse
from app.services.auth import IAuthServiceInterface


class PasswordVerifierProtocol(Protocol):
    """Protocol para verificação de senhas"""

    def __call__(self, plain_password: str, hashed_password: str) -> bool: ...


class TokenCreatorProtocol(Protocol):
    """Protocol para criação de tokens"""

    def __call__(self, data: Dict[str, str]) -> str: ...


class AuthService(IAuthServiceInterface):
    def __init__(
        self,
        user_repository: IUserRepositoryInterface,
        password_verifier: PasswordVerifierProtocol,
        token_creator: TokenCreatorProtocol,
    ):
        self._user_repository = user_repository
        self._password_verifier = password_verifier
        self._token_creator = token_creator

    async def login(self, login_input: UserLoginInput) -> UserLoginResponse:
        """
        Autentica um usuário e retorna token de acesso

        Args:
            login_input: Dados de login (email e senha)

        Returns:
            UserLoginResponse: Resposta com token de acesso

        Raises:
            UserNotAuthenticated: Se credenciais inválidas
        """
        # Buscar usuário por email usando repositório injetado
        user: User | None = await self._user_repository.get_by_email(
            login_input.email
        )

        # Validar usuário e senha
        if not user or not self._password_verifier(
            login_input.password, user.password
        ):
            raise UserNotAuthenticated()

        # Criar token de acesso usando token creator injetado
        access_token = self._token_creator(data={'sub': str(user.id)})

        return UserLoginResponse(access_token=access_token)
