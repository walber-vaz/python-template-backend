from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config import settings
from app.exception import DetailedHTTPException
from app.middlewares.response_middleware import ResponseMiddleware
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.utils.response_handler import ResponseHandler

app = FastAPI()

app.add_middleware(ResponseMiddleware)


@app.exception_handler(DetailedHTTPException)
async def detailed_http_exception_handler(
    request: Request, exc: DetailedHTTPException
):
    response_data = ResponseHandler.error(
        message=exc.detail,
        status_code=exc.status_code,
        error=type(exc).__name__,
    )
    return JSONResponse(
        status_code=exc.status_code, content=response_data.model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    response_data = ResponseHandler.error(
        message=exc.detail, status_code=exc.status_code, error='HTTPException'
    )
    return JSONResponse(
        status_code=exc.status_code, content=response_data.model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    response_data = ResponseHandler.error(
        message='Dados de entrada inválidos',
        status_code=HTTPStatus.BAD_REQUEST.value,
        error='ValidationError',
        data=exc.errors(),
    )
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST.value,
        content=response_data.model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    response_data = ResponseHandler.error(
        message='Ops! Tivemos um problema inesperado, tente novamente mais tarde.',  # noqa: E501
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        error=type(exc).__name__,
    )
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content=response_data.model_dump(),
    )


app.include_router(user_router, prefix=settings.API_PREFIX, tags=['Users'])
app.include_router(auth_router, prefix=settings.API_PREFIX, tags=['Auth'])
