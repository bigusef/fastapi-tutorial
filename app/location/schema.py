from pydantic import BaseModel, Field, ConfigDict, model_validator

from config import active_language


class CountryData(BaseModel):
    id: int
    name: str

    @model_validator(mode="before")
    def set_name(cls, data):
        language_attribute = f"name_{active_language()}"
        name = getattr(data, language_attribute, data.name_en)
        setattr(data, "name", name)
        return data

    model_config = ConfigDict(from_attributes=True)


class CountryForm(BaseModel):
    name_en: str = Field(max_length=50)
    name_ar: str = Field(max_length=50)


class FullCountryData(CountryForm):
    id: int

    model_config = ConfigDict(from_attributes=True)
