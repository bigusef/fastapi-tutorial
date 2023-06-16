from sqlalchemy import Column, String, Boolean

from config import Entity


class City(Entity):
    __tablename__ = "cities"

    name = Column(String(length=75), nullable=False)
    name_ar = Column(String(length=75), nullable=False)
    is_available = Column(Boolean, default=True)
