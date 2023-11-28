from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utilities.db import BaseEntity


class Country(BaseEntity):
    __tablename__ = "countries"

    name_en: Mapped[str] = mapped_column(String(50))
    name_ar: Mapped[str] = mapped_column(String(50))

    governorates: Mapped[list["Governorate"]] = relationship(back_populates="country", passive_deletes=True)


class Governorate(BaseEntity):
    name_en: Mapped[str] = mapped_column(String(75))
    name_ar: Mapped[str] = mapped_column(String(75))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="RESTRICT"), index=True)

    country: Mapped["Country"] = relationship(back_populates="governorates")
    cities: Mapped[list["City"]] = relationship(back_populates="governorate", passive_deletes=True)


class City(BaseEntity):
    __tablename__ = "cities"

    name_en: Mapped[str] = mapped_column(String(75))
    name_ar: Mapped[str] = mapped_column(String(75))
    governorate_id: Mapped[int] = mapped_column(ForeignKey("governorates.id", ondelete="RESTRICT"), index=True)

    governorate: Mapped["Governorate"] = relationship(back_populates="cities")
