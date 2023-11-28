import uuid
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from config import AppLanguage
from utilities.db import StatusMixin, BaseEntity


class User(StatusMixin, BaseEntity):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    name: Mapped[str] = mapped_column(String(75), nullable=True)
    language: Mapped[AppLanguage]

    is_staff: Mapped[bool] = mapped_column(default=False)
    date_joined: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_login: Mapped[datetime] = mapped_column(nullable=True)
