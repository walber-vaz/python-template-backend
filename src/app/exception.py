from http import HTTPStatus
from typing import Any, Optional

from fastapi import HTTPException


class DetailedHTTPException(HTTPException):
    STATUS_CODE = HTTPStatus.INTERNAL_SERVER_ERROR
    DETAIL = (
        'Ops! tivermos um problema inesperado, tente novamente mais tarde.'
    )

    def __init__(
        self, detail: Optional[str] = None, **kwargs: dict[str, Any]
    ) -> None:
        super().__init__(
            status_code=self.STATUS_CODE,
            detail=detail if detail else self.DETAIL,
            **kwargs,
        )


class Success(DetailedHTTPException):
    STATUS_CODE = HTTPStatus.OK
    DETAIL = 'Sucesso'


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = HTTPStatus.FORBIDDEN
    DETAIL = 'Ops! Você não tem permissão para acessar esse recurso.'


class NotFound(DetailedHTTPException):
    STATUS_CODE = HTTPStatus.NOT_FOUND
    DETAIL = 'Ops! Não encontramos o que você estava procurando.'


class BadRequest(DetailedHTTPException):
    STATUS_CODE = HTTPStatus.BAD_REQUEST
    DETAIL = 'Ops! Ocorreu um erro inesperado, tente novamente mais tarde.'


class Conflict(DetailedHTTPException):
    STATUS_CODE = HTTPStatus.CONFLICT
    DETAIL = 'Ops! Ocorreu um erro inesperado, tente novamente mais tarde.'


class ServerError(DetailedHTTPException):
    STATUS_CODE = HTTPStatus.INTERNAL_SERVER_ERROR
    DETAIL = (
        'Ops! Tivermos um problema inesperado, tente novamente mais tarde.'
    )


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = HTTPStatus.UNAUTHORIZED
    DETAIL = 'Ops! Você não está autenticado para acessar esse recurso.'

    def __init__(self) -> None:
        super().__init__(headers={'WWW-Authenticate': 'Bearer'})
