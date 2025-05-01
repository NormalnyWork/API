from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_session
from routers.auth import get_current_user
from schema.http_exeption import HttpException400, HttpException401
from schema.plant import PlantIn, PlantOut
from schema.user import UserOut
from service.plant_service import PlantService

responses = {
    400: {"model": HttpException400},
    401: {"model": HttpException401}
}

router = APIRouter(prefix="/plant", tags=["Plant"], responses=responses)

@router.post("", responses=responses)
async def create_plant(
        plant: PlantIn,
        current_user: UserOut = Depends(get_current_user),
        db: Session = Depends(get_session)) -> int:
    plant_id = PlantService(db).create_plant(current_user.id, plant)
    return plant_id


@router.get("", responses=responses)
async def get_plant(
        current_user: UserOut = Depends(get_current_user),
        db: Session = Depends(get_session)) -> list[PlantOut]:
    plants = PlantService(db).get_plants(current_user.id)
    return plants