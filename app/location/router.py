from fastapi import APIRouter
from starlette import status

from config.dependency import RequestHeaders
from utilities.db.dependency import PagePaginator

from .repository import CountryRepository
from .schema import FullCountryData, CountryForm, CountryData

router = APIRouter(prefix="/location")


@router.get("/country")
async def list_country(repo: CountryRepository, _: RequestHeaders) -> list[CountryData]:
    data = await repo.select_all()
    return [CountryData.model_validate(i) for i in data]


@router.post("/country")
async def create_new_country(data: CountryForm, repo: CountryRepository) -> FullCountryData:
    instance = await repo.create(name_en=data.name_en, name_ar=data.name_ar)
    return FullCountryData.model_validate(instance)


@router.get("/country/full")
async def list_country_with_full_data(repo: CountryRepository, pager: PagePaginator) -> list[FullCountryData]:
    data = await repo.select_all(paginator=pager)
    return [FullCountryData.model_validate(i) for i in data]


@router.put("/country/{country_id}")
async def update_country(country_id: int, data: CountryForm, repo: CountryRepository) -> FullCountryData:
    instance = await repo.update(country_id, **data.model_dump())
    return FullCountryData.model_validate(instance)


@router.delete("/country/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(country_id: int, repo: CountryRepository):
    country = await repo.get_by_id(country_id)
    await repo.delete(country)
