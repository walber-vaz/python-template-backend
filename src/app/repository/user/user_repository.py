from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.exceptions.user_exception import (
    UserEmailAlreadyExists,
    UserPhoneAlreadyExists,
)
from app.models import User
from app.repository.user import IUserRepositoryInterface


class UserRepository(IUserRepositoryInterface):
    """Implementação concreta do repositório de usuários com SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> Optional[User]:
        """Busca usuário por telefone"""
        stmt = select(User).where(User.phone == phone)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Busca usuário por ID"""
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Cria um novo usuário com validações"""
        # Validar email único
        existing_user_email = await self.get_by_email(user.email)
        if existing_user_email:
            raise UserEmailAlreadyExists('Email já está em uso')

        # Validar telefone único
        existing_user_phone = await self.get_by_phone(user.phone)
        if existing_user_phone:
            raise UserPhoneAlreadyExists('Telefone já está em uso')

        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError(
                'Erro ao criar usuário. Verifique os dados informados.'
            ) from e

    async def update(self, user: User) -> User:
        """Atualiza um usuário existente"""
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError(
                'Erro ao atualizar usuário. Verifique os dados informados.'
            ) from e

    async def delete(self, user_id: UUID) -> bool:
        """Remove um usuário"""
        user = await self.get_by_id(user_id)
        if not user:
            return False

        try:
            await self.session.delete(user)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            raise ValueError('Erro ao deletar usuário') from e
