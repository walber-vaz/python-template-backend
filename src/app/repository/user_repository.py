from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.exceptions.user_exception import (
    UserEmailAlreadyExists,
    UserPhoneAlreadyExists,
)
from app.models import User


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)

    return result.scalar_one_or_none()


async def get_user_by_phone(phone: str, session: AsyncSession) -> User | None:
    stmt = select(User).where(User.phone == phone)
    result = await session.execute(stmt)

    return result.scalar_one_or_none()


async def get_user_by_id(user_id: UUID, session: AsyncSession) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)

    return result.scalar_one_or_none()


async def create_user(user: User, session: AsyncSession) -> User:
    existing_user_email = await get_user_by_email(user.email, session)
    if existing_user_email:
        raise UserEmailAlreadyExists

    existing_user_phone = await get_user_by_phone(user.phone, session)
    if existing_user_phone:
        raise UserPhoneAlreadyExists

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
    except IntegrityError as e:
        await session.rollback()
        raise ValueError(
            'Erro ao criar usuário. Verifique os dados informados.'
        ) from e
