from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: int = Field(default=None, primary_key=True)
    phone_number: str
    name: str | None
    email: EmailStr | None

    is_active: bool = True
    is_superuser: bool = False

    # sa_column_kwargs={"onupdate": datetime.utcnow}
    # TODO: check if last modify working as expected
    created: datetime = Field(default_factory=datetime.utcnow)
    last_modify: datetime = Field(default_factory=datetime.utcnow)
