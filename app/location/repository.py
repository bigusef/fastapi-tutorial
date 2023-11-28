from typing import Annotated

from fastapi import Depends

from .domain import Country, Governorate, City
from utilities.db import Repository


class CountryRepository(Repository[Country]):
    pass


class GovernorateRepository(Repository[Governorate]):
    pass


class CityRepository(Repository[City]):
    pass


CountryRepository = Annotated[CountryRepository, Depends()]
GovernorateRepository = Annotated[GovernorateRepository, Depends()]
CityRepository = Annotated[CityRepository, Depends()]
