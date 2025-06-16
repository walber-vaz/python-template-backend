from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    data: T | None = None
    message: str
    status_code: int
    error: str | None = None
