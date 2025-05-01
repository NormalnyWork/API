from pydantic import BaseModel


class PlantIn(BaseModel):
    name: str
    image: str

    class Config:
        from_attributes = True


class PlantOut(BaseModel):
    id: int
    name: str
    image: str

    class Config:
        from_attributes = True