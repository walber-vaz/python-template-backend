from pydantic import UUID4, ConfigDict

from .base import UserBase


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    is_active: bool
    id: UUID4

    model_config = ConfigDict(from_attributes=True)
