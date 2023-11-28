from contextvars import ContextVar

from uvicorn.config import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from .settings import AppLanguage

_lang: ContextVar[AppLanguage] = ContextVar(AppLanguage("en"))


def active_language() -> AppLanguage:
    return _lang.get()


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            lang = request.headers["accept-language"]
            user_language = AppLanguage(lang)
        except Exception as ex:
            logger.error(ex)
            user_language = AppLanguage("en")

        _lang.set(user_language)
        response = await call_next(request)
        return response
