from enum import StrEnum

from pydantic import BaseModel, Field

class Interval(StrEnum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"

class Type(StrEnum):
    WATERING = "WATERING"
    HAIRCUT = "HAIRCUT"
    ROTATION = "ROTATION"
    CLEANING = "CLEANING"
    TRANSPLANTATION = "TRANSPLANTATION"


class PlantIn(BaseModel):
    name: str
    image: str

    class Config:
        from_attributes = True


class PlantOut(BaseModel):
    id: int
    name: str
    image: str
    watering: int | None
    fertilizers: int | None
    haircut: int | None
    rotation: int | None
    cleaning: int | None
    transplantation: int | None

    class Config:
        from_attributes = True

    # watering: int | None = Field(1)
    # fertilizers: int | None = Field(1)
    # haircut: int | None = Field(1)
    # rotation: int | None = Field(1)
    # cleaning: int | None = Field(1)
    # transplantation: int | None = Field(1)