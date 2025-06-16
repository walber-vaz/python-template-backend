from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(  # noqa: PLR6301
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ):
        response = await call_next(request)
        return response
