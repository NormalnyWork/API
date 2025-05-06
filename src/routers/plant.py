from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_session
from routers.auth import get_current_user
from schema.error import ErrorResponse
from schema.http_exeption import HttpException400, HttpException401
from schema.plant import PlantIn, CareType, CareIn, CareOut, PlantOut, PlantWithCareIn
from schema.user import UserOut
from service.plant_service import PlantService

responses = {
    400: {"model": HttpException400},
    401: {"model": HttpException401}
}

router = APIRouter(prefix="/plant", tags=["Plant"], responses=responses)


@router.post("", responses=responses)
async def create_plant_with_care(
    plant: PlantWithCareIn,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> int:
    plant_id = PlantService(db).create_plant_with_care(current_user.id, plant)
    return plant_id


@router.get("", responses={
    404: {
        "model": ErrorResponse,
        "description": "404\n- plant_not_found"},
})
async def get_plant(
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> list[PlantOut]:
    return PlantService(db).get_plants(current_user.id)


@router.patch("/{plant_id}", responses={
    404: {
        "model": ErrorResponse,
        "description": "404\n- plant_not_found"},
})
async def update_plant(
        plant_id: int,
        plant_patch: PlantIn,
        current_user: UserOut = Depends(get_current_user),
        db: Session = Depends(get_session)
) -> None:
    plant = PlantService(db).update_plant(plant_id, current_user.id, plant_patch)
    return plant


@router.put("/{plant_id}", responses={
    404: {
        "model": ErrorResponse,
        "description": "404\n- plant_not_found"},
})
async def update_plant_with_care(
    plant_id: int,
    plant_patch: PlantWithCareIn,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> None:
    PlantService(db).put_update_plant(plant_id, current_user.id, plant_patch)


@router.delete("/{plant_id}", responses={
    404: {
        "model": ErrorResponse,
        "description": "404\n- plant_not_found"},
})
async def delete_plant(
        plant_id: int,
        current_user: UserOut = Depends(get_current_user),
        db: Session = Depends(get_session)
) -> None:
    PlantService(db).delete_plant(plant_id, current_user.id)


@router.get("/care/{care_id}", responses={
    404: {
        "model": ErrorResponse,
        "description": "404\n- care_not_found"},
})
async def get_care(
        care_id: int,
        current_user: UserOut = Depends(get_current_user),
        db: Session = Depends(get_session)
) -> CareOut:
    care = PlantService(db).get_care(care_id, current_user.id)
    return care


@router.patch("/care/{care_id}", responses={
    404: {
        "model": ErrorResponse,
        "description": "404\n- care_not_found"},
})
async def update_care(
        care_id: int,
        care_patch: CareIn,
        current_user: UserOut = Depends(get_current_user),
        db: Session = Depends(get_session)
) -> None:
    care = PlantService(db).update_care(care_id, current_user.id, care_patch)
    return care


@router.delete("/care/{care_id}", responses={
    404: {
        "model": ErrorResponse,
        "description": "404\n- care_not_found"},
})
async def delete_care(
        care_id: int,
        current_user: UserOut = Depends(get_current_user),
        db: Session = Depends(get_session)
) -> None:
    PlantService(db).delete_care(care_id, current_user.id)

# @router.post("/care/{plant_id}", responses={
#     404: {
#         "model": ErrorResponse,
#         "description": "404\n- plant_not_found"},
# })
# async def create_care_plant(
#         plant_id: int,
#         care: List[CareIn],
#         current_user: UserOut = Depends(get_current_user),
#         db: Session = Depends(get_session)
# ) -> list[int]:
#     care_id = PlantService(db).create_care(plant_id, current_user.id, care)
#     return care_id
# @router.post("", responses=responses)
# async def create_plant(
#         plant: PlantIn,
#         current_user: UserOut = Depends(get_current_user),
#         db: Session = Depends(get_session)) -> int:
#     plant_id = PlantService(db).create_plant(current_user.id, plant)
#     return plant_id