from .event import lifespan
from .middleware import active_language, RequestContextMiddleware
from .settings import get_settings, AppLanguage

settings = get_settings()

__all__ = ["settings", "lifespan", "AppLanguage", "RequestContextMiddleware", "active_language"]
