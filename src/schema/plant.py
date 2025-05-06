from enum import StrEnum
from typing import List, Optional, Annotated

from pydantic import BaseModel, Field

class Interval(StrEnum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"

class CareType(StrEnum):
    WATERING = "WATERING"
    HAIRCUT = "HAIRCUT"
    FERTILIZE = "FERTILIZE"
    ROTATION = "ROTATION"
    CLEANING = "CLEANING"
    TRANSPLANTATION = "TRANSPLANTATION"


class CareIn(BaseModel):
    interval: Interval
    count: int = Field(..., ge=1)

    class Config:
        from_attributes = True


class CareOut(BaseModel):
    id: int
    type: CareType
    interval: Interval
    count: Annotated[int, ...]

    class Config:
        from_attributes = True


class CareService(CareIn):
    id: int

    class Config:
        from_attributes = True


class PlantWithCareIn(BaseModel):
    name: str
    image: str
    WATERING: Optional[CareIn] | None = None
    HAIRCUT: Optional[CareIn] | None = None
    FERTILIZE: Optional[CareIn] = None
    ROTATION: Optional[CareIn] | None = None
    CLEANING: Optional[CareIn] | None = None
    TRANSPLANTATION: Optional[CareIn] | None = None

    class Config:
        extra = "forbid"
        from_attributes = True


class PlantOut(BaseModel):
    id: int
    name: str
    image: str
    WATERING: Optional[CareService] = None
    HAIRCUT: Optional[CareService] = None
    FERTILIZE: Optional[CareService] = None
    ROTATION: Optional[CareService] = None
    CLEANING: Optional[CareService] = None
    TRANSPLANTATION: Optional[CareService] = None

    class Config:
        from_attributes = True

class PlantIn(BaseModel):
    name: str
    image: str

    # @field_validator("count")
    # @classmethod
    # def convert_count_to_seconds(cls, count, info):
    #     interval = info.data.get("interval")
    #
    #     if not interval:
    #         raise ValueError("Interval must be provided to calculate count")
    #
    #     seconds_in_day = 86400
    #     multiplier = {
    #         Interval.DAY: 1,
    #         Interval.WEEK: 7,
    #         Interval.MONTH: 30,
    #     }.get(interval)
    #
    #     if not multiplier:
    #         raise ValueError(f"Unknown interval: {interval}")
    #
    #     if count == 0:
    #         raise ValueError("Count must be greater than 0")
    #
    #     return int(seconds_in_day * multiplier / count)

