from http import HTTPStatus
from typing import Any, Optional, TypeVar

from app.schemas.response import Response

T = TypeVar('T')


class ResponseHandler:
    @staticmethod
    def success(
        data: Any = None,
        message: str = 'Sucesso',
        status_code: int = HTTPStatus.OK.value,
    ) -> Response[Any]:
        return Response(
            data=data, message=message, status_code=status_code, error=None
        )

    @staticmethod
    def error(
        message: str,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value,
        error: Optional[str] = None,
        data: Any = None,
    ) -> Response[Any]:
        return Response(
            data=data, message=message, status_code=status_code, error=error
        )
