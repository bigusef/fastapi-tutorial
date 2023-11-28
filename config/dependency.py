from typing import Annotated

from fastapi import Depends, Header
from pydantic import BaseModel

from config import AppLanguage


class RequestHeaders(BaseModel):
    accept_language: AppLanguage = Header(default=AppLanguage.ENGLISH)


RequestHeaders = Annotated[RequestHeaders, Depends()]
