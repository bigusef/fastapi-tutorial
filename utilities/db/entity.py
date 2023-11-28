from datetime import datetime

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

# Default naming convention for all indexes and constraints
# See why this is important and how it would save your time:
# https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    "all_column_names": lambda constraint, table: "_".join([column.name for column in constraint.columns.values()]),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class BaseEntity(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=convention)

    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def __repr__(self) -> str:
        return f"<Entity {self.__class__.__name__} #{self.id}>"


class StatusMixin(object):
    __abstract__ = True

    is_locked: Mapped[bool] = mapped_column(default=False)

    @property
    def is_active(self) -> bool:
        return not self.is_locked

    @is_active.setter
    def is_active(self, value) -> None:
        self.is_locked = not value  # type: ignore


class TimeStampMixin(object):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=datetime.utcnow)
